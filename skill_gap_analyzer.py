# skill_gap_analyzer.py
from typing import List, Set, Dict
from collections import Counter

def analyze_skill_gap(user_skills: Set[str], required_skills: List[str]) -> Dict:
    """
    Analyze the gap between user's current skills and required skills.
    
    Args:
        user_skills: Set of skills the user already has
        required_skills: List of skills required for the goal
    
    Returns:
        Dictionary with gap analysis results
    """
    required_set = set(required_skills)
    
    # Find missing skills
    missing = required_set - user_skills
    
    # Find matched skills
    matched = required_set.intersection(user_skills)
    
    # Calculate percentages
    total_required = len(required_set)
    total_matched = len(matched)
    total_missing = len(missing)
    
    match_percentage = round((total_matched / total_required) * 100) if total_required > 0 else 0
    
    return {
        "required_skills": list(required_set),
        "current_skills": list(user_skills),
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "total_required": total_required,
        "total_matched": total_matched,
        "total_missing": total_missing,
        "match_percentage": match_percentage,
        "gap_percentage": 100 - match_percentage
    }

def get_learning_resources(missing_skills: List[str]) -> Dict[str, List[str]]:
    """
    Get recommended learning resources for missing skills.
    
    Args:
        missing_skills: List of skills to learn
    
    Returns:
        Dictionary mapping skills to resource recommendations
    """
    # Pre-defined resource mapping
    resource_mapping = {
        "python": [
            "Python for Everybody (Coursera)",
            "Automate the Boring Stuff (Book/Video)",
            "Codecademy Python Course"
        ],
        "sql": [
            "SQL for Data Science (Coursera)",
            "SQLZoo (Interactive Tutorial)",
            "LeetCode SQL Problems"
        ],
        "html": [
            "HTML & CSS (Codecademy)",
            "FreeCodeCamp HTML Course",
            "MDN Web Docs"
        ],
        "css": [
            "CSS Flexbox & Grid (CSS-Tricks)",
            "FreeCodeCamp CSS Course",
            "Tailwind CSS Docs"
        ],
        "javascript": [
            "JavaScript.info (Tutorial)",
            "FreeCodeCamp JavaScript Course",
            "Eloquent JavaScript (Book)"
        ],
        "react": [
            "React Official Tutorial",
            "Full Stack Open (React Section)",
            "Scrimba React Course"
        ],
        "django": [
            "Django Official Tutorial",
            "MDN Django Tutorial",
            "Django for Beginners (Book)"
        ],
        "ml": [
            "Andrew Ng ML Course (Coursera)",
            "Fast.ai Course",
            "Hands-On ML (Book)"
        ],
        "pandas": [
            "Pandas Official Documentation",
            "Kaggle Pandas Course",
            "Python for Data Analysis (Book)"
        ],
        "numpy": [
            "NumPy Quickstart Tutorial",
            "Kaggle NumPy Course",
            "Python Data Science Handbook"
        ],
        "deep learning": [
            "Deep Learning Specialization (Coursera)",
            "Fast.ai Deep Learning Course",
            "Deep Learning with Python (Book)"
        ],
        "linux": [
            "Linux Journey (Interactive)",
            "Linux Basics for Hackers (Book)",
            "OverTheWire Bandit"
        ],
        "networking": [
            "Cisco Networking Academy",
            "Network Fundamentals (Coursera)",
            "TCP/IP Illustrated (Book)"
        ],
        "cybersecurity": [
            "Cybersecurity Fundamentals (edX)",
            "CompTIA Security+ Course",
            "TryHackMe Tutorials"
        ],
        "docker": [
            "Docker Official Tutorial",
            "Docker Mastery (Udemy)",
            "Kubernetes in Action (Book)"
        ],
        "aws": [
            "AWS Cloud Practitioner Essentials",
            "AWS Certified Solutions Architect Course",
            "AWS Workshop Studios"
        ],
        "git": [
            "Git Official Tutorials",
            "Pro Git (Book)",
            "GitHub Learning Lab"
        ],
        "iot": [
            "IoT Fundamentals (Coursera)",
            "Arduino Project Hub",
            "Raspberry Pi Projects"
        ],
        "arduino": [
            "Arduino Official Tutorials",
            "Adafruit Learning System",
            "SparkFun Tutorials"
        ],
        "sensors": [
            "Sensor Fundamentals (Coursera)",
            "Building Sensor Networks",
            "IoT Sensor Projects"
        ]
    }
    
    resources = {}
    for skill in missing_skills:
        skill_lower = skill.lower().strip()
        if skill_lower in resource_mapping:
            resources[skill] = resource_mapping[skill_lower]
        else:
            # Generic recommendations for unknown skills
            resources[skill] = [
                f"Search for '{skill}' courses on Coursera/edX",
                f"Find YouTube tutorials for '{skill}'",
                f"Practice with '{skill}' projects on GitHub"
            ]
    
    return resources

def suggest_learning_priority(missing_skills: List[str], dependencies: Dict[str, List[str]] = None) -> List[str]:
    """
    Suggest priority order for learning missing skills.
    
    Args:
        missing_skills: List of skills to learn
        dependencies: Optional dictionary of skill dependencies
    
    Returns:
        List of skills in recommended learning order
    """
    if dependencies is None:
        # Define default skill dependencies (pre-requisites)
        dependencies = {
            "django": ["python", "html", "css"],
            "react": ["javascript", "html", "css"],
            "ml": ["python", "statistics"],
            "deep learning": ["python", "ml"],
            "docker": ["linux", "git"],
            "kubernetes": ["docker"],
            "pytorch": ["python", "ml"],
            "tensorflow": ["python", "ml"],
            "pandas": ["python"],
            "numpy": ["python"]
        }
    
    # Create a simple ordering (skills without dependencies first)
    skill_set = set(missing_skills)
    ordered = []
    
    # First pass: skills with no dependencies
    for skill in missing_skills:
        skill_lower = skill.lower().strip()
        has_deps = False
        for dep_skill, deps in dependencies.items():
            if dep_skill == skill_lower:
                has_deps = True
                # Check if all dependencies are in the required set
                deps_met = all(dep in skill_set for dep in deps)
                if deps_met:
                    if skill not in ordered:
                        ordered.append(skill)
                break
        if not has_deps:
            if skill not in ordered:
                ordered.append(skill)
    
    # Second pass: remaining skills (with unmet dependencies)
    for skill in missing_skills:
        if skill not in ordered:
            ordered.append(skill)
    
    return ordered