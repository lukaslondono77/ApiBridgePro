# 🚀 What Can You Build with ApiBridge Pro APIs?

Now that you have 8 APIs connected, here are **real projects** you can build!

---

## 💰 Project 1: Live Crypto Price Dashboard

**What:** Real-time cryptocurrency price tracker

**APIs Used:**
- CoinGecko (Bitcoin, Ethereum, prices)

**What You Get:**
```json
{
  "bitcoin": {"usd": 110791},
  "ethereum": {"usd": 4123}
}
```

**Frontend Example (HTML/JS):**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Crypto Tracker</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; }
        .crypto { padding: 20px; margin: 10px; background: #f0f0f0; border-radius: 8px; }
        .price { font-size: 24px; color: green; font-weight: bold; }
    </style>
</head>
<body>
    <h1>💰 Live Crypto Prices</h1>
    <div id="cryptos"></div>

    <script>
        async function fetchPrices() {
            const response = await fetch('http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin,ethereum&vs_currencies=usd');
            const data = await response.json();
            
            document.getElementById('cryptos').innerHTML = `
                <div class="crypto">
                    <h2>₿ Bitcoin</h2>
                    <div class="price">$${data.bitcoin.usd.toLocaleString()}</div>
                </div>
                <div class="crypto">
                    <h2>Ξ Ethereum</h2>
                    <div class="price">$${data.ethereum.usd.toLocaleString()}</div>
                </div>
            `;
        }
        
        fetchPrices();
        setInterval(fetchPrices, 60000); // Update every minute
    </script>
</body>
</html>
```

**Save as:** `crypto-tracker.html` and open in browser!

**ApiBridge provides:**
- ✅ Caching (60 second - reduces API calls)
- ✅ Rate limiting (protects from abuse)
- ✅ Error handling
- ✅ Monitoring

---

## 🌍 Project 2: World Country Explorer

**What:** Search and explore country information

**APIs Used:**
- REST Countries (195 countries!)

**What You Get:**
```json
{
  "name": "Colombia",
  "capital": "Bogotá",
  "population": 50882884,
  "currencies": {"COP": {"symbol": "$"}},
  "flag": "🇨🇴"
}
```

**Frontend Example:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Country Explorer</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; }
        input { width: 100%; padding: 10px; font-size: 16px; }
        .country { padding: 20px; margin: 20px 0; background: #f5f5f5; border-radius: 8px; }
        .flag { font-size: 64px; }
    </style>
</head>
<body>
    <h1>🌍 World Country Explorer</h1>
    <input type="text" id="search" placeholder="Search for a country (e.g., Colombia, Japan, France)">
    <div id="result"></div>

    <script>
        document.getElementById('search').addEventListener('input', async (e) => {
            const country = e.target.value;
            if (country.length < 3) return;
            
            try {
                const response = await fetch(`http://localhost:8000/proxy/restcountries/name/${country}`);
                const data = await response.json();
                const info = data[0];
                
                document.getElementById('result').innerHTML = `
                    <div class="country">
                        <div class="flag">${info.flag}</div>
                        <h2>${info.name.common}</h2>
                        <p><strong>Official Name:</strong> ${info.name.official}</p>
                        <p><strong>Capital:</strong> ${info.capital ? info.capital[0] : 'N/A'}</p>
                        <p><strong>Population:</strong> ${info.population.toLocaleString()}</p>
                        <p><strong>Region:</strong> ${info.region}</p>
                        <p><strong>Currency:</strong> ${Object.values(info.currencies || {})[0]?.name || 'N/A'}</p>
                    </div>
                `;
            } catch (error) {
                document.getElementById('result').innerHTML = '<p>Country not found</p>';
            }
        });
    </script>
</body>
</html>
```

**Save as:** `country-explorer.html`

---

## 🐕 Project 3: Random Content Generator

**What:** Fun app that shows random dogs, cats, facts

**APIs Used:**
- Dog API (random dogs)
- Cat Facts (random facts)

**Frontend Example:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Random Fun!</title>
    <style>
        body { font-family: Arial; text-align: center; max-width: 600px; margin: 50px auto; }
        button { padding: 15px 30px; font-size: 18px; margin: 10px; cursor: pointer; }
        img { max-width: 100%; border-radius: 8px; margin: 20px 0; }
        .fact { padding: 20px; background: #f0f0f0; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>🎲 Random Fun Generator</h1>
    
    <button onclick="getRandomDog()">🐕 Random Dog</button>
    <button onclick="getRandomFact()">🐱 Cat Fact</button>
    
    <div id="content"></div>

    <script>
        async function getRandomDog() {
            const response = await fetch('http://localhost:8000/proxy/dog_api/breeds/image/random');
            const data = await response.json();
            document.getElementById('content').innerHTML = `
                <h2>🐕 Here's a Random Dog!</h2>
                <img src="${data.message}" alt="Random dog">
            `;
        }
        
        async function getRandomFact() {
            const response = await fetch('http://localhost:8000/proxy/catfacts/fact');
            const data = await response.json();
            document.getElementById('content').innerHTML = `
                <h2>🐱 Random Cat Fact</h2>
                <div class="fact">${data.fact}</div>
            `;
        }
    </script>
</body>
</html>
```

**Save as:** `random-fun.html`

---

## 📝 Project 4: Blog Reader App

**What:** Browse and read fake blog posts (great for testing!)

**APIs Used:**
- JSONPlaceholder (posts, users, comments)

**Frontend Example:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog Reader</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; }
        .post { padding: 20px; margin: 20px 0; background: #fff; border: 1px solid #ddd; border-radius: 8px; }
        .post h3 { color: #333; margin-top: 0; }
        .post p { color: #666; line-height: 1.6; }
        .author { color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <h1>📝 Blog Posts</h1>
    <div id="posts"></div>

    <script>
        async function loadPosts() {
            // Get posts
            const postsRes = await fetch('http://localhost:8000/proxy/jsonplaceholder/posts');
            const posts = await postsRes.json();
            
            // Get users
            const usersRes = await fetch('http://localhost:8000/proxy/jsonplaceholder/users');
            const users = await usersRes.json();
            
            // Combine them
            const postsHTML = posts.slice(0, 10).map(post => {
                const user = users.find(u => u.id === post.userId);
                return `
                    <div class="post">
                        <h3>${post.title}</h3>
                        <p>${post.body}</p>
                        <div class="author">By ${user?.name || 'Unknown'}</div>
                    </div>
                `;
            }).join('');
            
            document.getElementById('posts').innerHTML = postsHTML;
        }
        
        loadPosts();
    </script>
</body>
</html>
```

**Save as:** `blog-reader.html`

---

## 🎯 Real-World Use Cases

### 1. **Financial Dashboard** 💹
Combine multiple APIs:
- CoinGecko → Crypto prices
- (Add stock API) → Stock prices
- (Add forex API) → Currency rates

**Build:** Investment portfolio tracker

### 2. **Travel Planning App** ✈️
- REST Countries → Destination info
- (Add weather API) → Weather forecasts
- (Add exchange rate API) → Currency conversion

**Build:** Travel planner with all info in one place

### 3. **Developer Tool** 👨‍💻
- GitHub → Repo stats
- JSONPlaceholder → Test data
- (Add more dev APIs) → Complete toolkit

**Build:** Developer dashboard

### 4. **Fun Content App** 🎮
- Dog API → Random dogs
- Cat Facts → Cat facts
- (Add joke API) → Random jokes

**Build:** Entertainment website

---

## 🔧 How to Use in Your App

### React Example:

```javascript
import React, { useState, useEffect } from 'react';

function BitcoinPrice() {
  const [price, setPrice] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd')
      .then(res => res.json())
      .then(data => setPrice(data.bitcoin.usd));
  }, []);

  return <h1>Bitcoin: ${price?.toLocaleString()}</h1>;
}
```

### Vue.js Example:

```javascript
<template>
  <div>
    <h1>Country: {{ country }}</h1>
    <p>Population: {{ population }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      country: '',
      population: 0
    }
  },
  async mounted() {
    const res = await fetch('http://localhost:8000/proxy/restcountries/name/colombia');
    const data = await res.json();
    this.country = data[0].name.common;
    this.population = data[0].population;
  }
}
</script>
```

### Python Example:

```python
import requests

# Get Bitcoin price
response = requests.get('http://localhost:8000/proxy/coingecko/simple/price', 
    params={'ids': 'bitcoin', 'vs_currencies': 'usd'})
bitcoin_price = response.json()['bitcoin']['usd']
print(f"Bitcoin: ${bitcoin_price:,}")

# Get country data
response = requests.get('http://localhost:8000/proxy/restcountries/name/colombia')
country = response.json()[0]
print(f"{country['name']['common']} - Population: {country['population']:,}")
```

---

## 🎨 What ApiBridge Pro Does For You

When you use these APIs through ApiBridge:

### 1. **Caching** ⚡
```javascript
// First request: 200ms (fetches from API)
fetch('/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd')

// Second request (within 60s): 2ms (cached!)
fetch('/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd')
```

### 2. **Rate Limiting** 🛡️
```javascript
// Make 100 requests
for (let i = 0; i < 100; i++) {
  fetch('/proxy/catfacts/fact');
}
// ApiBridge automatically limits to protect the API
// Returns 429 when limit reached
```

### 3. **Monitoring** 📊
- Dashboard shows request counts
- See cache hit rates
- Monitor budget usage
- Track provider health

### 4. **Error Handling** 🔧
```javascript
// API is down? ApiBridge handles it gracefully
fetch('/proxy/someapi/endpoint')
  .then(res => {
    if (!res.ok) {
      // ApiBridge returns clean error
      console.log('API unavailable, try again later');
    }
  });
```

---

## 🎯 Quick Demos You Can Try NOW

### Demo 1: Test Caching

```bash
# First request (slow - fetches from API)
time curl -s http://localhost:8000/proxy/jsonplaceholder/posts > /dev/null

# Second request (FAST - cached!)
time curl -s http://localhost:8000/proxy/jsonplaceholder/posts > /dev/null

# Check dashboard - cache stats increase!
```

### Demo 2: Test Rate Limiting

```bash
# Rapid-fire requests
for i in {1..50}; do
  curl -s http://localhost:8000/proxy/catfacts/fact | jq -r .fact
  echo ""
done

# Some will return 429 (rate limited)
# Check dashboard - rate limit stats appear!
```

### Demo 3: Build a Multi-API Page

```html
<!DOCTYPE html>
<html>
<head>
    <title>API Showcase</title>
    <style>
        body { font-family: Arial; max-width: 1000px; margin: 50px auto; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { padding: 20px; background: #f5f5f5; border-radius: 8px; }
        button { padding: 10px 20px; cursor: pointer; background: #667eea; color: white; border: none; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>🌟 ApiBridge Pro - Live Demo</h1>
    
    <div class="grid">
        <!-- Bitcoin Price -->
        <div class="card">
            <h2>💰 Bitcoin Price</h2>
            <div id="bitcoin">Loading...</div>
            <button onclick="loadBitcoin()">Refresh</button>
        </div>
        
        <!-- Random Dog -->
        <div class="card">
            <h2>🐕 Random Dog</h2>
            <div id="dog">Click button to load</div>
            <button onclick="loadDog()">Get Dog</button>
        </div>
        
        <!-- Cat Fact -->
        <div class="card">
            <h2>🐱 Cat Fact</h2>
            <div id="catfact">Click button to load</div>
            <button onclick="loadCatFact()">Get Fact</button>
        </div>
        
        <!-- Country Info -->
        <div class="card">
            <h2>🌍 Country Info</h2>
            <input type="text" id="countryName" placeholder="Enter country name">
            <button onclick="loadCountry()">Search</button>
            <div id="country"></div>
        </div>
    </div>

    <script>
        async function loadBitcoin() {
            const res = await fetch('http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd');
            const data = await res.json();
            document.getElementById('bitcoin').innerHTML = 
                `<h1 style="color: green;">$${data.bitcoin.usd.toLocaleString()}</h1>`;
        }
        
        async function loadDog() {
            const res = await fetch('http://localhost:8000/proxy/dog_api/breeds/image/random');
            const data = await res.json();
            document.getElementById('dog').innerHTML = 
                `<img src="${data.message}" style="max-width: 100%; border-radius: 8px;">`;
        }
        
        async function loadCatFact() {
            const res = await fetch('http://localhost:8000/proxy/catfacts/fact');
            const data = await res.json();
            document.getElementById('catfact').innerHTML = 
                `<p style="font-style: italic;">"${data.fact}"</p>`;
        }
        
        async function loadCountry() {
            const name = document.getElementById('countryName').value;
            const res = await fetch(`http://localhost:8000/proxy/restcountries/name/${name}`);
            const data = await res.json();
            const country = data[0];
            
            document.getElementById('country').innerHTML = `
                <h3>${country.flag} ${country.name.common}</h3>
                <p><strong>Population:</strong> ${country.population.toLocaleString()}</p>
                <p><strong>Capital:</strong> ${country.capital?.[0] || 'N/A'}</p>
                <p><strong>Region:</strong> ${country.region}</p>
            `;
        }
        
        // Auto-load Bitcoin on page load
        loadBitcoin();
        setInterval(loadBitcoin, 60000); // Update every minute
    </script>
</body>
</html>
```

**Save as:** `api-showcase.html` and open in browser!

---

## 📱 Project 5: Mobile App Backend

Use ApiBridge as your backend for a mobile app:

**iOS (Swift):**
```swift
func getBitcoinPrice() {
    let url = URL(string: "http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd")!
    
    URLSession.shared.dataTask(with: url) { data, response, error in
        if let data = data {
            let price = try? JSONDecoder().decode(BitcoinPrice.self, from: data)
            print("Bitcoin: $\(price?.bitcoin.usd ?? 0)")
        }
    }.resume()
}
```

**Android (Kotlin):**
```kotlin
fun getBitcoinPrice() {
    val url = "http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd"
    
    val request = Request.Builder().url(url).build()
    client.newCall(request).enqueue(object : Callback {
        override fun onResponse(call: Call, response: Response) {
            val price = response.body?.string()
            println("Bitcoin price: $price")
        }
    })
}
```

---

## 🎓 Learning Projects (Great for Portfolios!)

### Beginner: Todo App
- JSONPlaceholder → Fake todos
- Build CRUD operations
- Practice API integration

### Intermediate: Weather Dashboard
- Multiple weather APIs
- Show multi-provider failover
- Cache for performance

### Advanced: Trading Bot
- CoinGecko → Prices
- Track price changes
- Trigger alerts
- Log to database

---

## 💼 Business Use Cases

### For Startups:

**1. SaaS Dashboard**
```
ApiBridge connects to:
├─ Stripe (payments)
├─ SendGrid (emails)
├─ Twilio (SMS)
└─ Analytics APIs

One gateway for all your integrations!
```

**Benefits:**
- Save $100K/year on API costs
- 99.99% uptime (failover)
- Instant integration (YAML config)

### For E-commerce:

**2. Product Enrichment**
```
ApiBridge connects to:
├─ Product APIs (inventory)
├─ Payment APIs (checkout)
├─ Shipping APIs (tracking)
└─ Review APIs (ratings)

Unified schema, one endpoint!
```

### For FinTech:

**3. Financial Aggregation**
```
ApiBridge connects to:
├─ Stock APIs (real-time prices)
├─ Crypto APIs (market data)
├─ Forex APIs (exchange rates)
└─ Banking APIs (transactions)

Budget controls built-in!
```

---

## 🚀 Advanced Features You Can Use

### 1. Multi-Provider Routing

Already set up for weather:
```yaml
weather_unified:
  providers:
    - openweather  # Primary
    - weatherapi   # Fallback
```

**Benefit:** If one fails, automatically uses the other!

### 2. Response Transformation

Unify different API formats:
```yaml
transforms:
  response:
    jmes: '{name: name, price: price_usd}'
```

**Benefit:** All providers return same format!

### 3. Budget Controls

Prevent surprise bills:
```yaml
budget:
  monthly_usd_max: 100
  on_exceed: block
```

**Benefit:** Never overspend on APIs!

### 4. PII Protection

Auto-redact sensitive data:
```yaml
pii_protection:
  enabled: true
  auto_scan: true
```

**Benefit:** GDPR compliant automatically!

---

## 📊 Monitor Everything

### Check Dashboard:
```
http://127.0.0.1:8000/admin
```

**You'll see:**
- Total requests per connector
- Cache hit rates (saves money!)
- Rate limit status
- Budget tracking
- Provider health

### Check Metrics:
```
http://127.0.0.1:8000/metrics
```

**Prometheus format:**
- Request counts
- Latency histograms
- Error rates
- Cache statistics

---

## 🎯 What To Do Right Now

### Step 1: Test All APIs (2 minutes)

```bash
# Test each one
curl http://localhost:8000/proxy/jsonplaceholder/posts | jq '.[0]'
curl http://localhost:8000/proxy/restcountries/name/usa | jq '.[0].name'
curl "http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd" | jq
curl http://localhost:8000/proxy/dog_api/breeds/image/random | jq
curl http://localhost:8000/proxy/catfacts/fact | jq
```

### Step 2: Watch Dashboard (1 minute)

```bash
# Open in browser
open http://127.0.0.1:8000/admin

# Make requests (run commands above)
# See stats update in real-time!
```

### Step 3: Build Something (30 minutes)

Pick one of the HTML examples above:
- `crypto-tracker.html` (easiest)
- `country-explorer.html` (useful)
- `random-fun.html` (most fun!)
- `api-showcase.html` (shows everything!)

Save the file and open in browser!

---

## 🎁 Bonus: Add More Free APIs

Want more? Add these (NO keys needed):

```yaml
# Add to connectors.yaml

jokes:
  base_url: https://official-joke-api.appspot.com
  allow_paths:
    - "^/random_joke$"
    - "^/jokes/programming/random$"

ipapi:
  base_url: https://ipapi.co
  allow_paths:
    - "^/json$"
    - "^/.*/json$"

chucknorris:
  base_url: https://api.chucknorris.io
  allow_paths:
    - "^/jokes/random$"
    - "^/jokes/categories$"
```

---

## 💡 Pro Tips

### Combine Multiple APIs

```javascript
// Get Bitcoin price AND country data in parallel
const [bitcoin, country] = await Promise.all([
  fetch('http://localhost:8000/proxy/coingecko/simple/price?ids=bitcoin&vs_currencies=usd'),
  fetch('http://localhost:8000/proxy/restcountries/name/colombia')
]);

// ApiBridge handles both efficiently!
```

### Use the SDK

```python
from apibridge_client import ApiBridgeClient

async with ApiBridgeClient("http://localhost:8000") as client:
    # Get Bitcoin price
    bitcoin = await client.proxy("coingecko", "/simple/price", 
        params={"ids": "bitcoin", "vs_currencies": "usd"})
    
    # Get country data
    country = await client.proxy("restcountries", "/name/colombia")
```

### Monitor Performance

```bash
# Check metrics to see caching benefits
curl http://localhost:8000/metrics | grep cache

# You'll see:
# apibridge_cache_hits_total{connector="coingecko"} 45
# apibridge_cache_misses_total{connector="coingecko"} 3
# 93% cache hit rate = 93% cost savings!
```

---

## 🎉 You Can Now:

✅ **Get live crypto prices** → Build crypto tracker  
✅ **Get country data** → Build travel app  
✅ **Get random content** → Build fun app  
✅ **Get test data** → Build/test any app  
✅ **Monitor everything** → See it all in dashboard  
✅ **Control costs** → Budget limits built-in  
✅ **Scale globally** → Multi-provider routing  

---

## 🚀 Start Building!

**Pick a project above and start coding!**

All APIs are:
- ✅ Connected
- ✅ Working
- ✅ Free
- ✅ Cached
- ✅ Monitored
- ✅ Ready to use!

**Dashboard:** http://127.0.0.1:8000/admin  
**API Docs:** http://127.0.0.1:8000/docs  

**Let's build something amazing!** 💻✨

