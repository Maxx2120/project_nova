import httpx
import asyncio
import os

BASE_URL = "http://localhost:8000"

async def test_endpoints():
    print(f"Testing endpoints at {BASE_URL}...")
    
    async with httpx.AsyncClient() as client:
        # 1. Test Root
        try:
            response = await client.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("✅ Root endpoint Check: OK")
            else:
                print(f"❌ Root endpoint Check: Failed with {response.status_code}")
        except Exception as e:
            print(f"❌ Root endpoint Check: Failed with error {e}")
            return

        # 2. Register
        username = "testuser_script"
        email = "testuser_script@example.com"
        password = "password123"
        
        print("\nTesting Registration...")
        response = await client.post(f"{BASE_URL}/api/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            print("✅ Registration: success")
        elif response.status_code == 400 and "already registered" in response.text:
            print("✅ Registration: User already exists (OK)")
        else:
            print(f"❌ Registration: Failed {response.text}")
            
        # 3. Login
        print("\nTesting Login...")
        response = await client.post(f"{BASE_URL}/api/auth/token", json={
            "email": email,
            "password": password
        })
        
        token = None
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ Login: Success, token received")
        else:
            print(f"❌ Login: Failed {response.text}")
            return

        headers = {"Authorization": f"Bearer {token}"}

        # 4. Test Chat
        print("\nTesting Chat Endpoint...")
        try:
            response = await client.post(f"{BASE_URL}/api/chat/chat", json={
                "message": "Hello AI",
                "model": "mistral" 
            }, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                print(f"✅ Chat: Success. Response: {response.json().get('message')[:50]}...")
            else:
                print(f"⚠️ Chat: Endpoint reachable but returned error (likely Ollama not running): {response.text}")
        except httpx.ReadTimeout:
             print("⚠️ Chat: Timeout (Ollama/Server might be slow)")
        except Exception as e:
             print(f"⚠️ Chat: Error {e}")

        # 5. Test Image Generation (Expect 500 or timeout if model not loaded, but endpoint should be hit)
        print("\nTesting Image Generation Endpoint...")
        try:
            response = await client.post(f"{BASE_URL}/api/image/generate", json={
                "prompt": "A beautiful sunset",
                "negative_prompt": ""
            }, headers=headers, timeout=5.0)
            
            if response.status_code == 200:
                 print("✅ Image Gen: Success")
            else:
                 print(f"⚠️ Image Gen: Failed as expected (No model loaded): {response.status_code}") # This is expected without GPU/Model
        except Exception as e:
             print(f"⚠️ Image Gen: Error {e}")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
