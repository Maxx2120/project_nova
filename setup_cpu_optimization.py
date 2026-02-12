"""
Quick Setup Script for CPU-Optimized Models
Runs all necessary setup steps for your laptop
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 CPU-OPTIMIZED AI MODEL SETUP")
    print("="*60)
    print("This script will set up:")
    print("  ✓ LCM for fast image generation (5-10 seconds)")
    print("  ✓ Phi-2 for CPU-optimized chat")
    print("  ✓ All required dependencies")
    print("="*60)
    
    input("\nPress Enter to continue...")
    
    steps = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install torch --index-url https://download.pytorch.org/whl/cpu", "Installing PyTorch (CPU version)"),
        ("pip install -r requirements.txt", "Installing requirements"),
        ("pip install lcm-solver omegaconf safetensors", "Installing LCM dependencies"),
    ]
    
    completed = 0
    for cmd, desc in steps:
        if run_command(cmd, desc):
            completed += 1
        else:
            print("\n⚠️  If you see errors with PyTorch, you may need to install manually.")
            print("Run: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
    
    print("\n" + "="*60)
    print("📋 NEXT STEPS")
    print("="*60)
    print("\n1. Install Ollama (for chat models):")
    print("   - Download from: https://ollama.ai")
    print("   - Run the installer")
    print("   - Wait for installation to complete")
    
    print("\n2. Pull Phi-2 model (chat):")
    print("   - Open PowerShell")
    print("   - Run: ollama pull phi")
    print("   - Wait for download (~1.5GB)")
    
    print("\n3. Start Ollama service:")
    print("   - Open PowerShell")
    print("   - Run: ollama serve")
    print("   - Keep this terminal open")
    
    print("\n4. Start the web app (in new terminal):")
    print("   - Open PowerShell")
    print("   - Run: python -m uvicorn backend.main:app --reload")
    print("   - Visit: http://localhost:8000/")
    
    print("\n" + "="*60)
    print(f"✅ Setup Progress: {completed}/{len(steps)} steps completed")
    print("="*60)
    
    if completed == len(steps):
        print("\n🎉 Installation complete! You're ready to go!")
        print("\n📖 For detailed docs, see: CPU_OPTIMIZATION_GUIDE.md")
    else:
        print("\n⚠️  Some steps failed. Please check the errors above.")
        print("You may need to install dependencies manually.")

if __name__ == "__main__":
    main()
