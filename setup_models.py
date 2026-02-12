#!/usr/bin/env python3
"""
Setup script to download and cache both Mistral and Stable Diffusion models.
Run this once before starting the application.
"""

import os
import sys
from pathlib import Path

def setup_stable_diffusion():
    """Download and cache Stable Diffusion v1-5 model"""
    print("\n" + "="*60)
    print("Setting up Stable Diffusion v1-5...")
    print("="*60)
    
    try:
        from diffusers import StableDiffusionPipeline
        import torch
        
        MODEL_ID = "runwayml/stable-diffusion-v1-5"
        
        # Check if already downloaded
        cache_dir = Path.home() / ".cache" / "huggingface" / "diffusers"
        print(f"\nCache directory: {cache_dir}")
        
        # Set environment variables for better download performance
        os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '600'  # 10 minute timeout
        
        print(f"\nDownloading {MODEL_ID}...")
        print("This may take 10-20 minutes on first run (~4-5GB download)")
        print("⏳ Please wait, model is downloading...\n")
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {device}")
        
        dtype = torch.float16 if device == "cuda" else torch.float32
        print(f"Data type: {dtype}\n")
        
        # Download and cache the model with simplified loading
        print("Initializing pipeline (this may take a few minutes)...")
        pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=dtype,
            safety_checker=None,  # Disable for faster loading in dev
            use_auth_token=False   # No auth needed for public model
        )
        
        print(f"\n✅ Stable Diffusion model downloaded successfully!")
        print(f"   Model: {MODEL_ID}")
        print(f"   Device: {device}")
        print(f"   Location: {cache_dir}")
        
        # Test load
        pipe = pipe.to(device)
        if device == "cpu":
            pipe.enable_attention_slicing()
        print("   ✅ Pipeline tested and optimized")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading Stable Diffusion: {e}")
        print(f"\nTroubleshooting:")
        print(f"  1. Check your internet connection")
        print(f"  2. Ensure you have 5-10GB free disk space")
        print(f"  3. Try again: python setup_models.py")
        print(f"  4. Alternative: Download manually from https://huggingface.co/runwayml/stable-diffusion-v1-5")
        return False


def setup_mistral():
    """Pull Mistral model from Ollama"""
    print("\n" + "="*60)
    print("Setting up Mistral for Ollama...")
    print("="*60)
    
    try:
        import ollama
        
        print("\n✓ Ollama package installed")
        print("ℹ️  Note: Ensure Ollama is installed and running on your system")
        print("   Download from: https://ollama.ai/")
        print("   Start with: ollama serve (in separate terminal)\n")
        
        print("⏳ Attempting to pull Mistral model...")
        print("   (This may take 5-10 minutes on first run)\n")
        
        # Pull the model - this will show progress
        try:
            # Test connection first
            ollama.list()
            print("✅ Connected to Ollama service\n")
        except:
            print("⚠️  Could not connect to Ollama service")
            print("   Make sure to run: ollama serve")
            print("   Then in another terminal: ollama pull mistral\n")
            return False
        
        # Pull mistral
        response = ollama.pull('mistral')
        print(f"\n✅ Mistral model pulled successfully!")
        
        # Verify it's available
        models = ollama.list()
        available = [m['name'] for m in models['models'] if 'mistral' in m['name'].lower()]
        if available:
            print(f"   Available models: {', '.join(available)}")
        
        return True
        
    except ImportError:
        print("⚠️  Ollama package not available (already installed via pip)")
        print("   Steps to complete manually:")
        print("   1. Download and install Ollama from: https://ollama.ai/")
        print("   2. Run: ollama serve")
        print("   3. In another terminal: ollama pull mistral")
        return False
    except ConnectionError:
        print("⚠️  Could not connect to Ollama service")
        print("   Steps to start Ollama:")
        print("   1. Make sure Ollama is installed: https://ollama.ai/")
        print("   2. Start the service: ollama serve")
        print("   3. In another terminal: ollama pull mistral")
        return False
    except Exception as e:
        print(f"⚠️  Error setting up Mistral: {e}")
        print("   Manual steps:")
        print("   1. Start Ollama: ollama serve")
        print("   2. Pull model: ollama pull mistral")
        return False

def setup_tinyllama():
    """Pull TinyLlama model from Ollama (Lightweight)"""
    print("\n" + "="*60)
    print("Setting up TinyLlama (Lightweight)...")
    print("="*60)
    
    try:
        import ollama
        print("⏳ Attempting to pull TinyLlama model...")
        ollama.pull('tinyllama')
        print(f"\n✅ TinyLlama model pulled successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Could not pull TinyLlama: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("NovaAI - Model Setup")
    print("="*60)
    
    sd_success = False
    mistral_success = False
    
    # Setup Stable Diffusion
    try:
        sd_success = setup_stable_diffusion()
    except KeyboardInterrupt:
        print("\n⚠️  Setup cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error during Stable Diffusion setup: {e}")
    
    # Setup Mistral
    try:
        mistral_success = setup_mistral()
    except KeyboardInterrupt:
        print("\n⚠️  Setup cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error during Mistral setup: {e}")

    # Setup TinyLlama
    tinyllama_success = False
    try:
        tinyllama_success = setup_tinyllama()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n❌ Unexpected error during TinyLlama setup: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("Setup Summary")
    print("="*60)
    print(f"Stable Diffusion: {'✅ Ready' if sd_success else '⚠️  Check steps above'}")
    print(f"Mistral (Ollama):  {'✅ Ready' if mistral_success else '⚠️  Check steps above'}")
    print(f"TinyLlama (Ollama): {'✅ Ready' if tinyllama_success else '⚠️  Check steps above'}")
    
    if sd_success and (mistral_success or tinyllama_success):
        print("\n✅ All models are ready!")
        print("\nNext steps:")
        print("  1. Start the app: python -m uvicorn backend.main:app --reload")
        print("  2. Visit: http://127.0.0.1:8000")
        print("  3. Test chat and image generation!")
        return 0
    elif sd_success or mistral_success:
        print("\n⚠️  Partial setup. Some features may be limited.")
        print("   Follow the troubleshooting steps above to complete setup.")
        return 0
    else:
        print("\n❌ Setup incomplete. Check the steps above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
