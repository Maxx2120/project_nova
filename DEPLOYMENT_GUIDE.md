# Complete Deployment Workflow

## Phase 1: Push Code to GitHub

### Option A: I Push for You
Provide your GitHub repo URL. I'll commit and push the updated code.

**Tell me:**
```
Your GitHub repo URL: https://github.com/YOUR_USERNAME/final-year-project.git
```

### Option B: You Push Yourself

From your project root, run:

```powershell
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare for deployment: add MODEL_HOST env var support"

# Set remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/final-year-project.git

# Push to main branch
git branch -M main
git push -u origin main
```

---

## Phase 2: Deploy Web App to Render

### 2.1 Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub (easier)

### 2.2 Create Web Service
- Click **New** → **Web Service**
- Select your GitHub repo
- Click **Connect**

### 2.3 Configure Service

| Field | Value |
|-------|-------|
| Name | `novaai-web` |
| Environment | Python 3.11 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |
| Plan | Free (or Starter $12/mo) |

### 2.4 Set Environment Variables

In **Environment** tab, add:

```
JWT_SECRET=supersecretkey123456789012345678
MODEL_HOST=http://WILL_UPDATE_LATER:11434
DATABASE_URL=sqlite:///./final_year_project.db
PYTHONUNBUFFERED=true
```

**Note:** Leave `MODEL_HOST` as placeholder for now. You'll update it after GPU VM is ready.

### 2.5 Deploy
Click **Create Web Service**. Wait 3-5 minutes for deployment.

**Get your live URL:** Render dashboard shows `https://novaai-web.onrender.com` (or similar)

---

## Phase 3: Set Up GPU VM for Models

### 3.1 Provision a GPU VM

Choose one (all support Ubuntu 20.04 LTS or later):

| Provider | Instance | Cost | Notes |
|----------|----------|------|-------|
| **AWS** | `g4dn.xlarge` | ~$0.52/hr | Standard choice |
| **GCP** | `a2-highgpu-1g` | ~$0.35/hr | Very fast |
| **Paperspace** | `GPU+ RTX 4000` | $0.40/hr | Simple console |
| **Lambda Labs** | `A10 GPU` | $0.40/hr | Easy to set up |
| **Linode** | `GPU Dedicated 1x A40` | ~$1.08/hr | Reliable |

**Quick Launch (AWS):**
1. Go to [AWS EC2](https://console.aws.amazon.com/ec2/)
2. Click **Launch Instance**
3. Search `Deep Learning AMI` → select Ubuntu version
4. Instance type: `g4dn.xlarge`
5. Storage: `50 GB` (for models)
6. Security group: Allow TCP 11434 from anywhere (or restrict to Render IPs)
7. Launch and note the **public IP**

### 3.2 Connect to VM and Run Setup Script

```bash
ssh -i your-key.pem ubuntu@<PUBLIC_IP>

# Download and run setup script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/final-year-project/main/GPU_VM_SETUP.sh
chmod +x gpu-vm-setup.sh
sudo ./gpu-vm-setup.sh

# This will take 20-40 minutes (downloads ~10GB of models)
# Keep the terminal open
```

Or run locally:
```bash
# Copy script to VM
scp -i your-key.pem GPU_VM_SETUP.sh ubuntu@<PUBLIC_IP>:~

# SSH and run
ssh -i your-key.pem ubuntu@<PUBLIC_IP>
sudo ~/gpu-vm-setup.sh
```

### 3.3 Verify Models Are Running

```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Should return JSON with "mistral" model listed
```

### 3.4 Get Public IP and Test Remotely

```bash
# From your local machine
curl http://<GPU_VM_PUBLIC_IP>:11434/api/tags

# Should return models JSON (confirms firewall opened)
```

---

## Phase 4: Connect Web App to Model Server

### 4.1 Update Render Environment Variable

1. Go to Render dashboard → your service → **Settings**
2. Click **Environment**
3. Edit `MODEL_HOST` value: `http://<GPU_VM_PUBLIC_IP>:11434`
4. Click **Save**

Render will auto-restart your app with the new environment variable.

### 4.2 Test the Connection

Wait 1-2 minutes for restart, then:

```bash
# From your browser
https://novaai-web.onrender.com/api/chat/models

# Should return list of Ollama models (mistral, etc.)
```

### 4.3 Test Chat Feature

1. Visit `https://novaai-web.onrender.com`
2. Signup / Login
3. Go to `/chat`
4. Select model: **mistral**
5. Type a message → Should get response in 10-30 seconds

---

## Phase 5: Test Image Generation (Optional for Now)

Image generation requires downloading additional model components on the GPU VM.

For now, the image feature will return: *"Model loading"* → *fails* (expected, because `backend/routers/image.py` still loads locally).

**To enable remote image generation:**
1. Update `backend/routers/image.py` to query GPU VM endpoint (instead of loading locally)
2. Or keep images on same GPU VM

For now, skip this unless you want to extend it.

---

## Summary Checklist

- [ ] Code pushed to GitHub
- [ ] Render web service created and deployed
- [ ] GPU VM provisioned (AWS/GCP/etc.)
- [ ] GPU VM setup script ran successfully
- [ ] Ollama + Mistral running on GPU VM
- [ ] Stable Diffusion model cached on GPU VM
- [ ] Firewall allows TCP 11434 from Render IP
- [ ] `MODEL_HOST` env var set in Render
- [ ] Web app restarted on Render
- [ ] Chat tested successfully with live data
- [ ] Public URL: `https://novaai-web.onrender.com` (live!)

---

## Monitoring & Logs

### Render Logs
```
Render dashboard → Your service → Logs tab
```
Shows app startup, API calls, errors.

### GPU VM Logs
```bash
ssh -i your-key.pem ubuntu@<PUBLIC_IP>
journalctl -u ollama -f  # Ollama service logs
tail -f /var/log/syslog  # System logs
```

### Check Services Running
```bash
ps aux | grep ollama
ps aux | grep python
curl http://localhost:11434/api/tags
```

---

## Costs

| Service | Cost | Notes |
|---------|------|-------|
| **Render (web app)** | Free or $12/mo | Free tier good for testing |
| **GPU VM** | $0.35–$1.08/hr | ~$250–$800/month if always on |
| **Data Transfer** | Free between same region | Keep VM same region as Render |
| **Total** | ~$250–$800/mo | Can reduce by stopping VM when not in use |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Render says "build failed" | Check logs. Usually missing dependency in `requirements.txt`. |
| Chat returns "Ollama not reachable" | Firewall blocking port 11434. Check AWS security group or GCP firewall. |
| GPU VM setup takes too long | Normal (20-40 min to download models). Don't interrupt. |
| Slow image generation (later) | Running on CPU. Ensure GPU detected: `nvidia-smi` on VM. |
| Render free tier crashes | Upgrade to Starter ($12/mo) for more memory. |

---

## Next Actions

1. **Provide GitHub URL** (optional; I can help push)
   OR run Git commands above
2. **Create Render account** and web service (follow Phase 2)
3. **Provision GPU VM** (Phase 3) — choose AWS/GCP
4. **Run GPU setup script** (Phase 3.2)
5. **Update MODEL_HOST** in Render (Phase 4.1)
6. **Test** (Phase 4.2-4.3)

**Live within 1-2 hours!** 🚀
