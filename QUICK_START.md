# 🚀 NovaAI - Model Installation & Integration

This document explains how to set up both **Mistral** and **Stable Diffusion** for your NovaAI project.

## What We've Set Up

✅ **Mistral LLM** - Integrated with Ollama for intelligent chat
✅ **Stable Diffusion v1-5** - Local image generation  
✅ **Model Manager** - Central module for model initialization and access
✅ **Auto-initialization** - Models load automatically on app startup

---

## Quick Start (3 Steps)

### Step 1️⃣ Install Ollama

Download and install from: **https://ollama.ai**

This provides Mistral for your chatbot.

### Step 2️⃣ Run Model Setup Script

Open PowerShell in your project directory:

```powershell
cd "c:\Users\uha\OneDrive\Desktop\final year project"
.\venv\Scripts\Activate.ps1
python setup_models.py
```

OR use the batch file:
```powershell
.\setup_models.bat
```

This will:
- Download and cache Stable Diffusion v1-5 model (~4GB)
- Configure Mistral in Ollama (~4GB)
- Verify both models are ready

### Step 3️⃣ Start the Server

```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

**Visit:** http://127.0.0.1:8000

---

## Architecture Overview

### Model Manager (`backend/model_manager.py`)
Central module for all AI models:
- ✅ Lazy loads Stable Diffusion pipeline
- ✅ Checks Ollama service availability
- ✅ Provides error handling and fallbacks
- ✅ Optimizes for CPU and GPU

### Image Router (`backend/routers/image.py`)
Updated to:
- ✅ Use the model manager for SD pipeline
- ✅ Handle GPU/CPU memory errors gracefully
- ✅ Create fallback placeholder images on error
- ✅ Log detailed error messages

### Chat Router (`backend/routers/chat.py`)
Already configured to:
- ✅ Call Ollama API at `http://localhost:11434`
- ✅ Support multiple models (mistral, llama2, etc.)
- ✅ Store chat history in SQLite
- ✅ Handle streaming responses

### Main App (`backend/main.py`)
Updated to:
- ✅ Initialize models on startup
- ✅ Mount static files and templates correctly
- ✅ Log application lifecycle events

---

## System Requirements

**Minimum:**
- CPU: Dual-core processor
- RAM: 8GB
- Storage: 15GB free (for models)
- Internet: Stable connection (one-time for downloads)

**Recommended:**
- CPU: Modern 4+ core processor
- RAM: 16GB+
- GPU: NVIDIA with CUDA support
- SSD: For faster model loading

**GPU Setup:**
If you have an NVIDIA GPU, install PyTorch with CUDA:
```powershell
pip uninstall torch -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## File Structure

```
final year project/
├── backend/
│   ├── model_manager.py          ← Central model management
│   ├── routers/
│   │   ├── chat.py               ← Uses Ollama (Mistral)
│   │   └── image.py              ← Uses Stable Diffusion
│   ├── main.py                   ← Model initialization on startup
│   └── ...other files
├── setup_models.py               ← Download & cache models
├── setup_models.bat              ← Windows batch setup helper
├── SETUP_MODELS.md               ← Detailed setup guide
└── QUICK_START.md                ← This file
```

---

## Usage

### 💬 Chat Feature (Mistral)

1. Navigate to: **http://127.0.0.1:8000/chat**
2. Login with your account
3. Select model: **mistral** (or llama2 if available)
4. Type your message
5. Wait for response (5-30 seconds)

**Example prompts:**
- "What is machine learning?"
- "Write a Python function to calculate factorial"
- "Explain quantum computing in simple terms"

### 🎨 Image Generation (Stable Diffusion)

1. Navigate to: **http://127.0.0.1:8000/image-generator**
2. Login with your account
3. Enter a detailed prompt
4. Click "Generate"
5. Wait for result (30-120 seconds on CPU, 10-30 on GPU)

**Example prompts:**
- "A beautiful sunset over mountains, oil painting"
- "A steampunk robot in a library, highly detailed"
- "A cozy coffee shop in autumn, digital art"

---

## Monitoring & Debugging

### Check Model Status

```powershell
# Check if Ollama is running
curl http://localhost:11434/api/tags

# List available models in Ollama
ollama list

# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
```

### View Server Logs

The server logs in the console show:
- Model initialization status
- Request processing
- Error details with full tracebacks

### Database Files

- **Database**: `database/` directory (or root if using SQLite)
- **Generated images**: `static/generated_images/`
- **Chat history**: Stored in SQLite database via `ChatHistory` model

---

## Troubleshooting

### ❌ "Ollama not reachable"

**Solution:**
```powershell
# Start Ollama service
ollama serve

# In another terminal, pull fresh model
ollama pull mistral
```

### ❌ "Stable Diffusion failed to load"

**Solution:**
```powershell
# Clear cache and re-download
rm -r "$env:USERPROFILE\.cache\huggingface"
python setup_models.py
```

### ❌ "CUDA out of memory"

**Solution:**
Reduce `num_inference_steps` in `backend/routers/image.py` (default 50 → try 20-30)

### ❌ "Download timeout"

**Solution:**
Network interrupted. Delete cache and try again:
```powershell
rm -r "$env:USERPROFILE\.cache\huggingface"
python setup_models.py
```

---

## Performance Tips

| Setting | Speed | Quality | RAM Used |
|---------|-------|---------|----------|
| 20 steps | ⚡⚡⚡ Fast | ⭐⭐ | 2GB |
| 50 steps | ⚡⚡ Medium | ⭐⭐⭐ | 4GB |
| 75 steps | ⚡ Slow | ⭐⭐⭐⭐ | 6GB |

Modify in `backend/routers/image.py` line 25:
```python
image = pipe(request.prompt, num_inference_steps=50).images[0]  # 50 = default
```

---

## Next Steps

After setup is complete:

1. ✅ Test chat: Ask Mistral a simple question
2. ✅ Test image generation: Create 1-2 images to verify
3. ✅ Create accounts: Test authentication
4. ✅ Check persistence: Verify chat history and images save
5. ✅ Explore: Try the video editor and other features

---

## Additional Resources

- **Ollama**: https://ollama.ai
- **Hugging Face Diffusers**: https://huggingface.co/docs/diffusers
- **Mistral Model**: https://huggingface.co/mistralai
- **Stable Diffusion**: https://huggingface.co/runwayml

---

## Support

If you encounter issues:

1. Check logs in the terminal for detailed error messages
2. Verify both Ollama and FastAPI are running
3. Ensure you have 15GB+ free disk space
4. Check internet connection for model downloads
5. Try restarting both services

---

**Last Updated:** February 10, 2026

🎉 Your NovaAI instance is now ready with full AI capabilities!
