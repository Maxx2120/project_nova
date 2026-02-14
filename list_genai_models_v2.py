import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

with open("valid_models.txt", "w", encoding="utf-8") as f:
    f.write("Fetching models...\n")
    try:
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"- {m.name}\n")
                found = True
        if not found:
            f.write("No models found with generateContent capability.\n")
    except Exception as e:
        f.write(f"Error listing models: {e}\n")
