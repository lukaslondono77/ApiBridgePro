# ApiBridge Pro - Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -e ".[dev]"
```

### 2. Set Environment Variables
```bash
export OPENWEATHER_KEY=your_key_here
export WEATHERAPI_KEY=your_key_here  
export GITHUB_TOKEN=ghp_your_token
export REDIS_URL=redis://localhost:6379/0  # optional
```

### 3. Run the Server
```bash
make run
# or
uvicorn app.main:app --reload --port 8000
```

### 4. Test It
```bash
# Health check
curl http://127.0.0.1:8000/health

# Admin dashboard
open http://127.0.0.1:8000/admin

# Metrics
curl http://127.0.0.1:8000/metrics

# API Documentation
open http://127.0.0.1:8000/docs
```

---

## 📋 Make Commands

```bash
make help          # Show all commands
make dev           # Install dev dependencies
make run           # Start development server
make test          # Run tests with coverage
make test-fast     # Run tests without coverage
make lint          # Check code style
make lint-fix      # Auto-fix linting issues
make format        # Format code
make type          # Run type checker
make sec           # Security scan
make quality       # Run lint + type + sec
make ci            # Run all CI checks
make clean         # Remove cache/build files
make docker        # Build Docker image
make docker-run    # Run Docker container
```

---

## 🧪 Running Tests

```bash
# All tests with coverage
pytest -v --cov=app --cov-report=term-missing

# Specific test file
pytest tests/test_cache.py -v

# Specific test
pytest tests/test_cache.py::test_cache_set_and_get -v

# With coverage HTML report
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

---

## 🐳 Docker

```bash
# Build image
docker build -t apibridge-pro:latest .

# Run container
docker run -p 8000:8000 \
  -e OPENWEATHER_KEY=${OPENWEATHER_KEY} \
  -e WEATHERAPI_KEY=${WEATHERAPI_KEY} \
  apibridge-pro:latest

# With docker-compose (full stack)
docker-compose up --build

# With observability stack
docker-compose --profile observability up
```

---

## 📊 Monitoring

### Prometheus Metrics
```bash
curl http://127.0.0.1:8000/metrics
```

**Key Metrics:**
- `apibridge_requests_total` - Total requests
- `apibridge_request_duration_seconds` - Latency histogram
- `apibridge_cache_hits_total` - Cache performance
- `apibridge_provider_health` - Provider status
- `apibridge_budget_spent_usd` - Cost tracking

### Admin Dashboard
```
http://127.0.0.1:8000/admin
```

Shows:
- System overview
- Budget tracking
- Provider health
- Rate limiting status
- Cache statistics

### Distributed Tracing
```bash
export OTEL_ENABLED=true
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

---

## 🔧 Configuration

### connectors.yaml
```yaml
my_api:
  base_url: https://api.example.com
  auth: {type: bearer, token: ${MY_API_TOKEN}}
  allow_paths:
    - "^/users/.*$"
    - "^/posts$"
  rate_limit: {capacity: 100, refill_per_sec: 10}
  cache_ttl_seconds: 60
  budget:
    monthly_usd_max: 100
    on_exceed: block
  cost_per_call_usd: 0.001
```

### Multi-Provider Setup
```yaml
weather:
  providers:
    - name: provider1
      base_url: https://api.provider1.com
      auth: {type: api_key_query, name: key, value: ${PROVIDER1_KEY}}
      weight: 1
    - name: provider2
      base_url: https://api.provider2.com
      auth: {type: api_key_query, name: apikey, value: ${PROVIDER2_KEY}}
      weight: 2
  strategy: {policy: fastest_healthy_then_cheapest}
  transforms:
    response:
      jmes: '{temp: temperature, city: location.name}'
```

---

## 🔐 Security Features

### PII Protection
```yaml
sensitive_api:
  pii_protection:
    enabled: true
    auto_scan: true  # Auto-detect PII
    action: redact   # redact | tokenize | encrypt | hash
    # OR field-specific rules:
    field_rules:
      email: encrypt
      ssn: redact
      phone: tokenize
```

### OAuth2 Auto-Refresh
```yaml
oauth_api:
  auth:
    type: oauth2_client_credentials
    token_url: https://auth.example.com/token
    client_id: ${CLIENT_ID}
    client_secret: ${CLIENT_SECRET}
    scope: "read write"
```

---

## 🐛 Troubleshooting

### Tests Failing
```bash
# Clear cache and retry
make clean
make test
```

### Import Errors
```bash
# Reinstall in editable mode
pip install -e ".[dev]"
```

### Redis Connection Issues
```bash
# Check Redis is running
redis-cli ping

# Or disable Redis (uses in-memory fallback)
unset REDIS_URL
```

### Type Check Errors
```bash
# Ignore third-party library warnings
mypy app/ --ignore-missing-imports
```

---

## 📚 File Structure

```
apibridge-pro/
├── app/
│   ├── main.py              # FastAPI app + routes
│   ├── gateway.py           # Proxy logic + routing
│   ├── connectors.py        # Connector policy parsing
│   ├── rate_limit.py        # Token bucket rate limiting
│   ├── caching.py           # In-memory TTL cache
│   ├── budget.py            # Cost tracking
│   ├── transforms.py        # JMESPath transforms
│   ├── drift.py             # Schema validation
│   ├── health.py            # Provider health tracking
│   ├── pii_firewall.py      # PII protection
│   ├── oauth2_manager.py    # OAuth2 token management
│   ├── observability.py     # Prometheus + OTEL
│   └── admin_ui.py          # Admin dashboard
├── tests/
│   ├── test_cache.py
│   ├── test_rate_limit.py
│   ├── test_transforms.py
│   ├── test_drift.py
│   ├── test_budget.py
│   ├── test_provider_routing.py
│   └── test_proxy_integration.py
├── connectors.yaml          # Connector configuration
├── pyproject.toml           # Dependencies + tool configs
├── Makefile                 # Development commands
├── Dockerfile               # Container build
├── docker-compose.yml       # Multi-service deployment
└── .github/workflows/ci.yml # CI/CD pipeline
```

---

## 🎯 Common Tasks

### Add a New Connector
1. Edit `connectors.yaml`:
   ```yaml
   my_new_api:
     base_url: https://api.example.com
     auth: {type: bearer, token: ${MY_TOKEN}}
     allow_paths: ["^/.*$"]
   ```
2. Restart server: `make run`
3. Test: `curl http://localhost:8000/proxy/my_new_api/endpoint`

### Add a New Provider to Existing Connector
```yaml
existing_api:
  providers:
    - name: existing
      base_url: https://api1.example.com
    - name: new_provider  # Add this
      base_url: https://api2.example.com
      weight: 2  # Lower priority
```

### Enable Record/Replay for Testing
```bash
# Record responses
export APIBRIDGE_MODE=record
make run
# Make requests...

# Replay without hitting real APIs
export APIBRIDGE_MODE=replay
make run
```

### View Coverage Report
```bash
make test
open htmlcov/index.html
```

---

## 📞 Support

- **Documentation:** See README.md and IMPROVEMENTS.md
- **Issues:** Check test results and logs
- **Contributing:** Follow code style (ruff + mypy)

---

**Quick Links:**
- Health: http://localhost:8000/health
- Admin: http://localhost:8000/admin
- Metrics: http://localhost:8000/metrics
- Docs: http://localhost:8000/docs


