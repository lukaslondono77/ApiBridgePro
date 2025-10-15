import logging
import time
from typing import Optional

import httpx
import orjson
from fastapi import HTTPException, Request, Response
from pydantic import BaseModel

from .budget import BudgetGuard
from .caching import get as cache_get
from .caching import set as cache_set
from .connectors import ConnectorPolicy
from .drift import validate_response
from .health import mark_failure, mark_success, pick_best
from .oauth2_manager import get_oauth2_manager
from .observability import MetricsCollector, trace_operation
from .pii_firewall import PIIAction, get_firewall
from .rate_limit import allow as rl_allow
from .transforms import apply_transform_jmes

logger = logging.getLogger(__name__)

# Registry for optional response models (schema drift checks)
MODEL_REGISTRY: dict[str, type[BaseModel]] = {}

def register_model(name: str, model: type[BaseModel]):
    MODEL_REGISTRY[name] = model

def _build_headers_passthrough(resp: httpx.Response, allowed: list[str]) -> dict[str, str]:
    return {k: v for k, v in resp.headers.items() if k.lower() in allowed}

async def _apply_auth(cfg: dict, headers: dict[str, str], params: dict[str, str], provider_key: str) -> tuple[dict[str, str], dict[str, str]]:
    t = cfg.get("type")
    if t == "api_key_header":
        headers[cfg["name"]] = cfg["value"]
    elif t == "api_key_query":
        params[cfg["name"]] = cfg["value"]
    elif t == "bearer":
        headers["Authorization"] = f"Bearer {cfg['token']}"
    elif t == "oauth2_client_credentials":
        # Auto-refresh OAuth2 token
        oauth2_mgr = get_oauth2_manager()
        token = await oauth2_mgr.get_token(
            provider_key=provider_key,
            token_url=cfg["token_url"],
            client_id=cfg["client_id"],
            client_secret=cfg["client_secret"],
            scope=cfg.get("scope"),
            extra_params=cfg.get("extra_params")
        )
        headers["Authorization"] = f"Bearer {token}"
    return headers, params

def cache_key(connector: str, url: str, method: str, query: str) -> str:
    return f"{connector}:{method}:{url}?{query}"

class Gateway:
    def __init__(self, policies: dict[str, ConnectorPolicy], budget: BudgetGuard):
        self.policies = policies
        # Create client with reasonable defaults, will override per-request
        self.client = httpx.AsyncClient(
            http2=True, 
            timeout=httpx.Timeout(15.0, connect=5.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
        self.budget = budget

    async def close(self):
        await self.client.aclose()

    @trace_operation("gateway.proxy")
    async def proxy(self, connector: str, full_path: str, request: Request) -> Response:
        start_time = time.time()
        if connector not in self.policies:
            raise HTTPException(404, f"Unknown connector '{connector}'")
        policy = self.policies[connector]

        if not policy.path_allowed(f"/{full_path}"):
            raise HTTPException(403, "Path not allowed by connector policy")

        # rate limit
        if not rl_allow(f"rl:{connector}", policy.rate.get("capacity",10), policy.rate.get("refill_per_sec",5)):
            MetricsCollector.record_rate_limit(connector)
            raise HTTPException(429, "Rate limit exceeded")

        # build base request
        method = request.method.upper()
        incoming_headers = dict(request.headers)
        incoming_headers.pop("host", None)
        incoming_headers.pop("content-length", None)
        params = dict(request.query_params)
        body = await request.body()

        # pick provider(s)
        providers = []
        if policy.providers:
            providers = pick_best(policy.providers)
        elif policy.base_url:
            p = {"name": "default", "base_url": policy.base_url, "weight": 1, "__key": f"{connector}:default"}
            providers = [p]
        else:
            raise HTTPException(500, "Connector misconfigured (no base_url/providers)")

        # caching for GET
        query_str = request.url.query
        ck = None
        if policy.cache_ttl > 0 and method == "GET":
            target_preview = providers[0]["base_url"].rstrip("/") + "/" + full_path
            ck = cache_key(connector, target_preview, method, query_str)
            cached = cache_get(ck)
            if cached:
                MetricsCollector.record_cache_hit(connector)
                content, hdrs, status = cached
                duration = time.time() - start_time
                MetricsCollector.record_request(connector, method, status, duration)
                return Response(content=content, status_code=status,
                                headers={k.decode(): v.decode() for k, v in hdrs})

        if policy.cache_ttl > 0 and method == "GET":
            MetricsCollector.record_cache_miss(connector)

        # Per-connector timeout from strategy
        timeout_seconds = policy.strategy.get("timeout_ms", 15000) / 1000
        request_timeout = httpx.Timeout(timeout_seconds, connect=5.0)
        
        # Retry configuration from strategy
        max_retries = policy.strategy.get("retries", 0)
        
        # try providers in order
        errors: list[str] = []
        for prov in providers:
            base_url = prov["base_url"].rstrip("/")
            url = f"{base_url}/{full_path}"
            headers = dict(incoming_headers)
            qparams = dict(params)
            headers, qparams = await _apply_auth(policy.auth or prov.get("auth", {}), headers, qparams, prov["__key"])
            # static injections
            headers.update(policy.static_headers)
            qparams.update(policy.static_params)

            # Retry loop
            for attempt in range(max_retries + 1):
                t0 = time.time()
                try:
                    resp = await self.client.request(
                        method=method, 
                        url=url, 
                        headers=headers, 
                        params=qparams,
                        content=(body if body else None),
                        timeout=request_timeout  # Use per-connector timeout
                    )
                    latency_ms = int((time.time() - t0) * 1000)
                    
                    # Record upstream metrics
                    MetricsCollector.record_upstream(connector, prov.get("name", "default"), resp.status_code, latency_ms / 1000)

                    if 200 <= resp.status_code < 300:
                        mark_success(prov["__key"], latency_ms)
                        MetricsCollector.update_provider_health(connector, prov.get("name", "default"), True)

                        raw = resp.content
                        out_headers = _build_headers_passthrough(resp, policy.passthrough_headers)
                        content = raw
                        meta = {"provider": prov.get("name","default"), "status": resp.status_code, "latency_ms": latency_ms}

                        # transform (JMES) if JSON
                        if resp.headers.get("content-type","").startswith("application/json"):
                            try:
                                data = resp.json()
                            except Exception:
                                data = None
                            if data is not None:
                                data = apply_transform_jmes(data, policy.transforms.get("response",{}).get("jmes"), meta)

                                # PII protection (if configured)
                                pii_cfg = policy.cfg.get("pii_protection")
                                if pii_cfg and pii_cfg.get("enabled"):
                                    firewall = get_firewall()
                                    if pii_cfg.get("auto_scan"):
                                        action = PIIAction(pii_cfg.get("action", "redact"))
                                        data = firewall.auto_scan(data, action)
                                    elif pii_cfg.get("field_rules"):
                                        field_rules = {k: PIIAction(v) for k, v in pii_cfg["field_rules"].items()}
                                        data = firewall.process_dict(data, field_rules)

                                # schema drift check
                                drift = None
                                if policy.response_model_name and policy.response_model_name in MODEL_REGISTRY:
                                    drift = validate_response(MODEL_REGISTRY[policy.response_model_name], data)
                                if drift:
                                    MetricsCollector.record_schema_drift(connector)
                                    out_headers["x-apibridge-drift"] = "1"
                                    out_headers["x-apibridge-drift-msg"] = drift[:180]
                                content = orjson.dumps(data)

                        # budget guard (simple per-call estimate)
                        if policy.cost_per_call_usd and policy.cost_per_call_usd > 0:
                            await self.budget.add_cost(connector, policy.cost_per_call_usd)
                            if policy.budget and policy.budget.get("monthly_usd_max"):
                                spent = await self.budget.get_cost(connector)
                                # Update metrics
                                MetricsCollector.update_budget(connector, time.strftime("%Y-%m"), spent)
                                if spent > float(policy.budget["monthly_usd_max"]):
                                    budget_action = policy.budget.get("on_exceed","block")
                                    if budget_action == "block":
                                        duration = time.time() - start_time
                                        MetricsCollector.record_request(connector, method, 402, duration)
                                        return Response(status_code=402, content=b'{"error":"budget_exceeded"}',
                                                        media_type="application/json")
                                    # "downgrade_provider" means: continue; the sorted list already prefers lower weight/cheaper
                                    out_headers["x-apibridge-budget"] = f"exceeded:{spent:.2f}"

                        # cache
                        if ck and policy.cache_ttl > 0 and method == "GET":
                            cache_set(ck, content, [(k.encode(), v.encode()) for k, v in out_headers.items()],
                                      resp.status_code, policy.cache_ttl)

                        # Record final metrics
                        duration = time.time() - start_time
                        MetricsCollector.record_request(connector, method, resp.status_code, duration)
                        
                        # Add observability headers
                        out_headers["X-ApiBridge-Provider"] = prov.get("name", "default")
                        out_headers["X-ApiBridge-Latency-Ms"] = str(latency_ms)
                        out_headers["X-ApiBridge-Cache"] = "miss"

                        return Response(content=content, status_code=resp.status_code, headers=out_headers)

                    # non-2xx - retry on 5xx if retries configured
                    if resp.status_code >= 500 and attempt < max_retries:
                        logger.warning(f"Provider {prov.get('name')} returned {resp.status_code}, retrying ({attempt+1}/{max_retries})")
                        continue  # Retry
                    
                    # Final failure after retries - try next provider
                    mark_failure(prov["__key"])
                    MetricsCollector.update_provider_health(connector, prov.get("name", "default"), False)
                    errors.append(f"{prov.get('name')}: {resp.status_code}")
                    break  # Exit retry loop, try next provider
                    
                except httpx.TimeoutException as e:
                    # Timeout - retry if configured
                    if attempt < max_retries:
                        logger.warning(f"Provider {prov.get('name')} timed out, retrying ({attempt+1}/{max_retries})")
                        continue
                    mark_failure(prov["__key"])
                    MetricsCollector.update_provider_health(connector, prov.get("name", "default"), False)
                    errors.append(f"{prov.get('name')}: timeout after {timeout_seconds}s")
                    break
                    
                except Exception as e:
                    # Other errors - retry if configured
                    if attempt < max_retries:
                        logger.warning(f"Provider {prov.get('name')} error: {e}, retrying ({attempt+1}/{max_retries})")
                        continue
                    mark_failure(prov["__key"])
                    MetricsCollector.update_provider_health(connector, prov.get("name", "default"), False)
                    errors.append(f"{prov.get('name')}: {type(e).__name__}: {e}")
                    break

        # All providers failed
        duration = time.time() - start_time
        MetricsCollector.record_request(connector, method, 502, duration)
        raise HTTPException(502, f"Upstream error(s): {', '.join(errors)}")

