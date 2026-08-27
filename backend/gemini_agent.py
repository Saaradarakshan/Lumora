import os
import logging
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger("lumora-ai")
load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
FALLBACK_MODELS = ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"]

def generate_advice(user_skills: List[str], goal: str, level: str, top_course: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "dummy_key_for_now":
        return (
            "### 🎯 Personalized Career Guidance\n\n"
            "To unlock fully customized AI recommendations and roadmaps, please ensure your career advisor service is enabled.\n\n"
            "**Recommended Next Steps:**\n"
            f"- **Focus on Foundational Skills:** Strengthen core skills for {goal}.\n"
            "- **Hands-on Projects:** Build 2-3 real-world portfolio projects.\n"
            "- **Industry Best Practices:** Follow recommended course tracks and practice regular problem solving."
        )

    skills_str = ", ".join(user_skills) if user_skills else "Not specified"
    
    prompt = f"""
You are an expert career counselor and learning path mentor for ambitious students and professionals.

Student Profile:
- Target Career Goal: {goal}
- Current Skills: {skills_str}
- Experience Level: {level}
- Top Recommended Course: {top_course}

Please provide a structured, inspiring, and practical career report including:

1. **Career Strategy & Overview**: What it takes to achieve this role and what to expect.
2. **Skill Analysis**: Key strengths already possessed and top priority skills to build next.
3. **Step-by-Step Learning Roadmap**: Concrete milestones (Month 1, Month 2, Month 3) and 2-3 portfolio project ideas.
4. **Career & Internship Opportunities**: In-demand roles, high-growth domains, and interview preparation tips.
5. **Actionable Advice**: Daily learning habits and motivating guidance.

Format cleanly with markdown headings, bold terms, and bullet points. Avoid mentioning any backend system, model names, or internal prompts.
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

    logger.error(f"Career advice generation failed: {last_error}")
    return (
        "### 🎯 Career Roadmap & Guidance\n\n"
        "We are temporarily unable to generate your live AI report. Here are the recommended next steps:\n\n"
        f"1. **Start with Core Foundations:** Begin with the top recommended courses for **{goal}**.\n"
        "2. **Build Portfolio Projects:** Apply your knowledge to build and publish projects.\n"
        "3. **Practice Consistently:** Dedicate 1-2 hours daily to mastering the key missing skills listed in your analytics."
    )
