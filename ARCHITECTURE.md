# ApiBridge Pro - Architecture

This document provides a high-level overview of ApiBridge Pro's architecture, design decisions, and data flow.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT APPLICATION                    │
│                  (Your app, curl, browser)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Request
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    ApiBridge Pro Gateway                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  FastAPI Application (app/main.py)                     │ │
│  │                                                         │ │
│  │  Routes:                                                │ │
│  │    • /proxy/{connector}/{path}  ← Main proxy endpoint │ │
│  │    • /health                    ← Health check         │ │
│  │    • /metrics                   ← Prometheus metrics   │ │
│  │    • /admin                     ← Admin dashboard      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Gateway Layer (app/gateway.py)                        │ │
│  │                                                         │ │
│  │  Responsibilities:                                      │ │
│  │    1. Validate path against allow_paths                │ │
│  │    2. Check rate limits                                │ │
│  │    3. Check budget                                     │ │
│  │    4. Select best provider (multi-provider routing)    │ │
│  │    5. Transform request                                │ │
│  │    6. Make upstream call (with retries)                │ │
│  │    7. Transform response                               │ │
│  │    8. Apply PII protection                             │ │
│  │    9. Cache response (if GET)                          │ │
│  │   10. Return to client                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌──────────────┬──────────────┬──────────────┬───────────┐ │
│  │  Rate Limit  │   Caching    │   Budget     │  Health   │ │
│  │   (Token     │   (LRU/TTL)  │   Guard      │  Tracking │ │
│  │   Bucket)    │              │  (Redis/Mem) │   (EMA)   │ │
│  └──────────────┴──────────────┴──────────────┴───────────┘ │
│                                                               │
│  ┌──────────────┬──────────────┬──────────────┬───────────┐ │
│  │  Transforms  │    Drift     │     PII      │  OAuth2   │ │
│  │  (JMESPath)  │  Sentinel    │   Firewall   │  Manager  │ │
│  └──────────────┴──────────────┴──────────────┴───────────┘ │
└───────────────────────────┬───────────────────────────────┬──┘
                            │                               │
                   ┌────────▼────────┐             ┌────────▼─────────┐
                   │  Redis (optional)│             │   Prometheus     │
                   │                 │             │   (metrics)      │
                   │  • Budget state │             │                  │
                   │  • Rate limits  │             │  • Requests      │
                   │  • Cache        │             │  • Latency       │
                   └─────────────────┘             │  • Errors        │
                                                   └──────────────────┘
                            │
                   ┌────────▼────────┐
                   │   Upstream APIs │
                   │                 │
                   │  Provider 1     │
                   │  Provider 2     │
                   │  Provider 3...  │
                   └─────────────────┘
```

---

## 🔄 Request Flow (Detailed)

### 1. Request Arrival

```python
# Client makes request
GET /proxy/weather_unified/weather?q=London
```

**Entry Point:** `app/main.py::proxy_endpoint()`

### 2. Connector Lookup

```python
# Find connector config
connector = connectors["weather_unified"]
```

**Module:** `app/connectors.py`

### 3. Path Validation

```python
# Check if path is allowed
if not policy.path_allowed("/weather"):
    return 403 Forbidden
```

**Security Checks:**
- Regex whitelist match
- Path traversal prevention (`..`)
- URL normalization
- Double slash removal

### 4. Rate Limiting

```python
# Check token bucket
if not rate_limiter.consume():
    return 429 Too Many Requests
```

**Algorithm:** Token bucket
**Storage:** In-memory (per connector)

### 5. Budget Check

```python
# Check monthly budget
if budget_guard.would_exceed(connector, cost):
    return 402 Payment Required
```

**Storage:** Redis (with in-memory fallback)
**Tracking:** Per connector, per month

### 6. Provider Selection (Multi-Provider)

```python
# Pick best provider based on:
# - Health (circuit breaker state)
# - Latency (EMA, last 100 requests)
# - Weight (config priority)

provider = health_tracker.pick_best(providers)
```

**Module:** `app/health.py`

**Circuit Breaker States:**
- CLOSED: Normal operation
- OPEN: Too many failures (5+), skip for 60s
- HALF_OPEN: Testing recovery

### 7. Cache Check (GET only)

```python
if method == "GET":
    cached = cache.get(cache_key)
    if cached:
        return cached  # Cache hit!
```

**Cache Key:** `{connector}:{url}:{query_params}`
**Eviction:** TTL-based (configurable per connector)

### 8. Request Transform (Optional)

```python
# Apply JMESPath transform to request
if policy.transforms.request:
    body = jmespath.search(policy.transforms.request.jmes, body)
```

**Module:** `app/transforms.py`

### 9. Upstream Request

```python
# Make HTTP request to upstream API
# With:
# - Dynamic timeout (from config)
# - Retry logic (on 5xx, timeouts)
# - Circuit breaker awareness

response = await httpx_client.request(
    method=method,
    url=upstream_url,
    headers=headers,
    timeout=timeout_seconds
)
```

**HTTP Client:** `httpx.AsyncClient`
**Features:**
- HTTP/2 support
- Connection pooling (20 keepalive, 100 max)
- Automatic retries (configurable)

### 10. Response Transform (Optional)

```python
# Unify responses from different providers
if policy.transforms.response:
    data = jmespath.search(policy.transforms.response.jmes, data)
```

**Use Case:** Make OpenWeather + WeatherAPI return same format

### 11. Schema Drift Detection (Optional)

```python
# Validate response against expected schema
if policy.response_model:
    drift_detected = validate_schema(data, policy.response_model)
    if drift_detected:
        headers["X-Drift-Warning"] = "true"
```

**Module:** `app/drift.py`
**Technology:** Pydantic

### 12. PII Protection (Optional)

```python
# Auto-detect and protect sensitive data
if policy.pii_protection.enabled:
    data = pii_firewall.protect(data, policy.pii_protection)
```

**Module:** `app/pii_firewall.py`

**Protection Methods:**
- Redact: `email@example.com` → `e****@e****`
- Tokenize: `email@example.com` → `TOK_x9k2f...`
- Encrypt: `email@example.com` → `ENC_af2k9...`
- Hash: `email@example.com` → `HASH_8f3e1...`

### 13. Health Update

```python
# Update provider health metrics
if success:
    health_tracker.mark_success(provider, latency_ms)
else:
    health_tracker.mark_failure(provider)
```

**Tracking:**
- Success/failure counts
- Latency EMA (exponential moving average)
- Circuit breaker state

### 14. Budget Update

```python
# Increment cost tracking
budget_guard.increment(connector, cost_usd)
```

**Persistence:** Redis (or in-memory)

### 15. Cache Store (GET only)

```python
if method == "GET" and status_code == 200:
    cache.set(cache_key, response, ttl=cache_ttl_seconds)
```

### 16. Observability

```python
# Add debug headers
response.headers["X-ApiBridge-Provider"] = provider_name
response.headers["X-ApiBridge-Latency-Ms"] = str(latency_ms)
response.headers["X-ApiBridge-Cache"] = "hit" or "miss"

# Record Prometheus metrics
apibridge_requests_total.labels(connector, status_code).inc()
apibridge_latency.observe(latency_ms / 1000)
```

### 17. Return Response

```python
return JSONResponse(content=data, status_code=status_code, headers=headers)
```

---

## 🗂️ Module Responsibilities

### Core Modules

| Module | Responsibility | Key Functions |
|--------|----------------|---------------|
| `app/main.py` | FastAPI app, routes | `proxy_endpoint()`, `startup()`, `shutdown()` |
| `app/gateway.py` | Orchestrate request flow | `proxy()` |
| `app/connectors.py` | Parse & validate config | `ConnectorPolicy`, `path_allowed()` |
| `app/config.py` | Load YAML, expand env vars | `load_yaml()`, `expand_env()` |

### Feature Modules

| Module | Responsibility | Key Functions |
|--------|----------------|---------------|
| `app/rate_limit.py` | Token bucket rate limiting | `consume()` |
| `app/caching.py` | TTL-based response cache | `get()`, `set()` |
| `app/budget.py` | Cost tracking & enforcement | `would_exceed()`, `increment()` |
| `app/health.py` | Provider selection & circuit breaker | `pick_best()`, `mark_success()`, `mark_failure()` |
| `app/transforms.py` | JMESPath transforms | `apply_transform()` |
| `app/drift.py` | Schema validation | `validate_against_model()` |
| `app/pii_firewall.py` | PII detection & protection | `protect()`, `detect_pii()` |
| `app/oauth2_manager.py` | OAuth2 token auto-refresh | `get_token()`, `refresh_if_needed()` |
| `app/observability.py` | Prometheus & OpenTelemetry | `record_request()`, `start_span()` |
| `app/admin_ui.py` | Admin dashboard HTML | `generate_dashboard()` |

---

## 🔐 Security Architecture

### Defense Layers

1. **Path Validation** (Layer 1)
   - Regex whitelist
   - Path traversal prevention
   - URL normalization
   - Full match (not partial)

2. **Authentication** (Layer 2)
   - Secrets from environment only
   - Multiple auth methods supported
   - OAuth2 with auto-refresh

3. **Rate Limiting** (Layer 3)
   - Per-connector limits
   - Token bucket algorithm
   - Prevents DoS

4. **Budget Controls** (Layer 4)
   - Hard limits
   - Real-time tracking
   - Automatic blocking

5. **PII Protection** (Layer 5)
   - Auto-detection
   - Multiple protection methods
   - GDPR compliance

6. **Circuit Breaker** (Layer 6)
   - Prevents cascade failures
   - Auto-recovery
   - Configurable thresholds

---

## 📊 Data Flow

### Configuration Loading

```
connectors.yaml
       ↓
load_yaml() [config.py]
       ↓
expand_env() [config.py]
       ↓
ConnectorPolicy [connectors.py]
       ↓
Gateway [gateway.py]
```

### Request Processing

```
Client Request
       ↓
FastAPI Route [main.py]
       ↓
Gateway.proxy() [gateway.py]
       ↓
Path Validation [connectors.py]
       ↓
Rate Limit Check [rate_limit.py]
       ↓
Budget Check [budget.py]
       ↓
Provider Selection [health.py]
       ↓
Cache Check [caching.py]
       ↓
Transform Request [transforms.py]
       ↓
Upstream HTTP Call [httpx]
       ↓
Transform Response [transforms.py]
       ↓
Schema Validation [drift.py]
       ↓
PII Protection [pii_firewall.py]
       ↓
Update Health [health.py]
       ↓
Update Budget [budget.py]
       ↓
Cache Store [caching.py]
       ↓
Return to Client
```

---

## 🔄 Multi-Provider Routing

### Provider Selection Algorithm

```python
def pick_best(providers: list) -> Provider:
    """
    1. Filter out providers with OPEN circuit breakers
    2. Sort by:
       a. Health (prefer CLOSED over HALF_OPEN)
       b. Latency (EMA, lower is better)
       c. Weight (lower weight = higher priority)
    3. Return first provider
    """
```

### Circuit Breaker State Machine

```
           ┌──────────┐
           │  CLOSED  │ (Normal)
           └────┬─────┘
                │
    5+ failures │
                ▼
           ┌──────────┐
           │   OPEN   │ (Blocked)
           └────┬─────┘
                │
    60s timeout │
                ▼
           ┌──────────┐
           │ HALF_OPEN│ (Testing)
           └────┬─────┘
                │
     Success    │   Failure
        ┌───────┴────────┐
        ▼                ▼
    CLOSED            OPEN
```

### Latency Tracking (EMA)

```python
# Exponential Moving Average
# Gives more weight to recent requests

new_latency = 0.3 * current_latency + 0.7 * previous_ema
```

**Benefits:**
- Smooth out spikes
- Respond quickly to changes
- Memory efficient (single number)

---

## 💾 State Management

### In-Memory State

- **Rate Limit Tokens** (per connector)
- **Cache** (LRU eviction, TTL expiration)
- **Health Metrics** (latency EMA, circuit breaker)
- **Budget Fallback** (when Redis unavailable)

### Redis State (Optional)

- **Budget Tracking** (persistent, shared across instances)
- **Distributed Rate Limiting** (future)
- **Distributed Caching** (future)

**Key Format:**
```
budget:{connector}:{YYYY-MM}
rate_limit:{connector}
cache:{connector}:{url}:{query_hash}
```

---

## ⚡ Performance Optimizations

### 1. HTTP/2 Connection Pooling

```python
httpx.AsyncClient(
    http2=True,
    limits=httpx.Limits(
        max_keepalive_connections=20,
        max_connections=100
    )
)
```

**Benefit:** Reuse connections, reduce latency

### 2. Async/Await Throughout

```python
async def proxy(...):
    response = await httpx_client.request(...)
```

**Benefit:** Non-blocking I/O, handle 1000s of concurrent requests

### 3. Smart Caching

```python
# Only cache GET requests
# Only cache 2xx responses
# Use TTL to prevent stale data
```

**Benefit:** Reduce upstream API calls by 60-90%

### 4. Lazy Provider Selection

```python
# Only check health of providers we might use
# Skip providers with OPEN circuit breakers
```

**Benefit:** Reduce latency in normal operation

---

## 🧪 Testing Architecture

### Test Layers

1. **Unit Tests** (60 tests)
   - Individual modules in isolation
   - Mock external dependencies
   - Fast (< 1 second total)

2. **Integration Tests** (8 tests)
   - Full ASGI app
   - Mocked upstream APIs (httpx mock)
   - Test request flow end-to-end

3. **Benchmark Tests**
   - Load testing (concurrent requests)
   - Latency measurement (p50, p95, p99)
   - Regression detection

### Test Fixtures

```python
@pytest.fixture
def test_app():
    """Provide FastAPI app with lifespan management"""
    # Calls startup() and shutdown()
    
@pytest.fixture
def mock_upstream():
    """Mock external API responses"""
```

---

## 🚀 Deployment Architecture

### Single Instance (Simple)

```
┌─────────────────┐
│  ApiBridge Pro  │
│   (Docker)      │
│                 │
│  • FastAPI      │
│  • In-memory    │
│    state        │
└─────────────────┘
```

**Use Case:** Dev, testing, small production

### Multi-Instance (Scalable)

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Instance │  │ Instance │  │ Instance │
│    1     │  │    2     │  │    3     │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
              ┌────▼────┐
              │  Redis  │ (Shared state)
              └─────────┘
```

**Use Case:** High traffic, high availability

### Kubernetes (Enterprise)

```
┌────────────────────────────────────┐
│         Ingress / Load Balancer    │
└────────────┬───────────────────────┘
             │
   ┌─────────┴─────────┐
   │                   │
   ▼                   ▼
┌──────┐           ┌──────┐
│ Pod 1│           │ Pod 2│
└──┬───┘           └──┬───┘
   │                  │
   └────────┬─────────┘
            │
     ┌──────▼──────┐
     │ Redis       │
     │ (StatefulSet)│
     └─────────────┘
     
     ┌─────────────┐
     │ Prometheus  │
     │ (Monitoring)│
     └─────────────┘
```

**Features:**
- Auto-scaling (HPA based on CPU/memory)
- Rolling updates
- Health checks
- Resource limits

---

## 🔍 Observability

### Metrics (Prometheus)

```
apibridge_requests_total{connector, status_code}
apibridge_latency_seconds{connector}
apibridge_cache_hits_total{connector}
apibridge_cache_misses_total{connector}
apibridge_budget_current{connector}
apibridge_rate_limit_rejections{connector}
```

### Traces (OpenTelemetry)

```
Span: proxy_request
  Span: path_validation
  Span: rate_limit_check
  Span: budget_check
  Span: provider_selection
  Span: cache_check
  Span: upstream_request
  Span: response_transform
  Span: cache_store
```

### Logs (Structured)

```json
{
  "timestamp": "2025-10-15T10:30:00Z",
  "level": "INFO",
  "message": "Request completed",
  "connector": "weather_unified",
  "provider": "openweather",
  "latency_ms": 145,
  "status_code": 200,
  "cache": "miss"
}
```

---

## 🎯 Design Principles

### 1. **Zero-Code Configuration**
YAML config only, no code changes for new APIs

### 2. **Fail-Safe Defaults**
If a feature fails (e.g., Redis), fall back to working state

### 3. **Explicitness Over Magic**
Clear, predictable behavior. No hidden side effects.

### 4. **Performance-First**
Async, pooling, caching, minimal overhead

### 5. **Security-First**
Path validation, circuit breakers, budget controls

### 6. **Developer Experience**
Clear errors, observability, documentation

---

## 📚 Further Reading

- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Detailed file-by-file guide
- [PRINCIPAL_ENGINEER_REVIEW.md](PRINCIPAL_ENGINEER_REVIEW.md) - Performance & security analysis
- [ROADMAP_TO_WORLD_CLASS.md](ROADMAP_TO_WORLD_CLASS.md) - Future architecture plans

---

**Questions?** Open an issue or ask in Discord!

