# test_gemini.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file")
    print("Please create .env file with: GEMINI_API_KEY=your_key_here")
    exit(1)

# Configure Gemini
genai.configure(api_key=API_KEY)

# ✅ UPDATED: Use newer model
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-pro"

try:
    response = model.generate_content("Say hello in one sentence.")
    print("✅ Gemini is working!")
    print("Response:", response.text)
except Exception as e:
    print("❌ Error:", e)
    print("Check your API key and internet connection.")