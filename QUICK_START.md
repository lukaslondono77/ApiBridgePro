# ⚡ Quick Start - 5 Minutes to Running!

**The absolute fastest way to get started with ApiBridge Pro.**

---

## 🚦 Three Simple Steps

### Step 1️⃣: Install (30 seconds)

```bash
cd ApiBridgePro
pip install -r requirements.txt
```

---

### Step 2️⃣: Set Keys (30 seconds)

```bash
export OPENWEATHER_KEY=dummy
export WEATHERAPI_KEY=dummy
export GITHUB_TOKEN=dummy
```

---

### Step 3️⃣: Run! (10 seconds)

```bash
uvicorn app.main:app --reload --port 8000
```

---

## ✅ Verify It Works

```bash
# New terminal window
curl http://127.0.0.1:8000/health
```

**Expected:**
```json
{"ok": true, "mode": "live", "connectors": [...]}
```

---

## 🌐 Open Dashboard

**In your browser, go to:**
```
http://127.0.0.1:8000/admin
```

**🎉 Done! You're running an API gateway!**

---

## 🎯 What Now?

### 5-Minute Path:
1. ✅ You just did it! Gateway is running.
2. 🌐 Explore the dashboard
3. 📚 Check out the API docs: http://127.0.0.1:8000/docs

### 30-Minute Path:
Follow **TUTORIAL.md** for a hands-on walkthrough!

### Deep Dive Path:
Read **GETTING_STARTED.md** for comprehensive guide!

---

## 🔥 Try Your First API Call

```bash
# Chuck Norris joke (free, no auth needed!)
curl http://127.0.0.1:8000/proxy/jokes/jokes/random
```

Wait, that's not configured yet! Let's add it:

**Edit `connectors.yaml`, add:**
```yaml
jokes:
  base_url: https://api.chucknorris.io
  allow_paths: ["^/jokes/random$"]
```

**Save and try again:**
```bash
curl http://127.0.0.1:8000/proxy/jokes/jokes/random
```

**🎉 You just integrated your first API!**

---

## 📖 Documentation Guide

Pick your path based on your needs:

| If you want to... | Read this |
|-------------------|-----------|
| Get started in 5 min | **QUICK_START.md** ← You are here! |
| Learn by doing (30 min) | **TUTORIAL.md** |
| Comprehensive setup guide | **GETTING_STARTED.md** |
| Understand the benefits | **COMPARISON.md** |
| See ROI & business value | **BUSINESS_VALUE.md** |
| View code review findings | **IMPROVEMENTS.md** |
| Quick developer reference | **QUICKSTART.md** |

---

## 🎬 Common Commands

```bash
# Start server
make run

# Run tests  
make test

# View all commands
make help

# Stop server
# Just press CTRL+C in the terminal
```

---

## ❓ Something Wrong?

### Issue: "Command not found: pip"
**Fix:** Install Python first → https://python.org/downloads/

### Issue: "Port 8000 in use"
**Fix:** `lsof -ti:8000 | xargs kill -9` (or use port 8001)

### Issue: "Module not found"
**Fix:** `pip install -r requirements.txt`

---

## 🎉 That's It!

**You're ready to start building!**

**Next:** Follow the **TUTORIAL.md** to build something real in 30 minutes!

---

**Questions?** Check **GETTING_STARTED.md** for detailed troubleshooting.

