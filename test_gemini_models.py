import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models_to_try = [
    "gemini-1.5-flash",
    "gemini-pro",
    "gemini-1.5-pro"
]

print("Testing models...")
for model_name in models_to_try:
    print(f"\nTrying: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content('Hello')
        print(f" -> SUCCESS! Response: {response.text[:50]}...")
    except Exception as e:
        print(f" -> ERROR: {e}")
