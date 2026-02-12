# ⚡ Quick Start Commands

## 🏃 Run Everything (3 Steps)

### Step 1: Install Dependencies
```powershell
python setup_cpu_optimization.py
```

### Step 2: Start Ollama (Keep this terminal open)
```powershell
ollama serve
```

### Step 3: Start Web App (New terminal)
```powershell
python -m uvicorn backend.main:app --reload
```

Then visit: **http://localhost:8000/**

---

## 💬 First-Time Ollama Setup

```powershell
# 1. Download model (one time, ~1.5GB)
ollama pull phi

# 2. Verify it's installed
ollama list

# 3. Start service
ollama serve
```

---

## 🎯 What You Get

| Feature | Speed | Quality | RAM |
|---------|-------|---------|-----|
| **Image Generation** | 5-10 sec | 🟢 Good | 4-6GB |
| **Chat** | 5-15 sec | 🟢 Good | 5-6GB |
| **Combined** | Fast | 🟢 Good | ~12GB ✅ |

---

## 🛠️ Troubleshooting One-Liners

```powershell
# Check if Ollama is running
curl http://localhost:11434/api/tags

# View available models
ollama list

# See what's loaded in memory
ollama list --verbose

# Clear Ollama cache (if having issues)
ollama list | % { ollama rm $_.Name }
ollama pull phi

# Monitor memory during generation
Get-Process | Where-Object {$_.WorkingSet -gt 500MB} | Sort-Object WorkingSet -Descending
```

---

## 📖 Full Documentation

See **CPU_OPTIMIZATION_GUIDE.md** for:
- Detailed setup instructions
- Performance tips
- Model alternatives
- Troubleshooting guide
- Performance monitoring

---

## 🚨 If Something's Wrong

1. **Ollama not found**
   ```powershell
   # Install from https://ollama.ai
   ```

2. **"Model not available" in chat**
   ```powershell
   ollama pull phi
   ```

3. **"Stable Diffusion model not available"**
   ```bash
   python setup_models.py
   ```

4. **Slow image generation**
   - First run is slower (model warmup)
   - Close other applications
   - Wait 5-10 minutes for optimization

5. **Out of memory**
   - Reduce browser tabs (consumes RAM)
   - Use TinyLlama instead of Phi:
     ```powershell
     ollama pull tinyllama
     ```

---

**Ready to go? Run Step 1 above! 🚀**
