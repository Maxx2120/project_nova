import requests
import random
import string
import time

BASE_URL = "http://127.0.0.1:8000"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

username = f"user_{random_string()}"
email = f"{username}@example.com"
password = "password123"

print(f"1. Registering user: {username}")
try:
    resp = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    print(f"   Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"   Error: {resp.text}")
        exit(1)
except Exception as e:
    print(f"   Failed to connect: {e}")
    exit(1)

print("2. Logging in...")
# The endpoint is /token and expects JSON with UserLogin schema (email, password)
resp = requests.post(f"{BASE_URL}/api/auth/token", json={
    "email": email,
    "password": password
})

print(f"   Status: {resp.status_code}")
if resp.status_code != 200:
    print(f"   Error: {resp.text}")
    exit(1)

token = resp.json().get("access_token")
print(f"   Token obtained: {token[:10]}...")

headers = {"Authorization": f"Bearer {token}"}

print("3. Testing Chat (default model handling)...")
payload = {"message": "Hello, explain quantum physics in 5 words."}
resp = requests.post(f"{BASE_URL}/api/chat", json=payload, headers=headers)
print(f"   Status: {resp.status_code}")
print(f"   Response: {resp.text}")

if resp.status_code == 200:
    print("\nSUCCESS! Chat is working.")
else:
    print("\nFAILED.")
