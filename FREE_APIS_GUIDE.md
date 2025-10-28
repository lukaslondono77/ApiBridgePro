# 🌐 Free APIs to Connect to ApiBridge Pro

This guide shows you how to get FREE API keys and connect real APIs to your ApiBridge Pro gateway.

---

## 🚀 Quick Start: 5 Free APIs (No Credit Card!)

### 1. OpenWeatherMap (Weather Data) ☁️

**What it does:** Get weather data for any city worldwide

**Get API Key (FREE):**
1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (FREE tier: 1,000 calls/day)
3. Verify email
4. Go to: https://home.openweathermap.org/api_keys
5. Copy your API key

**Configure ApiBridge:**
```bash
export OPENWEATHER_KEY=your_api_key_here
```

**Test it:**
```bash
curl "http://localhost:8000/proxy/weather_unified/weather?q=London"
```

**Already configured in:** `connectors.yaml` ✅

---

### 2. GitHub API (Repository Data) 🐙

**What it does:** Access GitHub repos, users, issues, etc.

**Get API Token (FREE):**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "ApiBridge Pro"
4. Scopes: Select `public_repo`, `read:user`
5. Click "Generate token"
6. Copy the token (starts with `ghp_`)

**Configure ApiBridge:**
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

**Test it:**
```bash
curl http://localhost:8000/proxy/github/user
```

**Already configured in:** `connectors.yaml` ✅

---

### 3. JSONPlaceholder (Mock Data - No Key Needed!) 🎭

**What it does:** Free fake REST API for testing

**No API key needed!** Just add to your connectors:

```yaml
# Add to connectors.yaml
jsonplaceholder:
  base_url: https://jsonplaceholder.typicode.com
  allow_paths:
    - "^/posts$"
    - "^/posts/.*$"
    - "^/users$"
    - "^/users/.*$"
    - "^/comments$"
  cache_ttl_seconds: 300
  rate_limit:
    capacity: 100
    refill_per_sec: 10
```

**Test it:**
```bash
curl http://localhost:8000/proxy/jsonplaceholder/posts
curl http://localhost:8000/proxy/jsonplaceholder/users/1
```

**Website:** https://jsonplaceholder.typicode.com

---

### 4. CoinGecko (Cryptocurrency Prices) 💰

**What it does:** Get crypto prices, market data (Bitcoin, Ethereum, etc.)

**No API key needed for demo!** (50 calls/minute free)

```yaml
# Add to connectors.yaml
coingecko:
  base_url: https://api.coingecko.com/api/v3
  allow_paths:
    - "^/simple/price$"
    - "^/coins/markets$"
    - "^/coins/.*$"
  cache_ttl_seconds: 60
  rate_limit:
    capacity: 50
    refill_per_sec: 1
```

**Test it:**
```bash
curl "http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd"
```

**Website:** https://www.coingecko.com/en/api

---

### 5. REST Countries (Country Data) 🌍

**What it does:** Get data about countries (population, capital, flag, etc.)

**No API key needed!**

```yaml
# Add to connectors.yaml
restcountries:
  base_url: https://restcountries.com/v3.1
  allow_paths:
    - "^/name/.*$"
    - "^/alpha/.*$"
    - "^/all$"
  cache_ttl_seconds: 86400  # 24 hours (data rarely changes)
  rate_limit:
    capacity: 100
    refill_per_sec: 10
```

**Test it:**
```bash
curl http://localhost:8000/proxy/restcountries/name/colombia
curl http://localhost:8000/proxy/restcountries/alpha/co
```

**Website:** https://restcountries.com

---

## 💳 Premium APIs (Free Tiers Available)

### 6. OpenAI (ChatGPT API) 🤖

**What it does:** GPT models, text generation, embeddings

**Get API Key:**
1. Go to: https://platform.openai.com/signup
2. Sign up (free $5 credit for new accounts!)
3. Go to: https://platform.openai.com/api-keys
4. Create new key
5. Copy key (starts with `sk-`)

**Configure:**
```bash
export OPENAI_API_KEY=sk-your_key_here
```

**Use connector from:** `examples/connectors/openai.yaml`

**Free tier:** $5 credit initially

---

### 7. Stripe (Payments) 💳

**What it does:** Process payments, manage subscriptions

**Get API Key:**
1. Go to: https://dashboard.stripe.com/register
2. Sign up (FREE for development)
3. Get your test API key
4. Copy from: https://dashboard.stripe.com/test/apikeys

**Configure:**
```bash
export STRIPE_SECRET_KEY=sk_test_your_key_here
```

**Use connector from:** `examples/connectors/stripe.yaml`

**Free tier:** Unlimited test transactions

---

### 8. SendGrid (Email) 📧

**What it does:** Send emails programmatically

**Get API Key:**
1. Go to: https://signup.sendgrid.com
2. Sign up (FREE: 100 emails/day)
3. Go to: Settings → API Keys
4. Create API key
5. Copy key (starts with `SG.`)

**Configure:**
```bash
export SENDGRID_API_KEY=SG.your_key_here
```

**Use connector from:** `examples/connectors/sendgrid.yaml`

**Free tier:** 100 emails/day forever

---

### 9. Twilio (SMS & Voice) 📱

**What it does:** Send SMS, make phone calls

**Get API Key:**
1. Go to: https://www.twilio.com/try-twilio
2. Sign up (FREE $15 credit)
3. Get Account SID and Auth Token
4. From: https://console.twilio.com

**Configure:**
```bash
export TWILIO_ACCOUNT_SID=ACxxxx
export TWILIO_AUTH_TOKEN=your_token
```

**Use connector from:** `examples/connectors/twilio.yaml`

**Free tier:** $15 credit

---

### 10. WeatherAPI (Better Weather Data) 🌦️

**What it does:** Weather, forecasts, astronomy

**Get API Key:**
1. Go to: https://www.weatherapi.com/signup.aspx
2. Sign up (FREE: 1M calls/month!)
3. Get your API key
4. From: https://www.weatherapi.com/my/

**Configure:**
```bash
export WEATHERAPI_KEY=your_key_here
```

**Already configured in:** `connectors.yaml` ✅

**Free tier:** 1,000,000 calls/month

---

## 🎯 Recommended Free APIs for Testing

### No API Key Needed (Start Immediately!)

| API | What it does | Website |
|-----|--------------|---------|
| **JSONPlaceholder** | Fake data for testing | https://jsonplaceholder.typicode.com |
| **REST Countries** | Country information | https://restcountries.com |
| **CoinGecko** | Crypto prices | https://coingecko.com/en/api |
| **PokeAPI** | Pokemon data | https://pokeapi.co |
| **Dog API** | Random dog pictures | https://dog.ceo/dog-api |
| **Cat Facts** | Random cat facts | https://catfact.ninja |
| **IP API** | IP geolocation | https://ip-api.com |

### Free Tier with API Key

| API | Free Tier | Website |
|-----|-----------|---------|
| **OpenWeatherMap** | 1K calls/day | https://openweathermap.org/api |
| **WeatherAPI** | 1M calls/month | https://weatherapi.com |
| **GitHub** | 5K req/hour | https://github.com/settings/tokens |
| **SendGrid** | 100 emails/day | https://sendgrid.com |
| **Twilio** | $15 credit | https://twilio.com |
| **OpenAI** | $5 credit | https://platform.openai.com |
| **Stripe** | Unlimited test | https://stripe.com |
| **Alpha Vantage** | 25 req/day | https://alphavantage.co |
| **ExchangeRate** | 1,500 req/month | https://exchangerate-api.com |

---

## 📋 How to Add Any API to ApiBridge Pro

### Step 1: Get the API Key

Go to the API provider's website and sign up.

### Step 2: Create Connector Config

Add to `connectors.yaml`:

```yaml
my_api:
  base_url: https://api.example.com
  
  auth:
    type: bearer  # or api_key_header, api_key_query, basic
    token: ${MY_API_KEY}
  
  allow_paths:
    - "^/endpoint1$"
    - "^/endpoint2$"
  
  rate_limit:
    capacity: 100
    refill_per_sec: 10
  
  cache_ttl_seconds: 60
  
  budget:
    monthly_usd_max: 10
    on_exceed: block
  
  cost_per_call_usd: 0.001
```

### Step 3: Set Environment Variable

```bash
export MY_API_KEY=your_actual_api_key
```

### Step 4: Restart ApiBridge

```bash
uvicorn app.main:app --reload --port 8000
```

### Step 5: Test It!

```bash
curl http://localhost:8000/proxy/my_api/endpoint1
```

---

## 🎓 Complete Example: Add PokeAPI

Let's add Pokemon API (no key needed!):

### 1. Add to connectors.yaml:

```yaml
pokemon:
  base_url: https://pokeapi.co/api/v2
  allow_paths:
    - "^/pokemon$"
    - "^/pokemon/.*$"
    - "^/ability/.*$"
  cache_ttl_seconds: 3600  # Pokemon data doesn't change
  rate_limit:
    capacity: 100
    refill_per_sec: 10
```

### 2. Restart server:

```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Test:

```bash
# Get Pikachu data
curl http://localhost:8000/proxy/pokemon/pokemon/pikachu

# Get all Pokemon (paginated)
curl "http://localhost:8000/proxy/pokemon/pokemon?limit=10"
```

Done! You now have Pokemon API connected! 🎮

---

## 🏆 Best Free APIs by Category

### 🤖 AI & Machine Learning
- **OpenAI** - GPT, DALL-E ($5 free credit)
- **Hugging Face** - AI models (free tier)
- **Cohere** - NLP models ($25 free credit)

### 💰 Finance & Crypto
- **CoinGecko** - Crypto prices (free, no key)
- **Alpha Vantage** - Stock data (25 req/day free)
- **ExchangeRate API** - Currency conversion (1,500 req/month)

### 🌦️ Weather
- **OpenWeatherMap** - 1K calls/day free
- **WeatherAPI** - 1M calls/month free
- **Tomorrow.io** - Weather forecasts (free tier)

### 📧 Communication
- **SendGrid** - 100 emails/day free forever
- **Mailgun** - 5K emails/month free
- **Twilio** - $15 credit for SMS/calls

### 🗺️ Location & Maps
- **IP API** - IP geolocation (free, no key)
- **Geocoding API** - Address to coordinates
- **REST Countries** - Country data (free, no key)

### 🎮 Fun & Testing
- **JSONPlaceholder** - Fake data for testing
- **PokeAPI** - Pokemon data
- **Dog API** - Random dog pictures
- **Cat Facts** - Random cat facts
- **XKCD** - Comic strips
- **Chuck Norris Jokes** - Random jokes

---

## 📚 Where to Find More APIs

### API Directories

1. **RapidAPI** - https://rapidapi.com/hub
   - 40,000+ APIs
   - Many have free tiers
   - Easy to browse by category

2. **Public APIs GitHub** - https://github.com/public-apis/public-apis
   - Huge list of free APIs
   - Categorized
   - Shows which need auth

3. **API List** - https://apilist.fun
   - Curated list of interesting APIs
   - Free and paid options

4. **Any API** - https://any-api.com
   - Directory of public APIs
   - Search by category

---

## 🎯 Recommended for ApiBridge Pro Demo

### Best for Demos (No Credit Card!)

1. **JSONPlaceholder** - Perfect for testing
   ```bash
   # No key needed!
   curl http://localhost:8000/proxy/jsonplaceholder/posts
   ```

2. **REST Countries** - Real useful data
   ```bash
   # No key needed!
   curl http://localhost:8000/proxy/restcountries/name/colombia
   ```

3. **CoinGecko** - Live crypto prices
   ```bash
   # No key needed!
   curl "http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd"
   ```

### Best for Production Use

1. **OpenWeatherMap** - Reliable weather (1K/day free)
2. **GitHub API** - If building dev tools (5K/hour free)
3. **SendGrid** - Email sending (100/day free forever)
4. **Stripe** - Payments (unlimited test mode)

---

## 🔧 Quick Setup Script

I'll create a connector for you right now with 3 free APIs:

```yaml
# Add these to your connectors.yaml

# 1. JSONPlaceholder (No key needed!)
jsonplaceholder:
  base_url: https://jsonplaceholder.typicode.com
  allow_paths:
    - "^/posts$"
    - "^/posts/.*$"
    - "^/users$"
    - "^/users/.*$"
    - "^/comments$"
  cache_ttl_seconds: 300
  rate_limit:
    capacity: 100
    refill_per_sec: 10

# 2. REST Countries (No key needed!)
restcountries:
  base_url: https://restcountries.com/v3.1
  allow_paths:
    - "^/name/.*$"
    - "^/alpha/.*$"
    - "^/all$"
  cache_ttl_seconds: 86400
  rate_limit:
    capacity: 100
    refill_per_sec: 10

# 3. CoinGecko (No key needed!)
coingecko:
  base_url: https://api.coingecko.com/api/v3
  allow_paths:
    - "^/simple/price$"
    - "^/coins/markets$"
    - "^/coins/list$"
  cache_ttl_seconds: 60
  rate_limit:
    capacity: 50
    refill_per_sec: 1

# 4. Dog API (No key needed!)
dog_api:
  base_url: https://dog.ceo/api
  allow_paths:
    - "^/breeds/image/random$"
    - "^/breeds/list/all$"
    - "^/breed/.*/images$"
  cache_ttl_seconds: 300
  rate_limit:
    capacity: 100
    refill_per_sec: 10
```

---

## 🚀 Test These APIs Right Now!

```bash
# 1. Start ApiBridge Pro
uvicorn app.main:app --reload --port 8000

# 2. Test JSONPlaceholder
curl http://localhost:8000/proxy/jsonplaceholder/posts | jq

# 3. Test REST Countries  
curl http://localhost:8000/proxy/restcountries/name/colombia | jq

# 4. Test CoinGecko
curl "http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin,ethereum&vs_currencies=usd" | jq

# 5. Test Dog API
curl http://localhost:8000/proxy/dog_api/breeds/image/random | jq
```

---

## 💡 Pro Tips

### Testing APIs Without Keys

Use these for development:
- JSONPlaceholder (posts, users, todos)
- REST Countries (country data)
- PokeAPI (pokemon data)
- Dog/Cat APIs (random images)

### Getting API Keys

Most APIs offer free tiers:
1. **Email signup** - Usually instant
2. **Verify email** - Check spam folder
3. **Dashboard** - Find API keys section
4. **Copy key** - Usually starts with specific prefix
5. **Set environment variable** - Don't hardcode!

### Free Tier Limits

Watch for:
- **Rate limits** - Requests per minute/hour/day
- **Monthly quotas** - Total requests per month
- **Feature limits** - Some features need paid tier
- **Credit card** - Some "free" tiers require card

### Best Practices

- ✅ Use environment variables for keys
- ✅ Never commit keys to git
- ✅ Set budget limits in ApiBridge
- ✅ Cache aggressively
- ✅ Respect rate limits

---

## 📋 Complete API Connector Template

Use this template for ANY API:

```yaml
my_new_api:
  base_url: https://api.example.com/v1
  
  # Auth (choose one)
  auth:
    type: bearer              # For: Authorization: Bearer TOKEN
    token: ${API_KEY}
    
    # OR
    # type: api_key_header
    # header_name: X-API-Key
    # token: ${API_KEY}
    
    # OR  
    # type: api_key_query
    # name: api_key
    # value: ${API_KEY}
    
    # OR
    # type: basic
    # username: ${API_USER}
    # password: ${API_PASS}
  
  # Security - only allow specific paths
  allow_paths:
    - "^/endpoint1$"
    - "^/endpoint2/.*$"
  
  # Performance
  rate_limit:
    capacity: 100        # Max requests
    refill_per_sec: 10   # Refill rate
  
  cache_ttl_seconds: 60  # Cache responses
  
  strategy:
    timeout_ms: 5000     # 5 second timeout
    retries: 2           # Retry twice on failure
  
  # Cost control
  budget:
    monthly_usd_max: 10
    on_exceed: block
  
  cost_per_call_usd: 0.001
  
  # Optional: PII protection
  pii_protection:
    enabled: false
    auto_scan: true
  
  # Optional: Transform responses
  # transforms:
  #   response:
  #     jmes: '{id: id, name: name}'
```

---

## 🎁 Ready-to-Use Connectors

I've already created these for you in `examples/connectors/`:

✅ `openai.yaml` - OpenAI GPT models  
✅ `stripe.yaml` - Stripe payments  
✅ `twilio.yaml` - SMS & voice  
✅ `sendgrid.yaml` - Email sending  
✅ `anthropic.yaml` - Claude AI  

Just copy them to your main `connectors.yaml`!

---

## 🚀 Next Steps

1. **Choose an API** from the list above
2. **Get API key** (or use no-key APIs)
3. **Add to** `connectors.yaml`
4. **Set environment variable** (if needed)
5. **Restart** ApiBridge Pro
6. **Test** with curl!

---

## 📞 Need Help?

- 📖 See example connectors in `examples/connectors/`
- 📚 Read `TUTORIAL.md` for step-by-step guide
- 🐛 Open issue on GitHub if stuck
- 💬 Check documentation for auth types

---

**Start with JSONPlaceholder - it works instantly with no setup!** 🎉

