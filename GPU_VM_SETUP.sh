#!/bin/bash
# GPU VM Setup Script - Install Ollama + Mistral + Stable Diffusion
# Run on a GPU-enabled Linux VM (AWS g4dn, GCP A2, Paperspace, Lambda Labs, etc.)
# Usage: chmod +x gpu-vm-setup.sh && ./gpu-vm-setup.sh

set -e

echo "==================================================================="
echo "NovaAI GPU Model Server Setup"
echo "==================================================================="
echo ""

# Check if running with sudo (optional but recommended)
if [[ $EUID -ne 0 ]]; then
   echo "⚠️  Not running with sudo. Some steps may fail."
   echo "Recommended: sudo ./gpu-vm-setup.sh"
   echo ""
fi

# ---- Step 1: System Updates ----
echo "Step 1: Updating system packages..."
apt-get update
apt-get upgrade -y

# ---- Step 2: Install CUDA + cuDNN (for GPU) ----
echo ""
echo "Step 2: Checking NVIDIA GPU and installing CUDA..."
nvidia-smi
if [ $? -ne 0 ]; then
    echo "⚠️  No NVIDIA GPU detected. Models will run on CPU (very slow)."
    echo "Proceeding anyway..."
else
    echo "✓ NVIDIA GPU detected."
    # CUDA toolkit may already be installed. Skip if present.
    if ! command -v nvcc &> /dev/null; then
        echo "Installing CUDA Toolkit..."
        # For Ubuntu 22.04 LTS
        wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
        dpkg -i cuda-keyring_1.0-1_all.deb
        apt-get update
        apt-get install -y cuda-toolkit-12-1
        echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
        export PATH=/usr/local/cuda/bin:$PATH
    fi
fi

# ---- Step 3: Install Python + pip ----
echo ""
echo "Step 3: Installing Python 3.11 and pip..."
apt-get install -y python3.11 python3.11-pip python3.11-venv
python3.11 --version

# ---- Step 4: Install Ollama ----
echo ""
echo "Step 4: Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh
ollama --version

# ---- Step 5: Pull Mistral Model ----
echo ""
echo "Step 5: Pulling Mistral model (this may take 5-10 minutes)..."
echo "⏳ Please wait..."
ollama pull mistral
echo "✓ Mistral model ready!"

# ---- Step 6: Create Virtual Environment for Stable Diffusion ----
echo ""
echo "Step 6: Setting up Python virtual environment for Stable Diffusion..."
cd /opt || cd ~
mkdir -p novaai-models
cd novaai-models
python3.11 -m venv venv
source venv/bin/activate

# ---- Step 7: Install PyTorch with CUDA Support ----
echo ""
echo "Step 7: Installing PyTorch with GPU support (CUDA 12.1)..."
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('PyTorch version:', torch.__version__)"

# ---- Step 8: Install Stable Diffusion + Dependencies ----
echo ""
echo "Step 8: Installing Stable Diffusion and dependencies..."
pip install diffusers accelerate safetensors transformers Pillow

# ---- Step 9: Download Stable Diffusion Model ----
echo ""
echo "Step 9: Downloading Stable Diffusion v1-5 (this may take 10-20 minutes, ~5GB)..."
python3.11 << 'PYTHON_SCRIPT'
from diffusers import StableDiffusionPipeline
import torch

print("Downloading Stable Diffusion v1-5...")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None
)
print("✓ Stable Diffusion downloaded and cached!")
print(f"Device: {device}")
PYTHON_SCRIPT

# ---- Step 10: Create Systemd Service for Ollama ----
echo ""
echo "Step 10: Creating systemd service for Ollama..."
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=$USER
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ollama.service
sudo systemctl start ollama.service
echo "✓ Ollama service enabled!"

# ---- Step 11: Create a Simple FastAPI Wrapper (Optional) ----
echo ""
echo "Step 11: Creating FastAPI wrapper for model endpoints (optional but recommended)..."
cat > /opt/novaai-models/model_api.py << 'FASTAPI_SCRIPT'
"""
FastAPI wrapper for Ollama + Stable Diffusion
Runs on port 8001
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import httpx
import os
import json
from pathlib import Path
from diffusers import StableDiffusionPipeline
import torch

app = FastAPI(title="NovaAI Model Server")

# ---- Load Stable Diffusion Pipeline ----
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading Stable Diffusion on {device}...")
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None
)
pipe = pipe.to(device)
if device == "cpu":
    pipe.enable_attention_slicing()

# ---- Health Check ----
@app.get("/health")
def health():
    return {"status": "ok", "device": device, "models": ["mistral", "stable-diffusion"]}

# ---- Proxy Ollama /api/generate ----
@app.post("/api/generate")
async def generate(request: dict):
    """Proxy to Ollama for chat/text generation"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json=request,
                timeout=120.0
            )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")

# ---- Proxy Ollama /api/tags ----
@app.get("/api/tags")
async def list_models():
    """Proxy to Ollama for model listing"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:11434/api/tags",
                timeout=5.0
            )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")

# ---- Image Generation ----
@app.post("/api/image/generate")
def generate_image(prompt: str):
    """Generate image using Stable Diffusion"""
    try:
        print(f"Generating image: {prompt}")
        image = pipe(prompt, num_inference_steps=50).images[0]
        # Save to /tmp
        output_path = f"/tmp/generated_{hash(prompt)}.png"
        image.save(output_path)
        return FileResponse(output_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
FASTAPI_SCRIPT

echo "✓ model_api.py created!"

# ---- Step 12: Final Instructions ----
echo ""
echo "==================================================================="
echo "✅ GPU Model Server Setup Complete!"
echo "==================================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Get your VM's public IP:"
echo "   curl ifconfig.me"
echo ""
echo "2. Test Ollama is running:"
echo "   curl http://localhost:11434/api/tags"
echo ""
echo "3. Update Render environment variable:"
echo "   Set MODEL_HOST = http://<YOUR_PUBLIC_IP>:11434"
echo ""
echo "4. Configure Firewall (if needed):"
echo "   AWS Security Group: Allow inbound TCP 11434 from anywhere (or Render IP)"
echo "   GCP Firewall: gcloud compute firewall-rules create allow-ollama --allow=tcp:11434"
echo ""
echo "5. Keep the VM running (Ollama service auto-starts on reboot)"
echo ""
echo "Models available:"
echo "  - Mistral (Ollama) on port 11434"
echo "  - Stable Diffusion on same VM (loaded in memory)"
echo ""
echo "To start the FastAPI wrapper (optional):"
echo "  cd /opt/novaai-models && source venv/bin/activate"
echo "  python model_api.py"
echo "  Then set MODEL_HOST = http://<YOUR_PUBLIC_IP>:8001"
echo ""
echo "==================================================================="
