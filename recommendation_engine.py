# recommendation_engine.py
from typing import List, Set, Dict
from course_database import Course, COURSES

def normalize_list(items):
    return [item.strip().lower() for item in items if item.strip()]

def score_course(course: Course, user_skills: Set[str], level: str, domain_pref: str):
    """Score a course based on user's skills and preferences"""
    score = 0
    matched_skills = set(course.skills).intersection(user_skills)
    
    # Skill match (most important)
    score += len(matched_skills) * 3
    
    # Difficulty match
    if course.difficulty == level:
        score += 2
    elif level == "beginner" and course.difficulty == "intermediate":
        score += 1  # Some flexibility
    
    # Domain match
    if domain_pref != "any":
        if course.domain == domain_pref:
            score += 3
    
    # Prerequisites match (bonus)
    prereq_met = all(p in user_skills for p in course.prerequisites)
    if prereq_met:
        score += 2
    
    # Calculate percentage
    total_possible = (len(course.skills) * 3) + 2 + 3 + 2
    match_percentage = round((score / total_possible) * 100, 1) if total_possible > 0 else 0
    
    return {
        "course": course,
        "score": score,
        "percentage": match_percentage,
        "matched_skills": matched_skills,
        "prerequisites_met": prereq_met,
        "missing_skills": set(course.skills) - user_skills
    }

def recommend_courses(user_skills: Set[str], level: str, domain_pref: str, limit: int = 10):
    """Get top matching courses"""
    recommendations = []
    
    for course in COURSES:
        result = score_course(course, user_skills, level, domain_pref)
        if result["score"] > 0:
            recommendations.append(result)
    
    # Sort by score descending
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations[:limit]

def generate_learning_path(user_skills: Set[str], goal: str, level: str):
    """Generate a structured learning path with milestones"""
    # Get recommendations for the goal domain
    domain = goal.lower()
    if "web" in domain or "website" in domain:
        domain_pref = "web"
    elif "machine learning" in domain or "ml" in domain:
        domain_pref = "ml"
    elif "ai" in domain or "artificial" in domain:
        domain_pref = "ai"
    elif "cyber" in domain or "security" in domain:
        domain_pref = "cybersecurity"
    elif "cloud" in domain:
        domain_pref = "cloud"
    elif "data" in domain or "analytics" in domain:
        domain_pref = "data"
    elif "iot" in domain:
        domain_pref = "iot"
    else:
        domain_pref = "any"
    
    recommendations = recommend_courses(user_skills, level, domain_pref, limit=12)
    
    # Group into months (3 courses per month)
    roadmap = []
    for i in range(0, len(recommendations), 3):
        month_num = i // 3 + 1
        month_courses = recommendations[i:i+3]
        roadmap.append({
            "month": month_num,
            "title": f"Month {month_num}: Building Core Skills",
            "courses": month_courses
        })
    
    return {
        "goal": goal,
        "domain": domain_pref,
        "current_skills": list(user_skills),
        "total_courses": len(recommendations),
        "roadmap": roadmap,
        "skill_gap": get_skill_gap(user_skills, recommendations)
    }

def get_skill_gap(user_skills: Set[str], recommendations: List[Dict]) -> Dict:
    """Identify missing skills across all recommended courses"""
    all_required = set()
    for rec in recommendations:
        all_required.update(rec["course"].skills)
    
    missing = all_required - user_skills
    
    # Count frequency of missing skills
    from collections import Counter
    skill_freq = Counter()
    for rec in recommendations:
        for skill in rec["missing_skills"]:
            skill_freq[skill] += 1
    
    return {
        "missing_skills": list(missing),
        "skill_frequency": dict(skill_freq.most_common(10))
    }