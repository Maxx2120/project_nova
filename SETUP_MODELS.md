# Model Setup Guide - NovaAI

This guide will help you set up **Mistral** (via Ollama) and **Stable Diffusion** for your NovaAI application.

## Prerequisites

- **Disk Space**: ~15GB (10GB for Stable Diffusion + 5GB for Mistral)
- **RAM**: 8GB minimum (16GB recommended)
- **GPU** (optional): NVIDIA GPU with CUDA support for faster image generation

---

## Step 1: Install Ollama (for Mistral Chat Model)

### Windows:

1. Download the Ollama installer from [https://ollama.ai](https://ollama.ai)
2. Run the installer and follow the setup wizard
3. Once installed, Ollama will start automatically as a service
4. Verify it's running: Open PowerShell and run:
   ```powershell
   curl http://localhost:11434/api/tags
   ```
   You should see a JSON response.

### Pull the Mistral Model:

1. Open PowerShell and run:
   ```powershell
   ollama pull mistral
   ```
   This will download the Mistral model (~4GB, takes 5-10 minutes)

2. Verify it's available:
   ```powershell
   ollama list
   ```
   You should see `mistral` in the list.

3. Test the model:
   ```powershell
   ollama run mistral
   ```
   Type a message to test - type `exit` to quit.

---

## Step 2: Download Stable Diffusion Model

The setup script will automatically download and cache the Stable Diffusion v1-5 model.

### From your project directory, run:

```powershell
cd "c:\Users\uha\OneDrive\Desktop\final year project"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the setup script
python setup_models.py
```

**What happens:**
- Downloads Stable Diffusion v1-5 (~4GB) - first run takes 5-10 minutes
- Model is cached in `%USERPROFILE%\.cache\huggingface\diffusers\`
- Subsequent runs will use the cached model (instant)

**Progress:**
```
============================================================
Setting up Stable Diffusion v1-5...
============================================================

Downloading runwayml/stable-diffusion-v1-5...
This may take 5-10 minutes on first run (~4GB download)
Using device: cpu
✓ Stable Diffusion model downloaded and cached successfully!
  Model location: C:\Users\...\AppData\Local\pip\cache\huggingface\diffusers


============================================================
Setting up Mistral for Ollama...
============================================================

Note: This requires Ollama to be installed and running.
Download Ollama from: https://ollama.ai

Attempting to pull Mistral model...
(This may take 5-10 minutes on first run)
✓ Mistral model pulled successfully!
  Model: mistral
```

---

## Step 3: Start the Application

Once both models are set up:

```powershell
# From your project directory
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The server will start and automatically initialize the models on startup.

---

## Step 4: Test the Features

### Chat (Mistral):
- Navigate to: http://127.0.0.1:8000/chat
- Make sure you're logged in
- Select "mistral" as the model
- Type a message and send
- Wait for response (5-30 seconds depending on message length)

### Image Generation (Stable Diffusion):
- Navigate to: http://127.0.0.1:8000/image-generator
- Make sure you're logged in
- Enter a detailed prompt (e.g., "A beautiful sunset over mountains")
- Click "Generate"
- Wait for generation (1-3 minutes on CPU, 10-30 seconds on GPU)
- Image will be displayed and saved

---

## Troubleshooting

### "Ollama not reachable" error when generating chat

**Problem:** Chat endpoint can't connect to Ollama
**Solution:**
1. Make sure Ollama is running: `ollama serve` in a separate terminal
2. Check Ollama is on port 11434: `curl http://localhost:11434/api/tags`
3. Restart the FastAPI server

### Image generation is very slow

**Problem:** Stable Diffusion running on CPU
**Solution:**
- If you have an NVIDIA GPU:
  1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
  2. Reinstall PyTorch with CUDA support:
     ```powershell
     pip uninstall torch -y
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```
- Alternatively, use smaller models or reduce `num_inference_steps` in the code

### "Out of Memory" errors

**Problem:** Not enough RAM to load models
**Solution:**
1. Close other applications
2. Reduce `num_inference_steps` in `backend/routers/image.py` (default: 50, try 20-30)
3. Use NVIDIA GPU if available
4. Use smaller models (option for future improvement)

### Model download gets stuck

**Problem:** Network interruption during download
**Solution:**
1. Delete the cache:
   ```powershell
   rm -r "$env:USERPROFILE\.cache\huggingface"
   ```
2. Re-run setup: `python setup_models.py`
3. Or manually: `ollama pull mistral`

---

## System Information

Check your setup:

```powershell
# Python version
python --version

# Check CUDA availability
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# List installed packages
pip list | grep -E "torch|diffusers|ollama"
```

---

## Notes

- **First run**: Both model downloads are large. Allow 15-30 minutes total
- **Caching**: After first run, models are cached and load much faster
- **GPU acceleration**: Highly recommended for image generation
- **Ollama background service**: On Windows, Ollama runs as a service and starts automatically with the system

---

## Next Steps

Once everything is running:
1. ✅ Test the chat feature with a simple prompt
2. ✅ Test image generation with a detailed prompt
3. ✅ Create user accounts and test persistence
4. ✅ Check generated images in `static/generated_images/`
5. ✅ View chat history in the database

Enjoy your AI web app! 🚀
