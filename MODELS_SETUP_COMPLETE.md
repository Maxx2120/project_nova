# ✅ MODELS READY FOR DOWNLOAD & INTEGRATION

Your NovaAI project is now **fully integrated** with Mistral and Stable Diffusion. Here's what has been set up:

## 📦 What's Installed

✅ **Model Manager** (`backend/model_manager.py`)
- Centralized model initialization
- Lazy loading for Stable Diffusion
- Ollama service monitoring
- Automatic optimization for CPU/GPU

✅ **Updated Image Router** (`backend/routers/image.py`)
- Integrated with Model Manager
- Error handling for low memory
- Fallback mechanisms

✅ **Main App Updates** (`backend/main.py`)
- Models initialize on startup
- Proper logging configured

✅ **Setup Scripts**
- `setup_models.py` - Full setup wizard
- `setup_models.bat` - Windows batch helper
- `QUICK_START.md` - Comprehensive guide
- `SETUP_MODELS.md` - Detailed instructions

---

## 🚀 QUICK START (Choose One Method)

### Method 1️⃣: **Automatic Setup** (Recommended)

```powershell
cd "c:\Users\uha\OneDrive\Desktop\final year project"
.\venv\Scripts\Activate.ps1
python setup_models.py
```

This will:
1. ✅ Download Stable Diffusion v1-5 (~5GB) - ~10-20 min
2. ✅ Configure Ollama with Mistral (manual step prompted)
3. ✅ Verify everything is ready

### Method 2️⃣: **Manual Setup** (If auto-download fails)

#### Step A: Install Ollama + Mistral

```powershell
# 1. Download installer from https://ollama.ai
# 2. Run installer and complete setup
# 3. Ollama starts as Windows service automatically
# 4. In PowerShell, pull Mistral:
ollama pull mistral

# Verify it works:
ollama run mistral
# Type: exit
```

#### Step B: Download Stable Diffusion

```powershell
cd "c:\Users\uha\OneDrive\Desktop\final year project"
.\venv\Scripts\Activate.ps1

# Option 1: Using Python (one-time download)
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"

# Option 2: Using Hugging Face CLI (if preferred)
pip install huggingface-hub[cli]
huggingface-cli download runwayml/stable-diffusion-v1-5
```

#### Step C: Start the App

```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 📋 System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| **RAM** | 8GB | 16GB+ |
| **CPU** | Dual-core | 4+ cores |
| **Storage** | 15GB free | 20GB free |
| **GPU** | Any | NVIDIA w/ CUDA |
| **Internet** | Stable | Broadband |

---

## 🔍 Verify Setup Status

After downloading models:

```powershell
# Check Ollama service
curl http://localhost:11434/api/tags

# Test Ollama with Mistral:
ollama run mistral
# Type message, then: exit

# Check Python access to Stable Diffusion:
python -c "from diffusers import StableDiffusionPipeline; print('✅ Stable Diffusion ready')"
```

---

## 🎯 How Models Are Integrated

### Chat Feature (Mistral via Ollama)

**Flow:**
```
User Message 
      ↓
FastAPI Endpoint (/api/chat/generate)
      ↓
HTTP Request to Ollama (localhost:11434)
      ↓
Mistral Model Inference
      ↓
JSON Response
      ↓
Save to Database
      ↓
Return to Frontend
```

**Code location:** `backend/routers/chat.py`

### Image Generation (Stable Diffusion)

**Flow:**
```
User Prompt
      ↓
FastAPI Endpoint (/api/image/generate)
      ↓
Model Manager (backend/model_manager.py)
      ↓
Load from HuggingFace Cache
      ↓
Stable Diffusion Inference
      ↓
Save PNG to static/generated_images/
      ↓
Return URL to Frontend
```

**Code location:** `backend/routers/image.py`

---

## 💡 Usage Examples

### 💬 Chat with Mistral

```bash
# Terminal 1: Start Ollama service
ollama serve

# Terminal 2: Start the app
python -m uvicorn backend.main:app --reload

# Browser: http://127.0.0.1:8000
# → Login
# → Navigate to /chat
# → Select "mistral"
# → Send message
# → Wait 5-30 seconds for response
```

### 🎨 Generate Images

```bash
# Same setup as above, then:
# Browser: http://127.0.0.1:8000
# → Login
# → Navigate to /image-generator
# → Enter prompt: "A serene landscape with mountains, sunset"
# → Click Generate
# → Wait 30-120 seconds (CPU) or 10-30 seconds (GPU)
# → Image appears and saves to static/generated_images/
```

---

## ⚙️ Configuration Options

### Modify Image Generation Quality

Edit `backend/routers/image.py` line ~25:

```python
# Lower = faster, lower quality
# Higher = slower, higher quality
image = pipe(request.prompt, num_inference_steps=50).images[0]
```

Recommended:
- **Fast:** 20-30 steps
- **Balanced:** 40-50 steps
- **High Quality:** 60-80 steps

### Use GPU if Available

```powershell
# Install PyTorch with CUDA (for NVIDIA GPUs)
pip uninstall torch -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify:
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### Use Different Ollama Models

```powershell
# List available models
ollama list

# Try another model
ollama pull llama2
ollama pull neural-chat

# In app, select from dropdown in /chat page
```

---

## 🔧 Troubleshooting

### Issue: "Ollama not reachable"
```powershell
# Make sure Ollama is running:
ollama serve  # Run in separate terminal
```

### Issue: "Stable Diffusion download stuck"
```powershell
# Clear cache and retry:
rm -r "$env:USERPROFILE\.cache\huggingface"
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
```

### Issue: "Out of Memory"
```powershell
# Reduce steps:
# In backend/routers/image.py, change num_inference_steps to 20-30
# Or use GPU with CUDA
```

### Issue: "Download timeout"
```powershell
# Download takes time, leave terminal running
# Or set longer timeout:
set HF_HUB_DOWNLOAD_TIMEOUT=600
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
```

---

## 📊 Directory Structure

```
project/
├── backend/
│   ├── model_manager.py          ← Model management
│   ├── routers/
│   │   ├── chat.py               ← Ollama integration
│   │   └── image.py              ← Stable Diffusion integration
│   ├── main.py                   ← Auto-initialization
│   └── ...
├── static/
│   ├── generated_images/         ← Saved generated images
│   └── ...
├── setup_models.py               ← Setup wizard
├── setup_models.bat              ← Windows helper
├── QUICK_START.md                ← This guide
└── SETUP_MODELS.md               ← Detailed setup
```

---

## ✨ What's Next

1. **Download models** - Use setup_models.py or follow manual steps
2. **Start services** - Ollama serve + FastAPI app
3. **Login** - Create account at http://127.0.0.1:8000/signup
4. **Test Chat** - Ask Mistral a question
5. **Test Images** - Generate an image with prompt
6. **Explore** - Try video editor and other features

---

## 🎓 Learning Resources

- **Ollama**: https://ollama.ai (Model management)
- **Hugging Face**: https://huggingface.co (Model hub)
- **Diffusers**: https://huggingface.co/docs/diffusers (Image generation)
- **FastAPI**: https://fastapi.tiangolo.com (Backend framework)

---

## 📞 Support

If models won't download:
1. Check internet connection
2. Try manual download with `python setup_models.py`
3. Ensure 15GB+ free disk space
4. Check firewall/VPN isn't blocking HuggingFace
5. Try clearing cache: `rm -r "$env:USERPROFILE\.cache\huggingface"`

**Status:** ✅ All integrations complete. Ready for model download!

---

**Last Updated:** February 10, 2026
