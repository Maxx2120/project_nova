
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"GET / status: {response.status_code}")
    except Exception as e:
        print(f"GET / failed: {e}")

def test_chat():
    try:
        # Assuming authentication is required or skipped based on implementation.
        # Looking at chat.py, it uses `Depends(auth.get_current_user)`.
        # I need a valid token. This is going to be tricky without creating a user first.
        # But wait, does the endpoint enforce auth? Yes: `current_user: models.User = Depends(auth.get_current_user)`
        print("Chat requires auth")
    except Exception as e:
        print(f"Chat check failed: {e}")

if __name__ == "__main__":
    test_root()
