# gemini_advisor.py
import os
import logging
from typing import Set, Optional
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger("lumora-advisor")
load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
FALLBACK_MODELS = ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"]

def generate_career_advice(user_skills: Set[str], goal: str, level: str, top_course=None) -> str:
    """Generate personalized career roadmap and advice for students."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return f"""# 🎯 Personalized Career Strategy & Learning Path

**Target Goal:** {goal}  
**Experience Level:** {level.title()}

### 1. Focus on Foundational Mastery
Start by strengthening your core competencies in **{goal}**. Complete foundational courses and practice hands-on exercises daily.

### 2. Build High-Impact Portfolio Projects
- Build 2-3 end-to-end projects demonstrating your skills.
- Document your codebase on GitHub and write clear README summaries.

### 3. Continuous Learning & Next Steps
- Follow structured milestones and practice interview problems regularly.
- Network with peers and participate in student tech communities.
"""

    skills_str = ", ".join(user_skills) if user_skills else "Not specified"
    course_name = getattr(top_course, "name", None) or (top_course if isinstance(top_course, str) else "Foundational Course")
    
    prompt = f"""
You are an expert career counselor and learning path advisor helping students achieve their goals.

Student Profile:
- Goal: {goal}
- Current Skills: {skills_str}
- Experience Level: {level}
- Top Recommended Course: {course_name}

Please provide a comprehensive career and learning advice report including:

1. **Career Path Overview**
   - What the student needs to achieve their goal
   - Realistic timeline and expectations

2. **Skill Analysis**
   - Current strong skills
   - Key missing skills to prioritize next

3. **Learning Strategy & Portfolio Projects**
   - Practical study plan for their level
   - 2-3 real-world portfolio project ideas

4. **Career & Internship Opportunities**
   - Matching job roles and career paths
   - In-demand industry domains

5. **Action Plan & Next Steps**
   - Weekly learning plan
   - Encouraging advice to start immediately

Format the response with clear markdown headings, bold highlights, and motivating language. Do not mention model names or internal instructions.
"""
    
    models_to_try = [DEFAULT_MODEL] + [m for m in FALLBACK_MODELS if m != DEFAULT_MODEL]
    last_error = None

    for m_name in models_to_try:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = e
            logger.warning(f"Model {m_name} failed: {e}")
            continue

    logger.error(f"Failed to generate advice: {last_error}")
    return f"""# 🎯 Career Roadmap & Action Plan

**Target Goal:** {goal}  
**Experience Level:** {level.title()}

### 1. Core Learning Strategy
Begin with your top recommended course: **{course_name}**. Focus on practical problem solving and building foundational confidence.

### 2. Priority Skills to Master Next
Review your skill gap breakdown and prioritize the highest-impact missing skills.

### 3. Portfolio Building
Develop practical projects showcasing your skills and push them to your public portfolio.
"""