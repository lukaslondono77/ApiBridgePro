# 🎯 ApiBridge Pro - Live Demos

Interactive HTML demos showcasing ApiBridge Pro's capabilities with real APIs.

## 🚀 Quick Start

### 1. Start the Server

```bash
# From project root
cd ApiBridgePro
uvicorn app.main:app --reload --port 8000
```

### 2. Open Any Demo

Just **double-click** any `.html` file or open in your browser:

- **`api-dashboard.html`** - Main demo with 5 working APIs
- **`bitcoin-tracker.html`** - Live Bitcoin price tracker
- **`country-explorer.html`** - Search 195 countries
- **`simple-dashboard.html`** - Clean 4-API demo

---

## 📋 Demos Overview

### 🎯 **Main Dashboard** (`api-dashboard.html`)

**5 Real APIs Working Live:**

1. 💰 **Bitcoin Price** - Live crypto prices from CoinGecko
2. 💎 **Ethereum Price** - Live market data
3. 🐕 **Random Dogs** - Real dog photos
4. 🐱 **Cat Facts** - Fun cat trivia
5. 🌍 **Country Explorer** - Search 195 countries

**Features:**
- ✅ No setup required
- ✅ Works immediately after starting server
- ✅ Beautiful gradient design
- ✅ Mobile responsive

---

### 💰 **Bitcoin Tracker** (`bitcoin-tracker.html`)

Real-time Bitcoin price monitoring with:
- Live price updates
- Price change indicators
- Refresh on demand
- Clean, professional UI

---

### 🌍 **Country Explorer** (`country-explorer.html`)

Interactive country search with:
- 195 countries database
- Flags, capitals, populations
- Real-time search
- Detailed country information

---

### 🎨 **Simple Dashboard** (`simple-dashboard.html`)

Clean 4-API demo:
- Bitcoin & Ethereum prices
- Random dog photos
- Country search
- Minimal, focused design

---

## 🔧 Configuration

**Server must be running on:** `http://localhost:8000`

To change the port, update this line in each demo:

```javascript
// Change this:
fetch('http://localhost:8000/proxy/...')

// To your port:
fetch('http://localhost:YOUR_PORT/proxy/...')
```

---

## 📝 Customization

### Adding Your Own API

1. **Add connector** to `connectors.yaml`:

```yaml
myapi:
  base_url: https://api.example.com
  allow_paths:
    - "^/endpoint$"
```

2. **Add card** to HTML:

```html
<div class="card">
    <h2>🎯 My API</h2>
    <div class="result" id="myapi">Click to load!</div>
    <button onclick="loadMyAPI()">Load</button>
</div>
```

3. **Add JavaScript function**:

```javascript
async function loadMyAPI() {
    const res = await fetch('http://localhost:8000/proxy/myapi/endpoint');
    const data = await res.json();
    document.getElementById('myapi').innerHTML = JSON.stringify(data);
}
```

---

## 🎨 Design Features

- **Gradient backgrounds** - Modern purple/blue gradients
- **Card-based layout** - Clean, organized interface
- **Badges** - Visual indicators (LIVE, REAL, FUN)
- **Responsive design** - Works on all screen sizes
- **Smooth animations** - Hover effects and transitions

---

## 🐛 Troubleshooting

### "Failed to fetch" errors

**Solution:** Make sure the server is running:
```bash
uvicorn app.main:app --reload --port 8000
```

### CORS errors

**Solution:** Server includes CORS middleware by default. If issues persist, check `app/main.py`.

### API not working

**Solution:** Check if connector is loaded:
```bash
curl http://localhost:8000/health
```

Look for your connector in the `connectors` array.

---

## 📚 Learn More

- **Main README:** `../README.md`
- **Getting Started:** `../GETTING_STARTED.md`
- **Tutorial:** `../TUTORIAL.md`
- **API Docs:** `http://localhost:8000/docs` (when server is running)

---

## 🤝 Contributing

Want to add a demo? PRs welcome!

1. Create new `.html` file
2. Follow existing design patterns
3. Test with server running
4. Submit PR

---

## 📄 License

MIT License - See `../LICENSE` for details

---

## 🌟 Showcase

Using these demos for your project? Let us know!

- Tag us on Twitter/X
- Show us on GitHub Discussions
- Share your implementation

---

**Built with ❤️ using ApiBridge Pro**


