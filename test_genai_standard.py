import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {bool(api_key)}")

try:
    print("Configuring GenAI...")
    genai.configure(api_key=api_key)
    
    print("Initializing Model...")
    model = genai.GenerativeModel('gemini-pro')
    
    print("Generating content...")
    response = model.generate_content('Hello, are you working?')
    
    print("\nSuccess!")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
