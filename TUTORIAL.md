# 🎓 ApiBridge Pro - Interactive Tutorial

**Learn by doing!** This hands-on tutorial takes you from zero to hero in 30 minutes.

---

## 🎯 What You'll Build

By the end of this tutorial, you'll have:

1. ✅ A working API gateway
2. ✅ Multi-provider weather API with failover
3. ✅ Cost tracking and budget controls
4. ✅ Real-time monitoring dashboard
5. ✅ Your own custom API connector

**Time required:** 30 minutes  
**Difficulty:** Beginner-friendly  
**Prerequisites:** Python 3.11+ installed

---

## 📝 Tutorial Overview

```
Part 1: Setup (5 min)           → Get ApiBridge running
Part 2: First API (10 min)      → Add weather API
Part 3: Add Failover (5 min)    → Multi-provider setup
Part 4: Budget Control (5 min)  → Track costs
Part 5: Your Own API (5 min)    → Custom connector
```

---

## Part 1: Setup & Installation (5 minutes)

### Step 1.1: Install Dependencies

```bash
# Navigate to project folder
cd ApiBridgePro

# Install
pip install -r requirements.txt
```

**✅ Checkpoint:** You should see "Successfully installed..." messages.

---

### Step 1.2: Start the Server

```bash
# Set dummy API keys (for now)
export OPENWEATHER_KEY=dummy
export WEATHERAPI_KEY=dummy
export GITHUB_TOKEN=dummy

# Start server
uvicorn app.main:app --reload --port 8000
```

**✅ Checkpoint:** You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### Step 1.3: Verify It's Working

Open a **new terminal** and run:

```bash
curl http://127.0.0.1:8000/health
```

**✅ Expected output:**
```json
{
  "ok": true,
  "mode": "live",
  "connectors": ["weather_unified", "github", "slack"]
}
```

**🎉 Success!** Your API gateway is running!

---

## Part 2: Your First API Integration (10 minutes)

Let's integrate a **free, no-auth-needed API** - the Chuck Norris Jokes API!

### Step 2.1: Add the Connector

1. Open `connectors.yaml` in your editor
2. Add this at the **bottom** of the file:

```yaml
# Chuck Norris Jokes API
jokes:
  base_url: https://api.chucknorris.io
  allow_paths:
    - "^/jokes/random$"
    - "^/jokes/categories$"
  cache_ttl_seconds: 300  # Cache jokes for 5 minutes
  rate_limit:
    capacity: 100
    refill_per_sec: 10
```

3. **Save the file**

**✅ Checkpoint:** The server should auto-reload (you'll see messages in the terminal).

---

### Step 2.2: Test Your New Connector

```bash
curl http://127.0.0.1:8000/proxy/jokes/jokes/random
```

**✅ Expected output:**
```json
{
  "icon_url": "https://...",
  "id": "...",
  "url": "https://...",
  "value": "Chuck Norris can divide by zero."
}
```

**🎉 Congratulations!** You just integrated your first API!

---

### Step 2.3: Explore the Dashboard

Open your browser:
```
http://127.0.0.1:8000/admin
```

You should see:
- ✅ "jokes" connector listed
- ✅ System overview showing 4 connectors
- ✅ Cache entries (if you made multiple requests)

**Try this:**
1. Make 5 requests to the jokes API
2. Refresh the dashboard
3. See the cache statistics update!

---

### Step 2.4: Test Caching

Let's prove caching works:

```bash
# First request (slow - hits the API)
time curl http://127.0.0.1:8000/proxy/jokes/jokes/random

# Second request (fast - served from cache!)
time curl http://127.0.0.1:8000/proxy/jokes/jokes/random
```

**✅ Expected:**
- First request: ~200-500ms
- Second request: ~2-5ms (100x faster!)

**Why?** The response is cached for 5 minutes!

---

## Part 3: Add Multi-Provider Failover (5 minutes)

Let's make your API super reliable with automatic failover!

### Step 3.1: Get Free API Keys

For this demo, we'll use free weather APIs:

1. **OpenWeather** - Sign up at https://openweathermap.org/api
   - Free tier: 1000 calls/day
   - Get your API key

2. **WeatherAPI** - Sign up at https://www.weatherapi.com/
   - Free tier: 1M calls/month
   - Get your API key

---

### Step 3.2: Set Your Real API Keys

```bash
# Set your real API keys
export OPENWEATHER_KEY="your_openweather_key_here"
export WEATHERAPI_KEY="your_weatherapi_key_here"

# Restart the server (CTRL+C then restart)
uvicorn app.main:app --reload --port 8000
```

---

### Step 3.3: Test Weather API

The `weather_unified` connector is already configured! Let's test it:

```bash
# Try different cities
curl "http://127.0.0.1:8000/proxy/weather_unified/weather?q=London"
curl "http://127.0.0.1:8000/proxy/weather_unified/weather?q=Tokyo"
curl "http://127.0.0.1:8000/proxy/weather_unified/weather?q=NewYork"
```

**✅ Expected output:**
```json
{
  "temp_c": 15.2,
  "humidity": 72,
  "provider": "openweather"
}
```

Notice the `"provider"` field - that tells you which API was used!

---

### Step 3.4: Watch the Dashboard

Open the dashboard:
```
http://127.0.0.1:8000/admin
```

You'll see:
- **Provider Health** section showing both providers
- **Which provider is faster** (lower latency)
- **Cache hit rates**

**Try this:**
1. Make 10 requests to different cities
2. Watch the dashboard update
3. See which provider is being used more

---

### Step 3.5: Test Failover (Advanced)

Want to see automatic failover in action?

**Simulate a provider failure:**

1. Edit `connectors.yaml`
2. Temporarily break the OpenWeather URL:
   ```yaml
   weather_unified:
     providers:
       - name: openweather
         base_url: https://BROKEN.openweathermap.org  # Added BROKEN!
   ```
3. Save (server auto-reloads)
4. Make a request:
   ```bash
   curl "http://127.0.0.1:8000/proxy/weather_unified/weather?q=Paris"
   ```

**✅ It still works!** ApiBridge automatically failed over to WeatherAPI!

**Check the logs** - you'll see it tried OpenWeather, failed, then succeeded with WeatherAPI.

**Don't forget to fix the URL:**
```yaml
base_url: https://api.openweathermap.org/data/2.5  # Fixed!
```

---

## Part 4: Add Budget Controls (5 minutes)

Let's make sure you never get a surprise API bill!

### Step 4.1: Understand Current Costs

The `weather_unified` connector already has budget tracking:

```yaml
budget:
  monthly_usd_max: 25  # Never spend more than $25/month
  on_exceed: downgrade_provider  # Use cheaper provider when needed
cost_per_call_usd: 0.0002  # Track $0.0002 per call
```

---

### Step 4.2: Check Budget Dashboard

Open the admin dashboard:
```
http://127.0.0.1:8000/admin
```

Look for the **Budget Overview** section:
- Shows current spending
- Shows monthly limit
- Visual progress bar

---

### Step 4.3: Add Budget to Your Jokes API

Let's add budget tracking to our jokes connector:

1. Edit `connectors.yaml`
2. Update the `jokes` connector:

```yaml
jokes:
  base_url: https://api.chucknorris.io
  allow_paths:
    - "^/jokes/random$"
    - "^/jokes/categories$"
  cache_ttl_seconds: 300
  rate_limit:
    capacity: 100
    refill_per_sec: 10
  
  # ADD THESE LINES:
  budget:
    monthly_usd_max: 10  # Limit to $10/month
    on_exceed: block     # Stop when limit hit
  cost_per_call_usd: 0.0001  # Assume $0.0001 per joke
```

3. Save the file

---

### Step 4.4: Test Budget Tracking

```bash
# Make a bunch of requests
for i in {1..100}; do
  curl -s http://127.0.0.1:8000/proxy/jokes/jokes/random > /dev/null
  echo "Request $i"
done
```

**Check the dashboard:**
- Budget Overview shows spending for "jokes"
- See the progress bar increase!

---

### Step 4.5: Simulate Budget Exceeded

Want to see what happens when you hit the limit?

1. Lower the budget temporarily:
   ```yaml
   budget:
     monthly_usd_max: 0.001  # Very low limit!
   ```

2. Make requests:
   ```bash
   curl "http://127.0.0.1:8000/proxy/jokes/jokes/random"
   ```

**After a few requests, you'll get:**
```json
{
  "error": "budget_exceeded"
}
```

**🎉 Budget protection working!** You'll never overspend!

**Don't forget to change it back:**
```yaml
monthly_usd_max: 10  # Back to normal
```

---

## Part 5: Create Your Own Custom Connector (5 minutes)

Now let's add a completely custom API of your choice!

### Step 5.1: Choose an API

Pick any free API you like. Here are some ideas:

- **Random User API** - https://randomuser.me/api/
- **Dog API** - https://dog.ceo/api/breeds/image/random
- **Cat Facts** - https://catfact.ninja/fact
- **Bored API** - https://www.boredapi.com/api/activity
- **Your own API!**

Let's use the **Dog API** as an example.

---

### Step 5.2: Add Your Connector

1. Open `connectors.yaml`
2. Add at the bottom:

```yaml
# Random Dog Pictures
dogs:
  base_url: https://dog.ceo/api
  allow_paths:
    - "^/breeds/.*$"
    - "^/breed/.*$"
  cache_ttl_seconds: 600  # Cache dog pics for 10 minutes
  rate_limit:
    capacity: 50
    refill_per_sec: 5
  budget:
    monthly_usd_max: 5
    on_exceed: block
  cost_per_call_usd: 0.0  # Free API!
```

3. Save

---

### Step 5.3: Test Your Connector

```bash
# Get a random dog picture
curl http://127.0.0.1:8000/proxy/dogs/breeds/image/random

# List all breeds
curl http://127.0.0.1:8000/proxy/dogs/breeds/list/all
```

**✅ Expected:**
```json
{
  "message": "https://images.dog.ceo/breeds/...",
  "status": "success"
}
```

**🎉 You created a custom connector in 5 minutes!**

---

### Step 5.4: Verify in Dashboard

Check the admin dashboard:
```
http://127.0.0.1:8000/admin
```

You should see:
- ✅ "dogs" connector listed
- ✅ Request counts
- ✅ Cache statistics
- ✅ Budget tracking (showing $0 since it's free!)

---

## 🎓 Bonus Challenges

### Challenge 1: Add Response Transformation

Transform the dog API response to a simpler format:

```yaml
dogs:
  # ... existing config ...
  transforms:
    response:
      jmes: '{url: message, status: status}'
```

**Result:** Instead of `{"message": "...", "status": "success"}`, you get `{"url": "...", "status": "success"}`

---

### Challenge 2: Add Multiple Providers

Find two APIs that do the same thing and set up failover:

```yaml
images:
  providers:
    - name: unsplash
      base_url: https://api.unsplash.com
      auth: {type: api_key_query, name: client_id, value: ${UNSPLASH_KEY}}
    - name: pexels
      base_url: https://api.pexels.com/v1
      auth: {type: api_key_header, name: Authorization, value: ${PEXELS_KEY}}
  strategy: {policy: fastest_healthy_then_cheapest}
```

---

### Challenge 3: Add PII Protection

If your API returns user data, protect it:

```yaml
users:
  base_url: https://randomuser.me/api
  pii_protection:
    enabled: true
    auto_scan: true
    action: encrypt
```

---

## 📊 Review: What You Learned

✅ **Installation** - Set up ApiBridge Pro  
✅ **Configuration** - Edit `connectors.yaml`  
✅ **Testing** - Use curl to test APIs  
✅ **Monitoring** - Use the admin dashboard  
✅ **Caching** - Save money with response caching  
✅ **Failover** - Multi-provider automatic failover  
✅ **Budget Control** - Prevent surprise bills  
✅ **Custom Connectors** - Add any API you want  

---

## 🎯 Next Steps

### Continue Learning:

1. **Read COMPARISON.md** - Understand benefits vs plain FastAPI
2. **Check BUSINESS_VALUE.md** - See ROI calculations
3. **Review IMPROVEMENTS.md** - Learn about advanced features

### Build Something Real:

1. **Add your production APIs** to `connectors.yaml`
2. **Set up monitoring** with Prometheus
3. **Deploy to production** with Docker
4. **Share your success** - Tweet about it!

---

### Try Advanced Features:

1. **OAuth2 Auto-Refresh** - See `connectors_advanced.yaml`
2. **Record/Replay Mode** - Test without hitting real APIs
3. **OpenTelemetry Tracing** - Distributed tracing
4. **Prometheus Metrics** - Detailed monitoring

---

## 📚 Quick Command Reference

```bash
# Start server
uvicorn app.main:app --reload --port 8000

# Test health
curl http://127.0.0.1:8000/health

# View dashboard
open http://127.0.0.1:8000/admin

# View API docs
open http://127.0.0.1:8000/docs

# Test connector
curl http://127.0.0.1:8000/proxy/CONNECTOR_NAME/PATH

# Run tests
make test

# Check quality
make ci
```

---

## ❓ Stuck? Check Troubleshooting

See **GETTING_STARTED.md** section "Troubleshooting" for common issues.

---

## 🎉 Congratulations!

**You've completed the ApiBridge Pro tutorial!**

You now know how to:
- ✅ Set up an API gateway in minutes
- ✅ Add any API with simple YAML
- ✅ Configure automatic failover
- ✅ Track costs and set budgets
- ✅ Monitor everything in real-time

**Ready to build something amazing? Go for it! 🚀**

---

**Found this helpful? ⭐ Star the project and share with friends!**

**Questions? Check the docs or open an issue on GitHub.**

