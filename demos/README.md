# ApiBridge Pro - Demo Apps

Ready-to-use HTML demos showing ApiBridge Pro in action!

---

## 🚀 Quick Start

**Prerequisites:**
1. ApiBridge Pro running: `uvicorn app.main:app --reload --port 8000`
2. Free APIs connected (already done! ✅)

**Run Demos:**
```bash
# Open any demo in your browser
open demos/bitcoin-tracker.html
open demos/country-explorer.html
open demos/api-dashboard.html
```

Or just **double-click** the HTML files!

---

## 📁 Available Demos

### 1. bitcoin-tracker.html 💰

**What it does:**
- Shows live Bitcoin price (updated every 60 seconds)
- Displays request count and cache hits
- Beautiful gradient design

**APIs Used:**
- CoinGecko (crypto prices)

**Features:**
- Auto-refresh every minute
- Shows latency (cache = <100ms!)
- Request counter

**Try it:**
```bash
open demos/bitcoin-tracker.html
```

---

### 2. country-explorer.html 🌍

**What it does:**
- Search any country in the world
- Shows flag, population, capital, currency, etc.
- Real-time search as you type

**APIs Used:**
- REST Countries (195 countries)

**Features:**
- Type-ahead search
- Beautiful flag display
- Comprehensive country data

**Try it:**
```bash
open demos/country-explorer.html
```

**Try searching:**
- Colombia 🇨🇴
- Japan 🇯🇵
- France 🇫🇷
- USA 🇺🇸

---

### 3. api-dashboard.html 🎯

**What it does:**
- Multi-API dashboard showing all capabilities
- Bitcoin, Ethereum, dogs, cats, countries, blog posts
- Beautiful dark mode design

**APIs Used:**
- CoinGecko (crypto)
- Dog API (random dogs)
- Cat Facts (facts)
- REST Countries (search)
- JSONPlaceholder (blog posts)

**Features:**
- 6 different APIs in one page
- Interactive buttons
- Real-time data

**Try it:**
```bash
open demos/api-dashboard.html
```

---

## 🎨 What ApiBridge Does For You

While using these demos, ApiBridge Pro provides:

✅ **Caching**
- Second request = instant (<10ms!)
- Open dashboard to see cache stats

✅ **Rate Limiting**
- Protects APIs from abuse
- Dashboard shows when limits hit

✅ **Monitoring**
- Every request tracked
- Real-time stats in dashboard

✅ **Error Handling**
- Graceful failures
- Clean error messages

✅ **Cost Control**
- Budget tracking (all $0 for free APIs)
- Would alert if paid API exceeded budget

---

## 📊 Watch It In Action

### Step 1: Open Dashboard
```
http://127.0.0.1:8000/admin
```

### Step 2: Open a Demo
```bash
open demos/api-dashboard.html
```

### Step 3: Click Buttons in Demo

Watch the dashboard update in real-time:
- Request counts increase
- Cache statistics grow
- Budget stays at $0
- Health status updates

**It's magical!** ✨

---

## 🧪 Experiments to Try

### Test Caching

1. Open `bitcoin-tracker.html`
2. Note the latency (e.g., 350ms)
3. Refresh page immediately
4. Note new latency (e.g., 15ms) ← **CACHED!**
5. Check dashboard → cache hits increased!

### Test Rate Limiting

1. Open browser console (F12)
2. Run this:
```javascript
for (let i = 0; i < 100; i++) {
  fetch('http://localhost:8000/proxy/catfacts/fact')
    .then(r => r.json())
    .then(d => console.log(i, d.fact));
}
```
3. Some will return 429 (rate limited)
4. Check dashboard → rate limit stats!

### Test Multi-Provider (if you add real weather keys)

1. Set real API keys for weather
2. Kill one provider (block the domain)
3. Weather still works! (failover to backup)
4. Dashboard shows which provider was used

---

## 🎯 Customize These Demos

All demos are simple HTML + JavaScript.

**Easy customizations:**
- Change colors in `<style>` section
- Add more APIs (copy button code)
- Modify layouts
- Add your branding

**Advanced:**
- Add charts (Chart.js)
- Add database (save data)
- Build with React/Vue
- Deploy to production

---

## 💡 Building Your Own App

Use these demos as templates:

```javascript
// Basic pattern:
async function getDataFromAPI() {
    const response = await fetch('http://localhost:8000/proxy/{connector}/{path}');
    const data = await response.json();
    // Use the data!
}
```

**That's it!** ApiBridge handles:
- Caching
- Rate limiting  
- Error handling
- Monitoring
- Cost tracking

---

## 🚀 Next Steps

### For Learning:
1. Open each demo
2. View source code (right-click → View Source)
3. Understand the pattern
4. Build your own!

### For Your Portfolio:
1. Customize a demo
2. Add features
3. Deploy somewhere
4. Show to employers!

### For Real Apps:
1. Pick a use case
2. Add necessary APIs
3. Build frontend
4. Deploy with ApiBridge backend

---

## 📚 More Resources

- **Full guide:** `WHAT_TO_BUILD.md` (841 lines of examples!)
- **API list:** `FREE_APIS_GUIDE.md` (100+ free APIs)
- **Tutorials:** `TUTORIAL.md` (step-by-step)
- **Dashboard:** http://127.0.0.1:8000/admin

---

## 🎉 You're Ready!

You have:
- ✅ 8 working APIs
- ✅ 3 demo apps
- ✅ Complete guides
- ✅ Running dashboard

**Start building!** 💻✨

---

**Questions?** Check the guides or open an issue on GitHub!

