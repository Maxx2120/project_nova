
import sys
import importlib

def check_import(module_name, pip_name=None):
    if pip_name is None:
        pip_name = module_name
    try:
        importlib.import_module(module_name)
        print(f"✅ {pip_name} is installed.")
        return True
    except ImportError:
        print(f"❌ {pip_name} is MISSING.")
        return False

def check_gpu():
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU is available: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️ GPU is NOT available (using CPU). Image generation might be slow.")
    except ImportError:
        pass

def main():
    print("Checking dependencies...")
    
    deps = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("sqlalchemy", "sqlalchemy"),
        ("diffusers", "diffusers"),
        ("transformers", "transformers"),
        ("torch", "torch"),
        ("PIL", "Pillow"),
        ("ollama", "ollama"),
    ]
    
    missing = []
    for module, pip_name in deps:
        if not check_import(module, pip_name):
            missing.append(pip_name)
    
    check_gpu()
    
    if missing:
        print("\n❌ Some dependencies are missing. Please run:")
        print(f"pip install {' '.join(missing)}")
        sys.exit(1)
    else:
        print("\n✅ All dependencies are installed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
