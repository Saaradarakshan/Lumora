# test_pathpilot.py
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
    
    print("\nMissing Skills:")
    for skill in path['skill_gap']['missing_skills'][:5]:
        print(f"  - {skill}")
    
    # Test 2: Display first month
    if path['roadmap']:
        print("\nFirst Month Courses:")
        for rec in path['roadmap'][0]['courses']:
            print(f"  - {rec['course'].name} ({rec['percentage']}% match)")
    
    # Test 3: Test Gemini (optional)
    print("\n" + "=" * 60)
    print("🤖 Test 2: Gemini AI Integration")
    print("=" * 60)
    
    top_course = None
    if path['roadmap'] and path['roadmap'][0]['courses']:
        top_course = path['roadmap'][0]['courses'][0]['course']
    
    try:
        advice = generate_career_advice(test_skills, test_goal, test_level, top_course)
        print("\nGenerated Advice (first 500 chars):")
        print(advice[:500] + "...")
        print("\n✅ Gemini AI integration working!")
    except Exception as e:
        print(f"❌ Gemini AI error: {e}")
        print("Make sure GEMINI_API_KEY is set in environment")
    
    print("\n" + "=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_system()