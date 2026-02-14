import httpx
import asyncio
import os

BASE_URL = "http://127.0.0.1:8000"

async def test_endpoints():
    with open("test_run.log", "w", encoding="utf-8") as log:
        def log_print(msg):
            print(msg)
            log.write(msg + "\n")
            
        log_print(f"Testing endpoints at {BASE_URL}...")
    headers = {}
    
    async with httpx.AsyncClient() as client:
        # 1. Test Root
        try:
            response = await client.get(f"{BASE_URL}/")
            if response.status_code == 200:
                with open("test_run.log", "a", encoding="utf-8") as log: log.write("Root endpoint: OK\n")
            else:
                with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Root endpoint: Failed {response.status_code}\n")
        except Exception as e:
            with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Root endpoint: Connection Error {e}\n")
            return

        # 2. Register/Login
        email = "tester_final@example.com"
        password = "password123"
        with open("test_run.log", "a", encoding="utf-8") as log: log.write("\nTesting Auth...\n")
        
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
            with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Auth: Login Success\n")
        else:
            with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Auth: Login Failed {response.text}\n")
            return

        # 3. Test Chat
        with open("test_run.log", "a", encoding="utf-8") as log: log.write("\nTesting Chat...\n")
        try:
            # We use a short timeout because we just want to know if it connects to Ollama/Endpoint
            response = await client.post(f"{BASE_URL}/api/chat", json={
                "message": "Hi", "model": "gemini-2.5-flash"
            }, headers=headers, timeout=20.0)
            
            if response.status_code == 200:
                with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Chat: Success (Response: {response.json().get('message')})\n")
            else:
                with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Chat: Error {response.status_code} - {response.text}\n")
        except Exception as e:
             with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Chat: Timeout or Error (common if Ollama is slow): {e}\n")

        # 4. Test Image Generation (Fallback Check)
        with open("test_run.log", "a", encoding="utf-8") as log: log.write("\nTesting Image Gen...\n")
        try:
            response = await client.post(f"{BASE_URL}/api/image/generate", json={
                "prompt": "Test Prompt"
            }, headers=headers, timeout=20.0)
            
            if response.status_code == 200:
                 with open("test_run.log", "a", encoding="utf-8") as log: log.write("Image Gen: Success (Fallback/Real)\n")
            else:
                 with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Image Gen: Failed {response.status_code} - {response.text}\n")
        except Exception as e:
             with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Image Gen: Error {e}\n")

        # 5. Test Video Upload
        with open("test_run.log", "a", encoding="utf-8") as log: log.write("\nTesting Video Upload...\n")
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
                with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Video Upload: Success (Task ID: {task_id})\n")
                
                # Test Process (Expected to be 500 because it's a dummy file, but validates endpoint hit)
                with open("test_run.log", "a", encoding="utf-8") as log: log.write("Testing Video Process Endpoint Reachability...\n")
                resp_proc = await client.post(f"{BASE_URL}/api/video/process/{task_id}", json={"prompt": "bw"}, headers={'Authorization': token})
                
                if resp_proc.status_code in [200, 500]: 
                     with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Video Process: Endpoint Reachable (Status: {resp_proc.status_code})\n")
                else:
                     with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Video Process: Unreachable {resp_proc.status_code}\n")
            else:
                with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Video Upload: Failed {response.status_code} - {response.text}\n")
                
        except Exception as e:
            with open("test_run.log", "a", encoding="utf-8") as log: log.write(f"Video: Error {e}\n")
        finally:
            if os.path.exists("test_vid.txt"):
                 try:
                    os.remove("test_vid.txt")
                 except:
                    pass

if __name__ == "__main__":
    asyncio.run(test_endpoints())
