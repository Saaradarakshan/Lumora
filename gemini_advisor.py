# gemini_advisor.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Set, Optional

# Load environment variables
load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file. Please add it.")

genai.configure(api_key=API_KEY)

# ✅ UPDATED: Use newer model
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-pro"

def generate_career_advice(user_skills: Set[str], goal: str, level: str, top_course=None):
    """Generate personalized career advice using Gemini"""
    
    skills_str = ", ".join(user_skills) if user_skills else "Not specified"
    
    prompt = f"""
You are an expert career counselor and learning path advisor.

Student Profile:
- Goal: {goal}
- Current Skills: {skills_str}
- Experience Level: {level}
- Top Recommended Course: {top_course.name if top_course else "Not specified"}

Please provide a comprehensive career and learning advice report including:

1. **Career Path Overview**
   - Explain what the student needs to achieve their goal
   - Realistic timeline and expectations

2. **Skill Analysis**
   - Skills they already have
   - Critical missing skills
   - Recommended order to learn missing skills

3. **Learning Strategy**
   - Study tips for their experience level
   - Recommended projects to build portfolio
   - Online resources and communities to join

4. **Career Opportunities**
   - Job roles matching this path
   - Expected salary ranges
   - Companies hiring in this space

5. **Motivation & Next Steps**
   - Daily/weekly study plan
   - Milestones to celebrate
   - Encouraging advice

Format the response with clear headings, bullet points, and motivational language.
Keep it practical and actionable.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"""
# AI Career Report (Error)

⚠️ **Error connecting to Gemini AI**

Error details: {str(e)}

Please check:
1. Your API key is correct in .env file
2. You have internet connection
3. The Gemini API is accessible

**In the meantime:**

Continue with your learning path. Focus on:
- Starting with foundational courses
- Building projects alongside learning
- Joining communities related to your goal

Good luck with your learning journey!
"""