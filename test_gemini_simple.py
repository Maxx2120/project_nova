import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {bool(api_key)}")

try:
    print("Initializing Client...")
    genai.configure(api_key=api_key)
    
    print("Generating content...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content('Hello, are you working?')
    
    print("\nSuccess!")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
