# test_gemini.py
import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Ensure console supports UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load environment variables
load_dotenv()

# Get API key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file")
    print("Please create .env file with: GEMINI_API_KEY=your_key_here")
    sys.exit(1)

# Configure Gemini
genai.configure(api_key=API_KEY)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

print(f"📡 Testing Gemini AI with model: {MODEL_NAME}...")

try:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content("Say hello and introduce yourself in one short sentence.")
    print("✅ Gemini is working!")
    print("Response:", response.text.strip())
except Exception as e:
    print("❌ Primary model failed, trying fallback model gemini-3.5-flash-lite...")
    try:
        fallback_model = genai.GenerativeModel("gemini-3.5-flash-lite")
        response = fallback_model.generate_content("Say hello in one short sentence.")
        print("✅ Gemini fallback model is working!")
        print("Response:", response.text.strip())
    except Exception as fallback_err:
        print("❌ Error:", fallback_err)
        print("Check your API key, model access, and internet connection.")
        sys.exit(1)