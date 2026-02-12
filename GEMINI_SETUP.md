# 🚀 Gemini API Setup Guide

This guide will help you integrate **Google Gemini API** into your NovaAI application for powerful chat capabilities.

## 🎯 What's Changed

- ✅ **Chat:** Now uses **Google Gemini Pro** (replaces Ollama)
- ✅ **Images:** Still uses **Stable Diffusion + LCM** (local, CPU-optimized)
- ✅ **Benefits:** No local model downloads, better quality, always up-to-date

## 📋 Requirements

- ✅ Google account (free)
- ✅ Gemini API key
- ✅ Internet connection (for API calls)
- ✅ No need for Ollama anymore

---

## 🔑 Step 1: Get Gemini API Key (FREE)

### Option A: Using makersuite.google.com (Easiest)
1. Go to: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"** button
3. Choose **"Create API key in new project"**
4. Copy your API key (looks like: `AIzaSyD...`)
5. Keep this safe!

### Option B: Using Google Cloud Console
1. Go to: https://console.cloud.google.com
2. Create new project
3. Enable Generative AI API
4. Create API key
5. Copy your API key

---

## 📝 Step 2: Set Environment Variable

### On Windows (PowerShell)

**Option 1: Set for current session only**
```powershell
$env:GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

**Option 2: Set permanently (Recommended)**
1. Press `Win + X`
2. Click **"System"**
3. Click **"Advanced system settings"**
4. Click **"Environment Variables"**
5. Click **"New..."** under User variables
6. Variable name: `GEMINI_API_KEY`
7. Variable value: `YOUR_API_KEY_HERE`
8. Click **OK**
9. Restart PowerShell

**Option 3: Create `.env` file (Easiest for local development)**
1. Create file in project root: `.env`
2. Add:
   ```
   GEMINI_API_KEY=YOUR_API_KEY_HERE
   ```
3. The app will automatically load it!

---

## 💾 Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- `google-generativeai>=0.3.0` (Gemini API client)
- `python-dotenv` (for .env file support)
- All other dependencies

---

## 🚀 Step 4: Start the Application

### Terminal 1: Start Web App
```powershell
python -m uvicorn backend.main:app --reload
```

### Terminal 2: Open Browser
```
http://localhost:8000/
```

**That's it!** No need to start Ollama anymore.

---

## ✅ Verify Setup

### Method 1: Test in Web UI
1. Go to http://localhost:8000/
2. Sign up / Login
3. Go to Chat page
4. Type a message → Should get response from Gemini

### Method 2: Test via Python
```python
import os
os.environ["GEMINI_API_KEY"] = "YOUR_KEY_HERE"

from backend import model_manager
model = model_manager.get_gemini_model()
response = model.generate_content("Hello! What is 2+2?")
print(response.text)
```

### Method 3: Check Logs
Look for in terminal:
```
✓ Gemini API loaded
✓ Gemini API configured successfully
```

---

## 🎯 Gemini Pro Capabilities

| Feature | Capability | Cost |
|---------|-----------|------|
| **Text Generation** | ✅ Excellent | Free tier: 60 calls/minute |
| **Reasoning** | ✅ Very good | Free tier included |
| **Code Generation** | ✅ Very good | Free tier included |
| **Long Context** | ✅ Good (30K tokens) | Free tier included |
| **Multilingual** | ✅ Yes | Free tier included |
| **Image Analysis** | ✅ Via gemini-pro-vision | Upgrade required |

---

## 💰 Pricing

### Free Tier
- **60 requests per minute**
- **Sufficient for personal projects**
- No credit card required initially
- Great for testing!

### Paid Tier
- **More requests** (100+ per minute)
- **Vision capabilities** (image analysis)
- **Better rate limits**
- **Cost:** ~$0.0005 per 1K input tokens

For this project, **free tier is more than enough**.

---

## 🔒 Security Best Practices

### ✅ DO:
- Store API key in `.env` file (not in code)
- Add `.env` to `.gitignore`
- Rotate keys periodically
- Use environment variables in production

### ❌ DON'T:
- Commit `.env` file to Git
- Share API key in messages/emails
- Put key in frontend code
- Use same key for multiple projects

### .gitignore (Ensure included)
```
.env
.env.local
*.env
```

---

## 🛠️ Troubleshooting

### "GEMINI_API_KEY not configured"
**Problem:** App can't find your API key

**Solutions:**
1. Check environment variable is set:
   ```powershell
   $env:GEMINI_API_KEY
   ```
2. Create `.env` file with key
3. Restart PowerShell/Terminal

### "Error: Quota exceeded"
**Problem:** Rate limit reached (60 requests/minute)

**Solution:**
- Wait a minute before next request
- Upgrade to paid tier for more limits
- Add retry logic in code

### "Invalid API key"
**Problem:** API key is wrong or revoked

**Solutions:**
1. Get new key from makersuite.google.com
2. Check for typos/spaces
3. Verify key format (starts with `AIzaSy`)

### "Connection timeout"
**Problem:** No internet connection

**Solution:**
- Check internet connection
- Check firewall settings
- Verify Google API is not blocked in region

### App crashes on startup
**Problem:** Gemini model initialization fails

**Solution:**
```powershell
# Test separately
python -c "import google.generativeai; print('✓ Gemini installed')"

# Reinstall if needed
pip install --upgrade google-generativeai
```

---

## 📊 Performance Comparison

| Aspect | Gemini API | Ollama Local | Stable Diffusion Local |
|--------|-----------|-------------|----------------------|
| **Chat Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | N/A |
| **Chat Speed** | ⚡ 2-10s | ⚡ 5-15s | N/A |
| **RAM Usage** | ✅ ~0MB | ❌ 5-6GB | ⚠️ 4-6GB (images only) |
| **Setup Time** | ⚡ 5 min | ⌛ 30 min | ⌛ 20 min |
| **Internet Required** | ✅ Yes | ❌ No | ❌ No |
| **Cost** | 💰 Free tier | ✅ Free | ✅ Free |
| **Offline Use** | ❌ No | ✅ Yes | ✅ Yes |

**Recommendation for your setup:**
- Use **Gemini API** for chat ✅ (best quality, lowest RAM)
- Keep **Stable Diffusion** for images ✅ (works offline, CPU)

---

## 🚨 Important: Image Generation

Gemini Pro doesn't generate images. Your setup:
- **Chat:** Gemini API ✓
- **Images:** Stable Diffusion + LCM ✓

This is optimal! You get:
- Best chat quality (Gemini)
- Offline image generation (SD)
- Minimal RAM usage (~4-6GB for images when generating)

---

## 📖 Useful Links

- Gemini API Docs: https://ai.google.dev/tutorials/python_quickstart
- API Key Page: https://makersuite.google.com/app/apikey
- Rate Limits: https://ai.google.dev/docs/quotas_limits
- Models: https://ai.google.dev/models
- Python Library: https://github.com/google/generative-ai-python

---

## 🎓 Code Example

### Using Gemini Directly
```python
import google.generativeai as genai
import os

# Configure API
gemini_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)

# Create model
model = genai.GenerativeModel('gemini-pro')

# Generate response
response = model.generate_content("What is machine learning?")
print(response.text)
```

### Using in FastAPI (Already Configured!)
```python
from backend import model_manager

# In your endpoint:
model = model_manager.get_gemini_model()
response = model.generate_content(user_message)
generated_text = response.text
```

---

## 📝 What Changed in Your Code

### Files Modified:
1. **`requirements.txt`** - Added `google-generativeai` and `python-dotenv`
2. **`backend/model_manager.py`** - Added Gemini model loading
3. **`backend/routers/chat.py`** - Now uses Gemini API instead of Ollama

### Key Changes:
```python
# Before: Ollama
response = await client.post("http://localhost:11434/api/generate", ...)

# After: Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(user_message)
```

---

## ✨ Next Steps

1. **Get API Key:** https://makersuite.google.com/app/apikey
2. **Set up .env file** in project root:
   ```
   GEMINI_API_KEY=YOUR_KEY_HERE
   ```
3. **Install deps:** `pip install -r requirements.txt`
4. **Run app:** `python -m uvicorn backend.main:app --reload`
5. **Test:** http://localhost:8000/ → Chat page

---

**Ready? Get your API key and start chatting! 🚀**
