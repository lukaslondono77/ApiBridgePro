# Security Policy

## 🔒 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in ApiBridge Pro, please report it responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please email: **security@apibridgepro.com**

Or use GitHub's private vulnerability reporting:
1. Go to the Security tab
2. Click "Report a vulnerability"
3. Fill out the form

### What to Include

Please include:

1. **Description** - What is the vulnerability?
2. **Impact** - What could an attacker do?
3. **Steps to Reproduce** - How can we reproduce it?
4. **Affected Versions** - Which versions are affected?
5. **Suggested Fix** - If you have ideas

### What to Expect

- **Acknowledgment** within 24 hours
- **Initial Assessment** within 72 hours
- **Regular Updates** every 3-5 days
- **Fix Timeline** depends on severity:
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

---

## 🛡️ Security Best Practices

### For Users

**1. Keep Dependencies Updated**

```bash
pip install --upgrade -r requirements.txt
```

**2. Use Environment Variables for Secrets**

```bash
# Good
export OPENAI_API_KEY=sk-...

# Bad - Don't hardcode in connectors.yaml!
auth:
  token: sk-hardcoded-key-bad-idea
```

**3. Restrict Allow Paths**

```yaml
# Good - Specific paths only
allow_paths:
  - "^/api/v1/users$"
  - "^/api/v1/posts$"

# Bad - Too permissive
allow_paths:
  - "^/.*$"  # Allows everything!
```

**4. Enable PII Protection**

```yaml
pii_protection:
  enabled: true
  auto_scan: true  # Auto-detect sensitive data
  action: encrypt
```

**5. Set Budget Limits**

```yaml
budget:
  monthly_usd_max: 100  # Prevent runaway costs
  on_exceed: block
```

**6. Use HTTPS in Production**

Never run ApiBridge Pro with HTTP in production. Always use HTTPS with valid certificates.

**7. Regular Security Audits**

```bash
# Run security scan
make sec

# Check for dependency vulnerabilities
pip-audit
```

---

## 🔐 Security Features

### Built-in Protection

1. **Path Validation**
   - Regex whitelist for allowed endpoints
   - Path traversal protection
   - URL normalization

2. **Rate Limiting**
   - Per-connector limits
   - Token bucket algorithm
   - Distributed rate limiting (with Redis)

3. **Budget Enforcement**
   - Real-time cost tracking
   - Hard limits
   - Automatic blocking

4. **PII Protection**
   - Auto-detection (email, SSN, credit cards, etc.)
   - Multiple protection methods (redact, tokenize, encrypt, hash)
   - GDPR/CCPA compliance

5. **Circuit Breaker**
   - Prevents cascade failures
   - Auto-recovery
   - DoS mitigation

6. **Authentication**
   - Multiple auth methods supported
   - OAuth2 token auto-refresh
   - Secrets from environment only

---

## 🚨 Known Security Considerations

### 1. Secrets Management

**Current:** Secrets stored in environment variables

**Recommendation for Production:**
- Use AWS Secrets Manager
- Use HashiCorp Vault
- Use Kubernetes Secrets
- Enable secret rotation

### 2. Network Security

**Ensure:**
- Run behind firewall
- Use private networks for Redis
- Enable TLS for all connections
- Use security groups/network policies

### 3. Logging

**Be Careful:**
- Don't log API keys
- Don't log sensitive request/response data
- Enable PII protection for logs
- Use structured logging

---

## 🏆 Security Hall of Fame

We recognize security researchers who responsibly disclose vulnerabilities:

| Researcher | Vulnerability | Date | Bounty |
|------------|---------------|------|---------|
| (Your name here!) | (Description) | (Date) | $X |

---

## 📚 Security Resources

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [httpx Security](https://www.python-httpx.org/advanced/)

---

## 🔄 Security Update Process

### For Maintainers

1. **Receive Report** → Acknowledge within 24h
2. **Assess Severity** → Critical/High/Medium/Low
3. **Develop Fix** → Create private branch
4. **Test Fix** → Comprehensive testing
5. **Prepare Release** → Security advisory draft
6. **Coordinate Disclosure** → Agree on timeline
7. **Release Fix** → Publish update
8. **Public Disclosure** → After users can update

### Severity Levels

**Critical** (CVSS 9.0-10.0)
- Remote code execution
- Authentication bypass
- Data exposure

**High** (CVSS 7.0-8.9)
- Privilege escalation
- SQL injection
- XSS

**Medium** (CVSS 4.0-6.9)
- DoS
- Information disclosure
- CSRF

**Low** (CVSS 0.1-3.9)
- Minor information leaks
- Low-impact bugs

---

## ✅ Secure Development Lifecycle

All code changes go through:

1. **Code Review** - At least one maintainer review
2. **Automated Scanning** - Bandit security scan
3. **Dependency Check** - pip-audit for vulnerabilities
4. **Test Coverage** - Security-specific tests
5. **Documentation** - Security implications documented

---

## 🙏 Thank You

Thank you for helping keep ApiBridge Pro secure for everyone!

**Report vulnerabilities:** security@apibridgepro.com

---

Last updated: 2025-10-15

