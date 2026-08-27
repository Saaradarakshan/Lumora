# test_pathpilot.py
import sys
import os
from dotenv import load_dotenv

# Ensure console supports UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

from recommendation_engine import recommend_courses, generate_learning_path, normalize_list
from gemini_advisor import generate_career_advice
from course_database import COURSES

def test_system():
    print("=" * 60)
    print("🧪 Testing PathPilot AI System")
    print("=" * 60)
    
    # Test data
    test_skills = {"python", "sql", "html", "css"}
    test_goal = "Data Science"
    test_level = "beginner"
    
    print(f"\nTest Profile:")
    print(f"  Skills: {', '.join(test_skills)}")
    print(f"  Goal: {test_goal}")
    print(f"  Level: {test_level}")
    
    # Test 1: Generate learning path
    print("\n" + "=" * 60)
    print("📚 Test 1: Generate Learning Path")
    print("=" * 60)
    
    path = generate_learning_path(test_skills, test_goal, test_level)
    
    print(f"\nGoal: {path['goal']}")
    print(f"Domain: {path['domain']}")
    print(f"Total Courses: {path['total_courses']}")
    print(f"Roadmap: {len(path['roadmap'])} months")
    
    assert path['total_courses'] > 0, "No courses found for learning path"
    assert len(path['roadmap']) > 0, "No roadmap generated"
    
    print("\nMissing Skills:")
    for skill in path['skill_gap']['missing_skills'][:5]:
        print(f"  - {skill}")
    
    # Test 2: Display first month
    if path['roadmap']:
        print("\nFirst Month Courses:")
        for rec in path['roadmap'][0]['courses']:
            print(f"  - {rec['course'].name} ({rec['percentage']}% match)")
    
    # Test 3: Test Gemini AI
    print("\n" + "=" * 60)
    print("🤖 Test 2: Gemini AI Integration")
    print("=" * 60)
    
    top_course = None
    if path['roadmap'] and path['roadmap'][0]['courses']:
        top_course = path['roadmap'][0]['courses'][0]['course']
    
    advice = generate_career_advice(test_skills, test_goal, test_level, top_course)
    if "Error connecting to Gemini AI" in advice or "GEMINI_API_KEY not found" in advice:
        print("\n⚠️ Gemini AI warning/error returned:")
        print(advice)
    else:
        print("\nGenerated Advice (preview):")
        preview = advice[:400] + ("..." if len(advice) > 400 else "")
        print(preview)
        print("\n✅ Gemini AI integration working successfully!")
    
    print("\n" + "=" * 60)
    print("✅ All Tests Finished!")
    print("=" * 60)

if __name__ == "__main__":
    test_system()