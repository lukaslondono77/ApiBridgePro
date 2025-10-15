import re
from typing import Any
from urllib.parse import unquote


class ConnectorPolicy:
    def __init__(self, name: str, cfg: dict[str, Any]):
        self.name = name
        self.cfg = cfg
        self.base_url = cfg.get("base_url")
        self.providers: list[dict[str, Any]] = []
        if "providers" in cfg:
            # multi-provider
            for i, p in enumerate(cfg["providers"]):
                p = dict(p)
                p["__key"] = f"{name}:{p.get('name','p'+str(i))}"
                self.providers.append(p)
        self.allow_paths = cfg.get("allow_paths", ["^.*$"])
        self.rate = cfg.get("rate_limit", {"capacity": 10, "refill_per_sec": 5})
        self.cache_ttl = int(cfg.get("cache_ttl_seconds", 0))
        self.strategy = cfg.get("strategy", {"policy": "fastest_healthy_then_cheapest", "timeout_ms": 20000, "retries": 1})
        self.auth = cfg.get("auth", {})
        self.static_headers = cfg.get("static_headers", {})
        self.static_params = cfg.get("static_params", {})
        self.transforms = cfg.get("transforms", {})  # {"response":{"jmes": "..."}}
        self.budget = cfg.get("budget")  # {"monthly_usd_max": X, "on_exceed": "downgrade_provider|block"}
        self.passthrough_headers = [h.lower() for h in cfg.get("passthrough_headers", ["content-type"])]
        self.response_model_name = cfg.get("response_model")  # optional string key to a registered model
        self.cost_per_call_usd = float(cfg.get("cost_per_call_usd", 0.0))

    def path_allowed(self, path: str) -> bool:
        """
        Validate path against allow_paths with security hardening.
        - Normalizes URL encoding
        - Prevents path traversal (../)
        - Prevents double slashes
        - Uses fullmatch for exact matching
        """
        # Normalize path to prevent bypasses
        normalized = unquote(path)  # Decode %2F, %2E%2E, etc.
        normalized = normalized.replace('//', '/')  # Remove double slashes
        normalized = normalized.rstrip('/')  # Remove trailing slash

        # Prevent path traversal
        if '..' in normalized:
            return False

        # Ensure starts with /
        if not normalized.startswith('/'):
            normalized = '/' + normalized

        # Use fullmatch instead of match for exact matching
        return any(re.fullmatch(p, normalized) for p in self.allow_paths)

def build_connector_policies(config: dict[str, Any]) -> dict[str, ConnectorPolicy]:
    return {name: ConnectorPolicy(name, cfg) for name, cfg in config.items()}


