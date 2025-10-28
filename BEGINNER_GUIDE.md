# 🚀 Beginner's Guide: ApiBridge Pro vs FastAPI

## What's the Difference?

### FastAPI - Build Your Own APIs
**FastAPI** is a web framework that helps you **build APIs**. Think of it as a tool to create new API endpoints.

**Example:** You build a FastAPI app that handles user registration:
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/users")
def create_user(name: str):
    return {"id": 1, "name": name}
```

### ApiBridge Pro - Connect to Existing APIs
**ApiBridge Pro** is an **API Gateway** that helps you **connect to and manage existing APIs**. Think of it as a smart proxy/router for APIs that already exist.

**Example:** You use ApiBridge Pro to connect to CoinGecko API:
```bash
# Call Bitcoin price through ApiBridge
GET http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd
```

---

## 📊 Simple Comparison

| | FastAPI | ApiBridge Pro |
|---|---|---|
| **Purpose** | Build new APIs | Connect to existing APIs |
| **Use When** | Creating endpoints | Calling external APIs |
| **Example** | Create `/users` endpoint | Call `/proxy/coingecko/simple/price` |
| **Output** | Your own API | Proxied external API response |

---

## 🎯 When to Use Each?

### Use **FastAPI** When:
✅ You're building a new API from scratch  
✅ You need custom business logic  
✅ You're creating database-backed endpoints  
✅ You want full control over responses  

**Example Use Cases:**
- Building a todo app API
- Creating a user authentication system
- Building a blog API
- Creating custom business endpoints

### Use **ApiBridge Pro** When:
✅ You need to call external APIs (OpenAI, Stripe, etc.)  
✅ You want to add features like caching, rate limiting, PII protection  
✅ You have multiple API providers and want failover  
✅ You want to unify different API schemas  
✅ You need to control costs and budgets  

**Example Use Cases:**
- Calling OpenAI/Anthropic APIs with caching
- Integrating payment APIs (Stripe) with budget limits
- Calling weather APIs with multiple providers and failover
- Calling cryptocurrency APIs with rate limiting

---

## 💡 Can You Use Both Together?

**YES!** They work perfectly together:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Browser   │────▶│  Your FastAPI│────▶│ ApiBridge   │────▶ External APIs
│   / Client  │     │   App        │     │   Pro       │     (OpenAI, Stripe)
└─────────────┘     └──────────────┘     └─────────────┘
                          │
                          │ Your custom logic
                          ▼
                    ┌─────────────┐
                    │  Database   │
                    └─────────────┘
```

**Example:** Your FastAPI app calls external APIs through ApiBridge Pro:

```python
from fastapi import FastAPI
from httpx import AsyncClient

app = FastAPI()

@app.get("/my-endpoint")
async def my_endpoint():
    # Call external API through ApiBridge Pro
    async with AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/proxy/coingecko/simple/price",
            params={"ids": "bitcoin", "vs_currencies": "usd"}
        )
        bitcoin_price = response.json()
    
    # Your custom logic
    return {
        "bitcoin_price": bitcoin_price,
        "your_data": "processed here"
    }
```

---

## 🎓 Beginner Examples

### Example 1: Simple FastAPI App (Building Your Own API)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.post("/users")
def create_user(name: str, email: str):
    # Your custom logic here
    return {"id": 1, "name": name, "email": email}
```

**Run it:**
```bash
uvicorn main:app --reload
```

**Use it:**
```bash
curl http://localhost:8000/hello
curl -X POST http://localhost:8000/users?name=John&email=john@example.com
```

---

### Example 2: ApiBridge Pro (Connecting to External APIs)

**1. Configure connector** (`connectors.yaml`):
```yaml
coingecko:
  base_url: https://api.coingecko.com/api/v3
  allow_paths:
    - "^/simple/price$"
  cache_ttl_seconds: 60
  rate_limit:
    capacity: 50
    refill_per_sec: 1
```

**2. Start ApiBridge Pro:**
```bash
apibridge
```

**3. Use it:**
```bash
# Get Bitcoin price (cached, rate-limited)
curl http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd
```

---

### Example 3: Combining Both (Recommended!)

**Your FastAPI app uses ApiBridge Pro to call external APIs:**

```python
from fastapi import FastAPI
from httpx import AsyncClient

app = FastAPI(title="My App")

async def get_bitcoin_price():
    """Get Bitcoin price through ApiBridge Pro"""
    async with AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/proxy/coingecko/simple/price",
            params={"ids": "bitcoin", "vs_currencies": "usd"}
        )
        return response.json()

@app.get("/bitcoin")
async def bitcoin():
    """Your custom endpoint that uses ApiBridge Pro"""
    price_data = await get_bitcoin_price()
    
    # Add your custom logic
    return {
        "bitcoin_usd": price_data["bitcoin"]["usd"],
        "timestamp": "2025-01-01T12:00:00Z",
        "your_custom_field": "value"
    }

@app.get("/health")
def health():
    """Your own health check"""
    return {"status": "ok"}
```

**Setup:**
```bash
# Terminal 1: Start ApiBridge Pro
apibridge

# Terminal 2: Start your FastAPI app
uvicorn main:app --reload --port 8001
```

**Use it:**
```bash
# Your custom endpoint
curl http://localhost:8001/bitcoin

# Direct API call through ApiBridge
curl http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd
```

---

## 🎯 Real-World Use Cases

### Use Case 1: AI Chat App
**Scenario:** You're building a ChatGPT clone

- **FastAPI:** Handle user authentication, chat history, database
- **ApiBridge Pro:** Call OpenAI/Anthropic APIs with:
  - Cost tracking (budget limits)
  - Caching (save money on repeated questions)
  - Rate limiting (prevent abuse)
  - PII protection (remove sensitive data)

### Use Case 2: E-commerce Site
**Scenario:** Online store with payments

- **FastAPI:** Product catalog, user accounts, orders
- **ApiBridge Pro:** 
  - Stripe payments (with budget limits)
  - Shipping API (with failover if one provider is down)
  - Analytics API (with caching)

### Use Case 3: Weather Dashboard
**Scenario:** Show weather for multiple cities

- **FastAPI:** User preferences, saved locations
- **ApiBridge Pro:**
  - Weather API with caching (save API calls)
  - Multiple weather providers (failover if one is down)
  - Rate limiting (prevent too many requests)

---

## 🎓 Learning Path

### Beginner: Start with FastAPI
1. Install: `pip install fastapi uvicorn`
2. Create simple endpoints
3. Learn about HTTP methods (GET, POST, etc.)
4. Understand request/response

### Intermediate: Add ApiBridge Pro
1. Install: `pip install apibridge-pro` (when published) or from GitHub
2. Connect to one external API (e.g., CoinGecko)
3. See how caching/rate limiting works
4. Combine with your FastAPI app

### Advanced: Full Integration
1. Connect multiple APIs
2. Use failover providers
3. Implement budget controls
4. Add PII protection
5. Set up monitoring/observability

---

## 🔗 Quick Links

### FastAPI
- **Learn:** https://fastapi.tiangolo.com/tutorial/
- **Docs:** https://fastapi.tiangolo.com/

### ApiBridge Pro
- **Install:** `pip install git+https://github.com/lukaslondono77/ApiBridgePro.git`
- **Guide:** See `PACKAGE_GUIDE.md`
- **Examples:** See `examples/` folder
- **Demos:** See `demos/` folder

---

## ❓ Common Questions

**Q: Can I use ApiBridge Pro without FastAPI?**  
A: Yes! ApiBridge Pro is a standalone API gateway. You can use it from any client (Python, JavaScript, curl, etc.)

**Q: Do I need to know FastAPI to use ApiBridge Pro?**  
A: No, but it helps! ApiBridge Pro uses FastAPI internally, but you can use it just like any REST API.

**Q: When should I use ApiBridge Pro vs calling APIs directly?**  
A: Use ApiBridge Pro when you need caching, rate limiting, cost control, failover, or PII protection. For simple one-off API calls, direct calls are fine.

**Q: Is ApiBridge Pro free?**  
A: Yes! It's open-source and free to use.

---

## 🚀 Ready to Start?

1. **Learn FastAPI first** (if you haven't): https://fastapi.tiangolo.com/tutorial/
2. **Try ApiBridge Pro:** Clone the repo and try the demos
3. **Combine them:** Build your own FastAPI app that uses ApiBridge Pro

Happy coding! 🎉

