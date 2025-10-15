# Contributing to ApiBridge Pro

Thank you for your interest in contributing to ApiBridge Pro! 🎉

We welcome contributions from everyone. This document provides guidelines for contributing to the project.

---

## 🌟 Ways to Contribute

### 1. **Add Connector Templates**
The most valuable contribution! Add pre-configured connectors for popular APIs.

**What we need:**
- Payment providers (Stripe, PayPal, Square, Adyen)
- Communication (Twilio, SendGrid, Mailgun, Slack)
- AI/ML (OpenAI, Anthropic, Cohere, Hugging Face)
- Data (Snowflake, BigQuery, Databricks)
- And many more!

**How to contribute a connector:**
1. Create a file in `connectors/community/{category}/{provider}.yaml`
2. Include clear documentation
3. Add usage examples
4. Test with real API (or well-documented test mode)
5. Submit PR with description

**Example:**
```yaml
# connectors/community/ai/openai.yaml
openai:
  base_url: https://api.openai.com/v1
  auth:
    type: bearer
    token: ${OPENAI_API_KEY}
  allow_paths:
    - "^/chat/completions$"
    - "^/completions$"
    - "^/embeddings$"
  rate_limit:
    capacity: 3500  # RPM limit for tier 1
    refill_per_sec: 58
  budget:
    monthly_usd_max: 100  # Prevent runaway costs
    on_exceed: block
  cost_per_call_usd: 0.002  # Estimate for gpt-3.5-turbo
```

### 2. **Improve Documentation**
- Fix typos or unclear explanations
- Add more examples
- Translate to other languages
- Create video tutorials

### 3. **Write Tests**
- Increase test coverage (target: 85%)
- Add integration tests
- Add performance tests
- Add security tests

### 4. **Fix Bugs**
- Check the [Issues](https://github.com/yourorg/apibridge-pro/issues) page
- Look for "good first issue" labels
- Reproduce the bug
- Submit a fix with tests

### 5. **Propose Features**
- Open an issue first to discuss
- Get feedback from maintainers
- Implement with tests
- Update documentation

---

## 🚀 Getting Started

### 1. **Fork the Repository**

Click the "Fork" button on GitHub.

### 2. **Clone Your Fork**

```bash
git clone https://github.com/YOUR_USERNAME/ApiBridgePro.git
cd ApiBridgePro
```

### 3. **Set Up Development Environment**

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests to ensure everything works
make test

# Start the development server
make run
```

### 4. **Create a Branch**

```bash
git checkout -b feature/my-awesome-feature
# or
git checkout -b fix/issue-123
```

### 5. **Make Your Changes**

- Write clear, documented code
- Follow existing code style
- Add tests for new functionality
- Update documentation

### 6. **Test Your Changes**

```bash
# Run all tests
make test

# Run linting
make lint

# Run type checking
make type

# Run security scan
make sec

# Or run everything
make ci
```

### 7. **Commit Your Changes**

```bash
git add .
git commit -m "feat: add OpenAI connector template"
# or
git commit -m "fix: resolve rate limiting issue #123"
```

**Commit message format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

### 8. **Push and Create Pull Request**

```bash
git push origin feature/my-awesome-feature
```

Then create a PR on GitHub with:
- Clear description of what changed
- Why the change is needed
- Any breaking changes
- Screenshots (if UI changes)

---

## 📝 Code Style Guidelines

### Python Code

**Follow PEP 8 with these specifics:**

```python
# Use type hints
async def my_function(name: str, age: int) -> dict[str, Any]:
    """Clear docstring explaining what this does."""
    return {"name": name, "age": age}

# Use descriptive variable names
connector_policy = load_connector("weather")  # Good
cp = load("w")  # Bad

# Keep functions small (< 50 lines ideal)
# Use early returns
def validate_path(path: str) -> bool:
    if not path:
        return False
    if '..' in path:
        return False
    return True
```

**Auto-format with:**
```bash
make format  # Uses ruff
```

### YAML Configs

```yaml
# Use consistent indentation (2 spaces)
connector_name:
  base_url: https://api.example.com
  auth:
    type: bearer
    token: ${API_KEY}  # Use ${ENV} for secrets
  
  # Add comments explaining non-obvious config
  cache_ttl_seconds: 300  # 5 minutes (typical API freshness)
```

### Tests

```python
def test_descriptive_name():
    """Test that X does Y when Z happens."""
    # Arrange
    input_data = {"key": "value"}
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

---

## 🧪 Testing Requirements

### All PRs Must:

1. **Pass existing tests**
   ```bash
   pytest tests/ -v
   ```

2. **Maintain or improve coverage**
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

3. **Pass linting**
   ```bash
   ruff check app/ tests/
   ```

4. **Pass type checking**
   ```bash
   mypy app/
   ```

5. **Pass security scan**
   ```bash
   bandit -r app/
   ```

### Writing Good Tests

```python
# Good test - clear, focused, independent
def test_cache_expires_after_ttl():
    """Test that cached entries expire after TTL"""
    cache_set("key", b"data", [], 200, ttl=1)
    assert get("key") is not None
    
    time.sleep(1.1)
    assert get("key") is None  # Expired

# Bad test - vague, depends on external state
def test_stuff():
    result = do_thing()
    assert result  # What are we testing?
```

---

## 📋 Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows project style (run `make format`)
- [ ] All tests pass (run `make test`)
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description explains the change
- [ ] Breaking changes are clearly marked

---

## 🏷️ Connector Contribution Guidelines

### Structure

```
connectors/community/
├── payments/
│   ├── stripe.yaml
│   ├── paypal.yaml
│   └── README.md
├── communication/
│   ├── twilio.yaml
│   ├── sendgrid.yaml
│   └── README.md
└── ai/
    ├── openai.yaml
    ├── anthropic.yaml
    └── README.md
```

### Template

```yaml
# connectors/community/{category}/{provider}.yaml

# Provider Name - Short Description
{provider_name}:
  base_url: https://api.{provider}.com
  
  # Authentication (choose appropriate method)
  auth:
    type: bearer  # or api_key_header, api_key_query, oauth2_client_credentials
    token: ${PROVIDER_API_KEY}
  
  # Allowed endpoints (be specific for security)
  allow_paths:
    - "^/v1/endpoint1$"
    - "^/v1/endpoint2$"
  
  # Performance tuning
  rate_limit:
    capacity: 100  # Based on provider limits
    refill_per_sec: 10
  
  cache_ttl_seconds: 60  # How long responses stay fresh
  
  # Cost management
  budget:
    monthly_usd_max: 100
    on_exceed: block
  cost_per_call_usd: 0.001  # Estimate from provider pricing
  
  # Optional: Transform responses for consistency
  transforms:
    response:
      jmes: '{id: id, status: status}'
  
  # Optional: PII protection
  pii_protection:
    enabled: true
    field_rules:
      email: encrypt
      phone: tokenize

# Documentation (in comments)
# 
# Setup:
#   1. Get API key from https://provider.com/api-keys
#   2. export PROVIDER_API_KEY=your_key
#   3. Add this connector to connectors.yaml
# 
# Usage:
#   curl http://localhost:8000/proxy/{provider_name}/v1/endpoint1
# 
# Rate Limits:
#   Free tier: 100 req/min
#   Paid tier: 1000 req/min
# 
# Cost:
#   $0.001 per request (estimate)
```

### Documentation Required

Each connector must include:
1. **Setup instructions** - How to get API keys
2. **Usage examples** - curl or SDK examples
3. **Rate limits** - Provider's limits
4. **Cost estimates** - Approximate pricing
5. **Common use cases** - What it's good for

---

## 💬 Communication

### Questions?

- **Discord:** Join our community server (link in README)
- **GitHub Discussions:** For feature requests and general questions
- **GitHub Issues:** For bugs and specific problems

### Getting Help

- Read the [documentation](docs/)
- Check [existing issues](https://github.com/yourorg/apibridge-pro/issues)
- Ask in Discord #help channel
- Tag maintainers in your PR (if needed)

---

## 🎯 What We're Looking For

### High Priority

1. **Connector templates** for popular APIs
2. **Bug fixes** with tests
3. **Documentation improvements**
4. **Performance optimizations** with benchmarks
5. **Security improvements**

### Medium Priority

1. Additional language SDKs (Go, Rust, Java)
2. Grafana dashboards
3. Deployment guides for more platforms
4. Translation to other languages

### Nice to Have

1. Video tutorials
2. Blog posts
3. Conference talks
4. Social media promotion

---

## ⭐ Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Eligible for swag (stickers, t-shirts)
- Featured in blog posts (for major contributions)
- Invited to contributor calls

Top contributors may be invited to:
- Core team
- Early access to features
- Influence roadmap

---

## 🚫 Code of Conduct

We follow the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

**In short:**
- Be respectful and inclusive
- Welcome newcomers
- Focus on what's best for the community
- Show empathy

**Not tolerated:**
- Harassment
- Discrimination
- Trolling
- Personal attacks

Violations will result in warnings or bans.

---

## 📜 License

By contributing to ApiBridge Pro, you agree that your contributions will be licensed under the MIT License.

---

## 🎉 Thank You!

Every contribution makes ApiBridge Pro better for everyone. Whether it's a typo fix or a major feature, we appreciate your help!

**Let's build something amazing together! 🚀**

---

## 📚 Additional Resources

- [Quick Start Guide](QUICK_START.md)
- [Architecture Documentation](PROJECT_STRUCTURE.md)
- [API Reference](https://docs.apibridgepro.com)
- [Discord Community](https://discord.gg/apibridge)
- [Roadmap](ROADMAP_TO_WORLD_CLASS.md)

---

**Questions? Open an issue or ask in Discord!**

