import httpx
import asyncio
import os

BASE_URL = "http://127.0.0.1:8000"

async def test_endpoints():
    print(f"Testing endpoints at {BASE_URL}...")
    headers = {}
    
    async with httpx.AsyncClient() as client:
        # 1. Test Root
        try:
            response = await client.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("✅ Root endpoint: OK")
            else:
                print(f"❌ Root endpoint: Failed {response.status_code}")
        except Exception as e:
            print(f"❌ Root endpoint: Connection Error {e}")
            return

        # 2. Register/Login
        email = "tester_final@example.com"
        password = "password123"
        print("\nTesting Auth...")
        
        # Register
        await client.post(f"{BASE_URL}/api/auth/register", json={
            "username": "tester_final", "email": email, "password": password
        })
        
        # Login
        response = await client.post(f"{BASE_URL}/api/auth/token", json={
            "email": email, "password": password
        })
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print(f"✅ Auth: Login Success")
        else:
            print(f"❌ Auth: Login Failed {response.text}")
            return

        # 3. Test Chat
        print("\nTesting Chat...")
        try:
            # We use a short timeout because we just want to know if it connects to Ollama/Endpoint
            response = await client.post(f"{BASE_URL}/api/chat", json={
                "message": "Hi", "model": "mistral"
            }, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                print(f"✅ Chat: Success (Response: {response.json().get('message')})")
            else:
                print(f"⚠️ Chat: Error {response.status_code} - {response.text}")
        except Exception as e:
             print(f"⚠️ Chat: Timeout or Error (common if Ollama is slow): {e}")

        # 4. Test Image Generation (Fallback Check)
        print("\nTesting Image Gen...")
        try:
            response = await client.post(f"{BASE_URL}/api/image/generate", json={
                "prompt": "Test Prompt"
            }, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                 print("✅ Image Gen: Success (Fallback/Real)")
            else:
                 print(f"❌ Image Gen: Failed {response.status_code} - {response.text}")
        except Exception as e:
             print(f"❌ Image Gen: Error {e}")

        # 5. Test Video Upload
        print("\nTesting Video Upload...")
        try:
            # Create dummy file
            with open("test_vid.txt", "wb") as f:
                f.write(b"dummy video content")

            # Prepare file for upload
            # We open it, use it in the request, and then we MUST close it before deletion
            
            # Using a context manager for the file inside the request is tricky with httpx shorthand
            # So we open, read, close, create a bytes buffer to send
            
            with open("test_vid.txt", "rb") as f:
                file_content = f.read()
                
            files = {'file': ('test_vid.mp4', file_content, 'video/mp4')}
            
            response = await client.post(f"{BASE_URL}/api/video/upload", files=files, headers={'Authorization': token})
            
            if response.status_code == 200:
                task_id = response.json()['id']
                print(f"✅ Video Upload: Success (Task ID: {task_id})")
                
                # Test Process (Expected to be 500 because it's a dummy file, but validates endpoint hit)
                print("Testing Video Process Endpoint Reachability...")
                resp_proc = await client.post(f"{BASE_URL}/api/video/process/{task_id}", json={"prompt": "bw"}, headers={'Authorization': token})
                
                if resp_proc.status_code in [200, 500]: 
                     print(f"✅ Video Process: Endpoint Reachable (Status: {resp_proc.status_code})")
                else:
                     print(f"❌ Video Process: Unreachable {resp_proc.status_code}")
            else:
                print(f"❌ Video Upload: Failed {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Video: Error {e}")
        finally:
            if os.path.exists("test_vid.txt"):
                 try:
                    os.remove("test_vid.txt")
                 except:
                    pass

if __name__ == "__main__":
    asyncio.run(test_endpoints())
