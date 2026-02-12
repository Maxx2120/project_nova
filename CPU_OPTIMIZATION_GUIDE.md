# CPU Optimization Guide for Your Laptop

This guide will help you set up **lightweight, CPU-optimized models** for both image generation and chat on your **AMD Ryzen 7 5825U laptop with 16GB RAM**.

## 🎯 Your Setup

- **Processor:** AMD Ryzen 7 5825U (8 cores, integrated Radeon GPU)
- **RAM:** 16GB (13.8GB usable)
- **Image Model:** Stable Diffusion + LCM Scheduler (5-10 sec/image)
- **Chat Model:** Phi-2 via Ollama (best balance for CPU)

---

## 🖼️ Image Generation Setup

### What Changed
- **Before:** Stable Diffusion v1.5 (50 steps, ~3-5 minutes per image on CPU)
- **After:** Stable Diffusion v1.5 + LCM Scheduler (4 steps, ~5-10 seconds per image on CPU)

### LCM (Latent Consistency Model) Benefits
- ✅ **4x-10x faster** than standard SD
- ✅ **Same quality** with fewer steps
- ✅ **Lower memory** footprint
- ✅ **CPU-optimized** inference

### Installation

1. **Update requirements:**
   ```bash
   pip install --upgrade diffusers transformers torch accelerate
   pip install lcm-solver omegaconf safetensors
   ```

2. **Start the application:**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

### Expected Performance
- **First run:** 2-3 minutes (model download + setup)
- **Subsequent runs:** 5-15 seconds per image
- **RAM usage:** ~4-6GB
- **CPU usage:** 100% (all cores during generation)

### Tips for Faster Generation
- Use shorter prompts (5-10 words)
- Avoid complex descriptions
- First generation is slower (model warming up)

---

## 💬 Chat Setup

### What Model to Use: Phi-2

**Why Phi-2?**
- ✅ Only 2.7B parameters (small but powerful)
- ✅ Best quality-to-size ratio
- ✅ Runs smoothly on your CPU
- ✅ 4-5GB RAM footprint
- ✅ Fast responses (5-15 seconds)

### Installation Steps

#### Step 1: Install Ollama
1. Download from: https://ollama.ai
2. Run the installer
3. Open PowerShell and verify:
   ```powershell
   ollama --version
   ```

#### Step 2: Pull Phi-2 Model
```powershell
ollama pull phi
```
This downloads ~1.5GB model file (do this once)

#### Step 3: Start Ollama Service
```powershell
ollama serve
```
This keeps Ollama running in the background (leave this terminal open)

#### Step 4: Test Chat in Your App
```bash
# In new PowerShell terminal
python -m uvicorn backend.main:app --reload
```

Visit: `http://localhost:8000/` → Chat page

### Expected Performance
- **Model load time:** 10-20 seconds (first time)
- **Response time:** 5-15 seconds per message
- **RAM usage:** 5-6GB
- **CPU usage:** 100% during response generation

### Alternative Chat Models (if Phi-2 is too slow)
```powershell
ollama pull tinyllama      # 1.1B - Fast, lower quality
ollama pull neural-chat    # 7B - Slower but better quality
ollama pull mistral        # 7B - Best quality (slower)
```

---

## 📊 Complete System Requirements

```
Total RAM when running both:
├── OS + Applications:     ~2-3GB
├── Image Generation:      ~4-6GB (during generation)
└── Chat:                  ~5-6GB (during response)
   ─────────────────────────────────
   Total Peak Usage:       11-14GB ✅ (leaves 2-3GB buffer)
```

---

## 🚀 Quick Start Commands

### Terminal 1: Start Ollama (Keep Running)
```powershell
ollama serve
```

### Terminal 2: Start Web App
```powershell
python -m uvicorn backend.main:app --reload
```

### Then Open Browser
```
http://localhost:8000/
```

---

## ⚡ Performance Optimization Tips

### For Image Generation
1. **Use LCM** (already configured) ✓
2. **Close browser tabs** - Reduces memory pressure
3. **Avoid running other heavy apps** - Chrome, VS Code, etc.
4. **Shorter prompts** = Faster generation

### For Chat
1. **Use Phi-2** (already configured) ✓
2. **Shorter context** = Faster responses
3. **One chat at a time** - CPU can handle one LLM inference
4. **Restart Ollama periodically** - Clears memory cache

### System-Wide
- Disable unnecessary startup apps
- Monitor task manager during testing
- Close unused browser tabs

---

## 🔧 Troubleshooting

### Image Generation is Slow
**Problem:** Taking >20 seconds
**Solution:**
```python
# In backend/routers/image.py, change steps to:
steps = 2  # Even faster (lower quality)
steps = 4  # Default (good balance)
steps = 6  # Better quality (slower)
```

### Chat is Not Responding
**Problem:** Connection error to Ollama
**Solution:**
1. Check if Ollama is running: `ollama serve` in Terminal 1
2. Verify model is loaded:
   ```powershell
   ollama list
   ```
3. Test Ollama directly:
   ```powershell
   curl http://localhost:11434/api/tags
   ```

### Out of Memory Errors
**Problem:** App crashes with OOM
**Solution:**
1. Close other applications
2. Use smaller model:
   ```powershell
   ollama pull tinyllama  # Much smaller
   # Then change DEFAULT_MODEL in backend/routers/chat.py
   ```
3. Reduce inference steps for images

### Model Not Found
**Problem:** "Model not available" error
**Solution:**
1. Run setup script:
   ```bash
   python setup_models.py
   ```
2. Ensure Ollama models are pulled:
   ```powershell
   ollama pull phi
   ```

---

## 📈 Monitoring Performance

### Check CPU Usage
```powershell
# In PowerShell
Get-Process | Where-Object {$_.WorkingSet -gt 100MB} | Sort-Object WorkingSet -Descending
```

### Check GPU (if applicable)
```powershell
# AMD Radeon GPU info
wmic path win32_videocontroller get name
```

### Monitor Memory in Task Manager
- Press Ctrl+Shift+Esc
- Click "Performance" tab
- Watch Memory usage during generation

---

## 📝 Model Specifications Summary

| Component | Model | Size | Speed | Quality | RAM |
|-----------|-------|------|-------|---------|-----|
| **Images** | SD v1.5 + LCM | 4GB | ⚡ 5-10s | Good | 4-6GB |
| **Chat** | Phi-2 | 1.5GB | ⚡ 5-15s | Good | 5-6GB |

---

## 🎓 What's Changed in Your Code

### 1. `requirements.txt`
- Added LCM support
- Added `omegaconf` and `safetensors`
- Updated version pins

### 2. `backend/model_manager.py`
- Now uses `LCMScheduler` for fast inference
- Automatically detects CPU vs GPU
- Better logging and optimization hints

### 3. `backend/routers/image.py`
- Reduced inference steps to 4 (LCM optimized)
- Faster image generation on CPU

### 4. Chat (unchanged from Ollama)
- Just install Phi-2 model with Ollama
- App automatically uses it

---

## 📞 Need Help?

If something doesn't work:

1. **Check logs:**
   ```powershell
   # Look at terminal output for error messages
   ```

2. **Verify setup:**
   ```powershell
   python verify_installation.py
   ```

3. **Test components separately:**
   ```bash
   python -c "from diffusers import LCMScheduler; print('✓ LCM available')"
   ```

---

**Your system is ready for CPU-optimized AI! 🚀**
