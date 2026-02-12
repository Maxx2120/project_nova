#!/usr/bin/env python3
"""
Gemini API Setup Verification Script
Checks if everything is configured correctly for Gemini API usage
"""

import os
import sys
from pathlib import Path

def check_gemin_setup():
    """Check Gemini API setup"""
    print("\n" + "="*60)
    print("[*] GEMINI API SETUP VERIFICATION")
    print("="*60)
    
    # Check 1: API Key
    print("\n[1] Checking Gemini API Key...")
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"    [+] GEMINI_API_KEY found: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("    [-] GEMINI_API_KEY not set in environment")
        print("       Fix: Set environment variable or create .env file")
    
    # Check 2: .env file
    print("\n[2] Checking .env file...")
    env_file = Path(".env")
    if env_file.exists():
        print(f"    [+] .env file exists: {env_file.absolute()}")
        with open(env_file) as f:
            content = f.read()
            if "GEMINI_API_KEY" in content:
                print("    [+] GEMINI_API_KEY defined in .env")
            else:
                print("    [-] GEMINI_API_KEY not in .env file")
    else:
        print("    [~] .env file not found (using environment variables)")
    
    # Check 3: .env.example
    print("\n[3] Checking .env.example...")
    if Path(".env.example").exists():
        print("    [+] .env.example found (reference template available)")
    
    # Check 4: .gitignore
    print("\n[4] Checking .gitignore...")
    gitignore = Path(".gitignore")
    if gitignore.exists():
        with open(gitignore) as f:
            content = f.read()
            if ".env" in content:
                print("    [+] .env properly ignored in Git")
            else:
                print("    [-] .env not in .gitignore (security risk!)")
    
    # Check 5: Requirements
    print("\n[5] Checking requirements.txt...")
    with open("requirements.txt") as f:
        content = f.read()
        if "google-genai" in content:
            print("    [+] google-genai in requirements.txt")
        else:
            print("    [-] google-genai not in requirements.txt")
        if "python-dotenv" in content:
            print("    [+] python-dotenv in requirements.txt")
        else:
            print("    [-] python-dotenv not in requirements.txt")
    
    # Check 6: Import tests
    print("\n[6] Testing imports...")
    try:
        import google.genai
        print("    [+] google.genai imported successfully")
    except ImportError:
        print("    [-] google.genai not installed - Run: pip install google-genai")
    
    try:
        from dotenv import load_dotenv
        print("    [+] python-dotenv imported successfully")
    except ImportError:
        print("    [-] python-dotenv not installed - Run: pip install python-dotenv")
    
    try:
        from backend.model_manager import get_gemini_model
        print("    [+] Gemini model functions available")
    except Exception as e:
        print(f"    [-] Backend import error: {e}")
    
    # Check 7: Configuration
    print("\n[7] Configuration Summary...")
    print(f"    Project Root: {Path.cwd().absolute()}")
    print(f"    .env File: {env_file.absolute()} ({'exists' if env_file.exists() else 'not found'})")
    print(f"    API Key Set: {'Yes' if api_key else 'No'}")
    
    # Final status
    print("\n" + "="*60)
    if api_key:
        print("[+] READY! You can now start the app:")
        print("    python -m uvicorn backend.main:app --reload")
    else:
        print("[-] SETUP INCOMPLETE")
        print("    Steps to complete:")
        print("    1. Get API key: https://makersuite.google.com/app/apikey")
        print("    2. Create .env file with: GEMINI_API_KEY=your_key_here")
        print("    3. Run this script again to verify")
    print("="*60 + "\n")
    
    return bool(api_key)

if __name__ == "__main__":
    success = check_gemin_setup()
    sys.exit(0 if success else 1)
