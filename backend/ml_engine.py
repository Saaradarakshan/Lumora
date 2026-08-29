import json
from typing import List, Set

def parse_skills(raw_skills) -> Set[str]:
    """Parse skill data safely whether it is a JSON string, list, or comma-separated string."""
    if not raw_skills:
        return set()
    if isinstance(raw_skills, (list, set)):
        return {str(s).strip().lower() for s in raw_skills if str(s).strip()}
    if isinstance(raw_skills, str):
        try:
            parsed = json.loads(raw_skills)
            if isinstance(parsed, list):
                return {str(s).strip().lower() for s in parsed if str(s).strip()}
        except Exception:
            pass
        return {s.strip().lower() for s in raw_skills.split(",") if s.strip()}
    return set()

def score_item(item, user_skills: Set[str], level: str, domain_pref: str, is_internship=False):
    """
    Unified scoring engine for courses and internships.
    """
    score = 0
    item_skills = parse_skills(getattr(item, "skills", ""))
    matched_skills = item_skills.intersection(user_skills)
    
    # Skill match (heaviest weight)
    score += len(matched_skills) * 3
    
    # Difficulty/Level match
    item_level = (item.level if is_internship else item.difficulty) or ""
    item_level_clean = item_level.strip().lower()
    user_level_clean = level.strip().lower()
    
    if item_level_clean == user_level_clean:
        score += 2
    elif user_level_clean == "beginner" and item_level_clean == "intermediate":
        score += 1
        
    # Domain match
    item_domain = (getattr(item, "domain", "") or "").strip().lower()
    domain_pref_clean = (domain_pref or "any").strip().lower()
    if domain_pref_clean != "any" and item_domain == domain_pref_clean:
        score += 3
        
    total_possible = (len(item_skills) * 3) + 2 + 3
    match_percentage = round((score / total_possible) * 100, 1) if total_possible > 0 else 0
    
    return {
        "item": item,
        "score": score,
        "percentage": match_percentage,
        "matched_skills": sorted(list(matched_skills))
    }

def get_recommendations(items: List, user_skills: List[str], level: str, domain_pref: str, is_internship=False):
    user_skills_set = {s.strip().lower() for s in user_skills if s and s.strip()}
    
    recommendations = []
    for item in items:
        result = score_item(item, user_skills_set, level, domain_pref, is_internship)
        if result["score"] > 0:
            recommendations.append(result)
            
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations[:10]
