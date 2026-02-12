# ⚡ Quick Start with Gemini API

## 🚀 3-Step Setup

### Step 1: Get Free API Key (2 minutes)
```
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key (looks like: AIzaSyD...)
```

### Step 2: Set Environment Variable (1 minute)
Create `.env` file in project root:
```
GEMINI_API_KEY=YOUR_KEY_HERE
```

### Step 3: Install & Run (1 minute)
```powershell
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

Then visit: **http://localhost:8000/**

---

## ✅ Verify It Works

Type in Chat page: `"Hello! What is Python?"`

You should get a response from Gemini Pro instantly!

---

## 📊 What You Get

- **Chat:** Gemini Pro (free, unlimited for reasonable use)
- **Images:** Stable Diffusion (local, CPU-optimized, offline)
- **Speed:** Images 5-10s, Chat 2-10s
- **RAM:** ~4-6GB (down from 12GB with Ollama + SD)
- **Zero Internet Required for Images:**  ✓ (SD works offline)

---

## 🔒 Important: API Key Security

1. **Never commit .env to Git**
2. Add to .gitignore:
   ```
   .env
   .env.local
   ```
3. Keep key private!

---

## 🆘 Troubleshooting

**"GEMINI_API_KEY not configured"**
- Restart PowerShell after setting environment variable
- Or create `.env` file instead

**Still getting errors?**
- See full guide: [GEMINI_SETUP.md](GEMINI_SETUP.md)

---

**Need help? Check GEMINI_SETUP.md for complete documentation! 📖**
