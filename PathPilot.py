"""
=========================================================
PATH PILOT
AI Internship Recommendation System
Powered by Google Gemini
=========================================================
"""

from dataclasses import dataclass
from typing import List, Set
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =========================================================
# GEMINI CONFIGURATION
# =========================================================

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file. Please add it.")

genai.configure(api_key=API_KEY)

# model = genai.GenerativeModel("gemini-2.5-flash")
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-pro"

# =========================================================
# DATA STRUCTURE
# =========================================================

@dataclass
class Internship:
    title: str
    company: str
    skills: List[str]
    level: str
    domain: str
    mode: str

# =========================================================
# INTERNSHIP DATABASE
# =========================================================

INTERNSHIPS = [

    Internship(
        "Python Web Development Intern",
        "TechHive Solutions",
        ["python","html","css","django","git"],
        "beginner",
        "web",
        "remote"
    ),

    Internship(
        "Frontend Web Intern",
        "PixelCraft Studio",
        ["html","css","javascript","react"],
        "beginner",
        "web",
        "hybrid"
    ),

    Internship(
        "Machine Learning Intern",
        "DataSense Analytics",
        ["python","pandas","numpy","ml","scikit-learn"],
        "intermediate",
        "ml",
        "remote"
    ),

    Internship(
        "AI Research Assistant Intern",
        "NeuroLabs AI",
        ["python","ml","deep learning","pytorch"],
        "advanced",
        "ai",
        "onsite"
    ),

    Internship(
        "Cybersecurity Analyst Intern",
        "SecureNet Systems",
        ["linux","networking","python","cybersecurity"],
        "intermediate",
        "cybersecurity",
        "onsite"
    ),

    Internship(
        "Cloud & DevOps Intern",
        "CloudBridge",
        ["linux","docker","aws","git"],
        "intermediate",
        "cloud",
        "hybrid"
    ),

    Internship(
        "IoT & Embedded Systems Intern",
        "SmartThings Labs",
        ["iot","arduino","sensors","python"],
        "beginner",
        "iot",
        "onsite"
    ),

    Internship(
        "Data Analytics Intern",
        "InsightPoint",
        ["excel","sql","python","pandas"],
        "beginner",
        "ml",
        "remote"
    ),

    Internship(
        "Backend Developer Intern",
        "StackFlow Technologies",
        ["python","django","rest api","databases"],
        "intermediate",
        "web",
        "remote"
    ),

    Internship(
        "General Tech Intern",
        "BrightStart Innovations",
        ["communication","teamwork","python"],
        "beginner",
        "general",
        "hybrid"
    )

]
# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize_list(items):
    return [item.strip().lower() for item in items if item.strip()]


def get_user_input():

    print("=" * 55)
    print("        PATH PILOT - AI Internship Advisor")
    print("=" * 55)

    raw_skills = input(
        "\nEnter your skills (comma separated):\n> "
    )

    user_skills = set(normalize_list(raw_skills.split(",")))

    level = input(
        "\nExperience (beginner/intermediate/advanced):\n> "
    ).strip().lower()

    domain = input(
        "\nPreferred Domain (web/ml/ai/cybersecurity/cloud/iot/any):\n> "
    ).strip().lower()

    mode = input(
        "\nPreferred Mode (remote/onsite/hybrid/any):\n> "
    ).strip().lower()

    return user_skills, level, domain, mode


# =========================================================
# SCORING ENGINE
# =========================================================

def score_internship(internship, user_skills, level, domain_pref, mode_pref):

    score = 0

    matched_skills = set(internship.skills).intersection(user_skills)

    score += len(matched_skills) * 2

    if internship.level == level:
        score += 2

    elif level == "beginner" and internship.level == "intermediate":
        score += 1

    if domain_pref != "any":

        if internship.domain == domain_pref:
            score += 3

    if mode_pref != "any":

        if internship.mode == mode_pref:
            score += 1

    total_possible = (
        len(internship.skills) * 2
        + 2
        + 3
        + 1
    )

    match_percentage = round(
        (score / total_possible) * 100,
        1
    )

    return score, match_percentage, matched_skills


# =========================================================
# RECOMMENDATION ENGINE
# =========================================================

def recommend_internships(
    user_skills,
    level,
    domain_pref,
    mode_pref
):

    recommendations = []

    for internship in INTERNSHIPS:

        score, percent, matched = score_internship(
            internship,
            user_skills,
            level,
            domain_pref,
            mode_pref
        )

        if score > 0:

            recommendations.append({

                "internship": internship,

                "score": score,

                "percentage": percent,

                "matched_skills": matched

            })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations


# =========================================================
# DISPLAY RECOMMENDATIONS
# =========================================================

def display_recommendations(results):

    print("\n")
    print("=" * 60)
    print("TOP MATCHING INTERNSHIPS")
    print("=" * 60)

    for i, item in enumerate(results[:5], start=1):

        internship = item["internship"]

        print(f"\n{i}. {internship.title}")
        print(f"Company : {internship.company}")
        print(f"Domain  : {internship.domain.upper()}")
        print(f"Level   : {internship.level.title()}")
        print(f"Mode    : {internship.mode.title()}")

        print(f"Match   : {item['percentage']}%")

        if item["matched_skills"]:
            print(
                "Matched Skills:",
                ", ".join(item["matched_skills"])
            )

        else:
            print("Matched Skills: None")
# =========================================================
# AI SKILL GAP ANALYSIS
# =========================================================

def skill_gap_analysis(user_skills, internship):

    required = set(internship.skills)

    known = required.intersection(user_skills)

    missing = required - user_skills

    print("\n" + "="*60)
    print("SKILL GAP ANALYSIS")
    print("="*60)

    print("\nSkills You Already Have:")

    if known:

        for skill in sorted(known):
            print("✓", skill.title())

    else:
        print("None")

    print("\nSkills You Should Learn:")

    if missing:

        for skill in sorted(missing):
            print("•", skill.title())

    else:
        print("None! Excellent match.")
# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    user_skills, level, domain_pref, mode_pref = get_user_input()

    recommendations = recommend_internships(
        user_skills,
        level,
        domain_pref,
        mode_pref
    )

    if not recommendations:

        print("\nNo suitable internships found.")
        print("Try adding more skills like:")
        print("Python, SQL, HTML, CSS, Linux, Git")
        return

    display_recommendations(recommendations)

    top = recommendations[0]["internship"]

    skill_gap_analysis(user_skills, top)

    print("\n" + "=" * 60)

    use_ai = input(
        "Would you like Gemini AI Career Guidance? (yes/no): "
    ).strip().lower()

    if use_ai == "yes":

        print("\nGenerating AI Career Report...")
        print("Please wait...\n")

        report = generate_ai_advice(
            user_skills,
            level,
            domain_pref,
            recommendations
        )

        print("=" * 60)
        print("AI CAREER REPORT")
        print("=" * 60)
        print(report)

        save_report(report)

    else:

        print("\nThank you for using Path Pilot!")

    print("\n" + "=" * 60)
    print("Good Luck with Your Internship Journey!")
    print("=" * 60)
# =========================================================
# GEMINI AI CAREER ADVISOR
# =========================================================

def generate_ai_advice(user_skills, level, domain_pref, recommendations):

    if not recommendations:
        return "No recommendations available."

    top = recommendations[0]["internship"]

    prompt = f"""
You are an expert career counselor helping engineering students.

Student Profile

Skills:
{', '.join(user_skills)}

Experience Level:
{level}

Preferred Domain:
{domain_pref}

Recommended Internship

Title:
{top.title}

Company:
{top.company}

Required Skills:
{', '.join(top.skills)}

Work Mode:
{top.mode}

Please provide:

1. Why this internship suits the student.

2. Skills the student already has.

3. Skills the student is missing.

4. Three project ideas.

5. A 30-day learning roadmap.

6. Five interview questions.

7. Resume improvement tips.

8. End with an encouraging career tip.

Format everything nicely with headings and bullet points.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Gemini AI Error:\n{e}"
# =========================================================
# SAVE REPORT
# =========================================================

def save_report(report):

    choice = input("\nWould you like to save this report? (yes/no): ").lower()

    if choice == "yes":

        with open("Career_Report.txt", "w", encoding="utf-8") as file:

            file.write(report)

        print("\nReport saved successfully as Career_Report.txt")

if __name__ == "__main__":
    main()
