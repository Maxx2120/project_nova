
import requests
import sys

def check_ollama():
    try:
        url = "http://localhost:11434/api/tags"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"Ollama is online. Found {len(models)} models.")
            for m in models:
                print(f" - {m['name']}")
            return True
        else:
            print(f"Ollama is online but returned {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Ollama is NOT reachable at localhost:11434. Is it running?")
        return False
    except Exception as e:
        print(f"Error checking Ollama: {e}")
        return False

def check_sd():
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
    except ImportError:
        print("PyTorch NOT installed.")

if __name__ == "__main__":
    check_ollama()
    check_sd()
