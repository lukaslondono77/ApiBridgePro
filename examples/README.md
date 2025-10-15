# ApiBridge Pro - Examples

This directory contains examples demonstrating various features of ApiBridge Pro.

---

## 📁 Directory Structure

```
examples/
├── python/              # Python SDK examples
│   ├── weather_example.py
│   ├── github_example.py
│   └── multi_api_example.py
├── typescript/          # TypeScript SDK examples
│   ├── weather-example.ts
│   └── payment-example.ts
├── curl/                # curl command examples
│   ├── examples.sh
│   └── advanced_examples.sh
└── connectors/          # Connector templates
    ├── openai.yaml
    ├── stripe.yaml
    ├── twilio.yaml
    ├── sendgrid.yaml
    └── README.md
```

---

## 🚀 Quick Start Examples

### 1. Health Check

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "ok": true,
  "mode": "live",
  "connectors": ["weather_unified", "github", "slack"]
}
```

---

### 2. Weather API (Multi-Provider)

```bash
curl "http://localhost:8000/proxy/weather_unified/weather?q=London"
```

**Features demonstrated:**
- Multi-provider routing (OpenWeather + WeatherAPI)
- Automatic failover
- Response unification
- Caching

---

### 3. Python SDK

```python
from apibridge_client import ApiBridgeClient

async with ApiBridgeClient("http://localhost:8000") as client:
    # Get weather
    weather = await client.proxy("weather_unified", "/weather", params={"q": "London"})
    data = weather.json()
    print(f"Temperature: {data['temp_c']}°C")
```

**See:** `python/weather_example.py` for complete example

---

### 4. Budget Controls

```yaml
# In connectors.yaml
my_api:
  budget:
    monthly_usd_max: 100  # Never spend more than $100/month
    on_exceed: block      # Stop requests when limit hit
  cost_per_call_usd: 0.001
```

**Test:**
```bash
# Make requests until budget is hit
for i in {1..1000}; do
  curl http://localhost:8000/proxy/my_api/endpoint
done

# Eventually returns: {"error": "budget_exceeded"}
```

---

### 5. PII Protection

```yaml
# In connectors.yaml
customer_api:
  pii_protection:
    enabled: true
    auto_scan: true  # Auto-detect emails, SSNs, etc.
    action: encrypt  # Or redact, tokenize, hash
```

**Result:**
```json
{
  "email": "ENC_x9k2f...",  // Encrypted
  "ssn": "1**-**-***9"       // Redacted
}
```

---

## 🎓 Example Categories

### Beginner Examples
- `curl/examples.sh` - Basic curl commands
- `python/weather_example.py` - Simple weather API
- `connectors/stripe.yaml` - Payment API setup

### Intermediate Examples
- `python/multi_api_example.py` - Multiple APIs in one app
- `connectors/openai.yaml` - AI API with budget limits
- `typescript/weather-example.ts` - TypeScript SDK

### Advanced Examples
- Multi-provider with custom transforms
- OAuth2 auto-refresh configuration
- Multi-region deployment
- Custom error handling

---

## 🏃 Running the Examples

### Python Examples

```bash
cd examples/python

# Install SDK (if not already)
pip install httpx

# Run weather example
python weather_example.py --city Tokyo

# Compare multiple cities
python weather_example.py --compare

# Demonstrate caching
python weather_example.py --cache-demo
```

### curl Examples

```bash
cd examples/curl

# Make executable
chmod +x examples.sh

# Run all examples
./examples.sh
```

### TypeScript Examples

```bash
cd examples/typescript

# Install dependencies
npm install

# Run example
npm run example
```

---

## 📚 Connector Templates

### Available Templates

Located in `connectors/`:

- **AI/ML**
  - `openai.yaml` - OpenAI GPT models
  - `anthropic.yaml` - Anthropic Claude
  - `huggingface.yaml` - Hugging Face models

- **Payments**
  - `stripe.yaml` - Stripe payment processing
  - `paypal.yaml` - PayPal integration
  - `square.yaml` - Square payments

- **Communication**
  - `twilio.yaml` - SMS/Voice
  - `sendgrid.yaml` - Email sending
  - `mailgun.yaml` - Email API

- **Developer Tools**
  - `github.yaml` - GitHub API
  - `gitlab.yaml` - GitLab API
  - `slack.yaml` - Slack integration

### Using Templates

1. **Choose a template:**
   ```bash
   cp connectors/openai.yaml connectors.yaml
   # or append to existing connectors.yaml
   ```

2. **Set API keys:**
   ```bash
   export OPENAI_API_KEY=sk-...
   ```

3. **Restart ApiBridge:**
   ```bash
   make run
   ```

4. **Test:**
   ```bash
   curl http://localhost:8000/health
   # Should show new connector in list
   ```

---

## 🎯 Common Use Cases

### Use Case 1: Multi-Provider Weather

**Scenario:** Need weather data with 99.99% uptime

**Solution:**
```yaml
weather:
  providers:
    - {name: openweather, base_url: ...}
    - {name: weatherapi, base_url: ...}
  strategy: {policy: fastest_healthy_then_cheapest}
  cache_ttl_seconds: 300
```

**Benefit:** If one provider is down, automatically uses the other

---

### Use Case 2: Cost-Controlled AI

**Scenario:** Use OpenAI but prevent runaway costs

**Solution:**
```yaml
openai:
  budget:
    monthly_usd_max: 100
    on_exceed: block
  cost_per_call_usd: 0.002
```

**Benefit:** Automatically stops at $100, no surprise $10K bills

---

### Use Case 3: GDPR-Compliant Customer API

**Scenario:** Customer data with PII protection

**Solution:**
```yaml
customers:
  pii_protection:
    enabled: true
    field_rules:
      email: encrypt
      phone: tokenize
      ssn: redact
```

**Benefit:** Automatic GDPR compliance, no manual redaction

---

## 🔧 Tips & Tricks

### Tip 1: Test Connectors Locally

```bash
# Use record mode to test without hitting real APIs
export APIBRIDGE_MODE=record
make run

# Make requests (responses are recorded)
curl http://localhost:8000/proxy/myapi/endpoint

# Switch to replay mode
export APIBRIDGE_MODE=replay
make run

# Same request now served from recording (no API call!)
```

### Tip 2: Debug with Headers

```bash
# Check which provider was used
curl -i http://localhost:8000/proxy/weather/current | grep X-ApiBridge

# Output:
# X-ApiBridge-Provider: openweather
# X-ApiBridge-Latency-Ms: 145
# X-ApiBridge-Cache: miss
```

### Tip 3: Monitor Your Budget

```bash
# Check dashboard
open http://localhost:8000/admin

# Or get JSON
curl http://localhost:8000/admin/health-json | jq .budgets
```

---

## 📖 More Resources

- **Full Documentation:** See main README.md
- **Tutorials:** See TUTORIAL.md
- **Architecture:** See PROJECT_STRUCTURE.md
- **API Reference:** See QUICKSTART.md

---

## 🤝 Contributing Examples

Have a great example? We'd love to include it!

1. Create your example file
2. Test it thoroughly
3. Add clear documentation
4. Submit a PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Questions?** Open an issue or ask in Discord!

