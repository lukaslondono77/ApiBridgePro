# ApiBridge Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/tests-60%20passing-success)](https://github.com/lukaslondono77/ApiBridgePro/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Sponsor](https://img.shields.io/badge/Sponsor-💖-pink)](https://github.com/lukaslondono77)

**Enterprise-grade Universal API Gateway** with smart routing, PII protection, observability, and budget control.

One endpoint, any provider — with multi-provider routing, schema unification, budgets, and advanced security.

## ✨ Features

### Core Features
- **YAML Connectors**: Define auth, allowed paths, rate limits, retries, and caching in a simple YAML configuration
- **Multi-Provider Routing**: Fastest healthy provider with automatic failover
- **JMESPath Transforms**: Unify responses across different API providers
- **Budget Guardrails**: Track API costs with Redis or in-memory fallback
- **Schema-Drift Sentinel**: Validate responses against Pydantic models
- **Record/Replay Mode**: Record responses for development and CI testing

### Advanced Features ⭐ NEW
- **🔒 PII Firewall**: Automatic detection and protection of sensitive data with redact/tokenize/encrypt/hash options
- **🔑 OAuth2 Auto-Refresh**: Automatic client_credentials token management per provider
- **📊 Observability**: Prometheus metrics + OpenTelemetry distributed tracing
- **📈 Admin Dashboard**: Beautiful real-time dashboard for monitoring budgets, health, and cache statistics

## 🚀 Quick Start

### Run locally

```bash
# Set your API keys as environment variables
export OPENWEATHER_KEY=YOUR_KEY
export WEATHERAPI_KEY=YOUR_KEY
export GITHUB_TOKEN=ghp_xxx
export SLACK_BOT_TOKEN=xoxb-xxx

# Optional: Redis for budgets (falls back to memory)
export REDIS_URL=redis://localhost:6379/0

# Optional: Enable OpenTelemetry tracing
export OTEL_ENABLED=true
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Optional: Set PII encryption key (auto-generated if not set)
export PII_ENCRYPTION_KEY=your-secret-key-here

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Try it

**Health check:**
```bash
curl http://127.0.0.1:8000/health
```

**Admin Dashboard (NEW!):**
```
http://127.0.0.1:8000/admin
```
Beautiful real-time dashboard showing:
- System overview
- Budget tracking with visual indicators
- Provider health status
- Rate limiting status
- Cache statistics

**Prometheus Metrics (NEW!):**
```bash
curl http://127.0.0.1:8000/metrics
```

**Weather (unified response from multiple providers):**
```bash
# OpenWeatherMap or WeatherAPI (automatically routes to fastest healthy provider)
curl "http://127.0.0.1:8000/proxy/weather_unified/weather?q=Bogota"
# or
curl "http://127.0.0.1:8000/proxy/weather_unified/current.json?q=Bogota"
```

**GitHub user:**
```bash
curl http://127.0.0.1:8000/proxy/github/user
```

**Slack:**
```bash
curl -X POST "http://127.0.0.1:8000/proxy/slack/chat.postMessage" \
  -H "Content-Type: application/json" \
  -d '{"channel": "general", "text": "Hello from ApiBridge!"}'
```

## Docker

```bash
docker build -t apibridge-pro .
docker run -p 8000:8000 \
  -e OPENWEATHER_KEY=YOUR_KEY \
  -e WEATHERAPI_KEY=YOUR_KEY \
  -e GITHUB_TOKEN=ghp_xxx \
  apibridge-pro
```

## Record/Replay Mode

Perfect for development and CI/CD testing:

```bash
# Record mode - captures API responses
export APIBRIDGE_MODE=record
uvicorn app.main:app --reload --port 8000
# Make requests... responses are recorded in-memory

# Replay mode - serves recorded responses without hitting real APIs
export APIBRIDGE_MODE=replay
uvicorn app.main:app --reload --port 8000
```

## 📝 Configuration

Edit `connectors.yaml` to add or modify API connectors. Each connector supports:

### Basic Configuration
- `base_url` or `providers[]` for multi-provider setups
- `allow_paths`: Regex patterns for allowed endpoints
- `rate_limit`: Token bucket configuration
- `cache_ttl_seconds`: Response caching duration
- `transforms.response.jmes`: JMESPath expression for response transformation
- `budget`: Monthly USD limits with configurable actions
- `response_model`: Pydantic model name for schema validation

### Authentication Options
- `api_key_header`: API key in header
- `api_key_query`: API key in query parameter
- `bearer`: Static bearer token
- `oauth2_client_credentials`: Auto-refreshing OAuth2 tokens (NEW!)

### PII Protection (NEW!)
```yaml
pii_protection:
  enabled: true
  auto_scan: true           # Auto-detect PII patterns
  action: redact            # redact | tokenize | encrypt | hash
  field_rules:              # Or specify per-field rules
    email: encrypt
    ssn: redact
    phone: tokenize
    address: hash
```

### OAuth2 Example
```yaml
auth:
  type: oauth2_client_credentials
  token_url: https://auth.example.com/oauth/token
  client_id: ${OAUTH_CLIENT_ID}
  client_secret: ${OAUTH_CLIENT_SECRET}
  scope: "read write"
```

See `connectors_advanced.yaml` for comprehensive examples.

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         ApiBridge Gateway               │
│  ┌────────────────────────────────┐    │
│  │  Rate Limiting & Path Check    │    │
│  └──────────┬─────────────────────┘    │
│             ▼                           │
│  ┌────────────────────────────────┐    │
│  │  Cache Layer (GET requests)    │    │
│  └──────────┬─────────────────────┘    │
│             ▼                           │
│  ┌────────────────────────────────┐    │
│  │  Multi-Provider Routing        │    │
│  │  (Health + Latency Based)      │    │
│  └──────────┬─────────────────────┘    │
│             ▼                           │
│  ┌────────────────────────────────┐    │
│  │  JMESPath Transformation       │    │
│  └──────────┬─────────────────────┘    │
│             ▼                           │
│  ┌────────────────────────────────┐    │
│  │  Schema Validation (Optional)  │    │
│  └──────────┬─────────────────────┘    │
│             ▼                           │
│  ┌────────────────────────────────┐    │
│  │  Budget Tracking               │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
       │
       ▼
┌──────────────────┐
│  External APIs   │
└──────────────────┘
```

## 📊 Monitoring & Observability

### Prometheus Metrics

ApiBridge Pro exposes metrics at `/metrics`:

- `apibridge_requests_total` - Total requests by connector, method, status
- `apibridge_request_duration_seconds` - Request latency histogram
- `apibridge_upstream_requests_total` - Upstream provider requests
- `apibridge_upstream_duration_seconds` - Upstream latency
- `apibridge_cache_hits_total` - Cache hit count
- `apibridge_cache_misses_total` - Cache miss count
- `apibridge_rate_limit_exceeded_total` - Rate limit violations
- `apibridge_budget_spent_usd` - Current budget spending
- `apibridge_provider_health` - Provider health status (1=healthy, 0=unhealthy)
- `apibridge_schema_drift_total` - Schema drift detections

### OpenTelemetry Tracing

Enable distributed tracing:

```bash
export OTEL_ENABLED=true
export OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
```

Traces include:
- Gateway request spans
- Upstream provider calls
- Cache operations
- Transform operations

### Admin Dashboard

Access the admin dashboard at `/admin` for:
- Real-time system metrics
- Budget tracking with visual progress bars
- Provider health monitoring
- Rate limit status
- Cache statistics
- Auto-refresh every 10 seconds

## 🔒 PII Protection

ApiBridge Pro includes enterprise-grade PII protection:

### Auto-Scan Mode
Automatically detects and protects:
- Email addresses
- Social Security Numbers (SSN)
- Credit card numbers
- Phone numbers
- IP addresses

### Field-Level Protection
```yaml
pii_protection:
  enabled: true
  field_rules:
    user.email: encrypt      # Reversible encryption
    ssn: redact             # Masked output (e.g., "1**-**-***4")
    phone: tokenize         # Consistent hash token
    address: hash           # One-way hash
```

### Protection Actions
- **Redact**: Masks with asterisks (keeps first/last char)
- **Tokenize**: Deterministic token (same input → same token)
- **Encrypt**: Reversible encryption (requires `PII_ENCRYPTION_KEY`)
- **Hash**: One-way hash (irreversible)

## 🔑 OAuth2 Auto-Refresh

Automatic token management for OAuth2 client_credentials flow:

```yaml
auth:
  type: oauth2_client_credentials
  token_url: https://auth.example.com/oauth/token
  client_id: ${CLIENT_ID}
  client_secret: ${CLIENT_SECRET}
  scope: "read write"
  extra_params:           # Optional additional parameters
    audience: "https://api.example.com"
```

Features:
- Automatic token refresh before expiration
- Per-provider token caching
- Thread-safe token management
- Configurable scopes

## 📚 API Documentation

When running, visit:
- **Admin Dashboard**: http://127.0.0.1:8000/admin
- **Prometheus Metrics**: http://127.0.0.1:8000/metrics
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

To disable docs in production:
```bash
export DISABLE_DOCS=true
```

## 🏗️ Production Deployment

### Docker Compose Example

```yaml
version: '3.8'
services:
  apibridge:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
      - OTEL_ENABLED=true
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
      - PII_ENCRYPTION_KEY=${PII_ENCRYPTION_KEY}
    depends_on:
      - redis
      - jaeger

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "4317:4317"    # OTLP gRPC

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apibridge-pro
spec:
  replicas: 3
  selector:
    matchLabels:
      app: apibridge-pro
  template:
    metadata:
      labels:
        app: apibridge-pro
    spec:
      containers:
      - name: apibridge
        image: apibridge-pro:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_URL
          value: "redis://redis-service:6379/0"
        - name: OTEL_ENABLED
          value: "true"
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: "http://otel-collector:4317"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

For more details, see:
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community guidelines
- [SECURITY.md](SECURITY.md) - Security policy

## 💖 Sponsor This Project

<div align="center">

<a href="https://github.com/lukaslondono77">
  <img src="https://github.com/lukaslondono77.png" width="100" style="border-radius: 50%;" alt="Lukas Londono"/>
</a>

### **[Lukas Londono](https://github.com/lukaslondono77)**

[![Support the Project](https://img.shields.io/badge/Sponsor_Lukas_Londono-💖-pink?style=for-the-badge&logo=github)](https://github.com/lukaslondono77)

</div>

---

ApiBridge Pro is **100% open source** and maintained with love by **[Lukas Londono](https://github.com/lukaslondono77)**.

If you find this project useful and want to support ongoing development:

**Why sponsor?**
- ✨ Help maintain and improve ApiBridge Pro
- 🚀 Fund new features and integrations
- 📚 Support documentation and tutorials
- 🐛 Faster bug fixes and security updates
- 🌍 Keep this project free and open source for everyone

**What your sponsorship enables:**
- More connector templates (OpenAI, Stripe, Twilio, and 100+ more)
- Advanced features (GraphQL support, WebSocket proxying, gRPC)
- Performance improvements and optimizations
- Professional support and consulting
- Community events and workshops

**Other ways to support:**
- ⭐ Star this repository
- 🐦 Share on Twitter/LinkedIn
- 📝 Write a blog post or tutorial
- 🗣️ Speak about ApiBridge Pro at meetups
- 🤝 Contribute code, docs, or connector templates

Every contribution, big or small, makes a difference! 🙏

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

Copyright © 2025 [Lukas Londono](https://github.com/lukaslondono77)

