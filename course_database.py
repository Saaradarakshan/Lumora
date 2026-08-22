# course_database.py
from dataclasses import dataclass
from typing import List

@dataclass
class Course:
    name: str
    platform: str  # Coursera, edX, Udemy, YouTube
    skills: List[str]
    difficulty: str  # beginner, intermediate, advanced
    domain: str  # web, ml, ai, cybersecurity, cloud, iot, data, general
    duration: str  # "4 weeks", "2 months"
    prerequisites: List[str]
    url: str = ""  # Optional

# Expanded course database (repurposed from internships)
COURSES = [
    Course(
        "Python Programming Masterclass",
        "Udemy",
        ["python", "programming", "variables", "loops", "functions"],
        "beginner",
        "general",
        "4 weeks",
        []
    ),
    Course(
        "Web Development Bootcamp",
        "Coursera",
        ["html", "css", "javascript", "react"],
        "beginner",
        "web",
        "6 weeks",
        ["Python basics"]
    ),
    Course(
        "Machine Learning A-Z",
        "Udemy",
        ["python", "pandas", "numpy", "ml", "scikit-learn"],
        "intermediate",
        "ml",
        "8 weeks",
        ["Python", "Statistics basics"]
    ),
    Course(
        "Deep Learning Specialization",
        "Coursera",
        ["python", "ml", "deep learning", "pytorch", "tensorflow"],
        "advanced",
        "ai",
        "12 weeks",
        ["Machine Learning"]
    ),
    Course(
        "Cybersecurity Fundamentals",
        "edX",
        ["linux", "networking", "python", "cybersecurity"],
        "intermediate",
        "cybersecurity",
        "6 weeks",
        ["Networking basics", "Linux"]
    ),
    Course(
        "AWS Cloud Practitioner",
        "AWS",
        ["linux", "docker", "aws", "git", "cloud"],
        "intermediate",
        "cloud",
        "4 weeks",
        ["Linux"]
    ),
    Course(
        "Data Science with Python",
        "Coursera",
        ["excel", "sql", "python", "pandas", "data visualization"],
        "beginner",
        "data",
        "8 weeks",
        ["Python basics"]
    ),
    Course(
        "Django Web Framework",
        "Udemy",
        ["python", "django", "rest api", "databases"],
        "intermediate",
        "web",
        "6 weeks",
        ["Python", "Web basics"]
    ),
    Course(
        "IoT with Arduino",
        "edX",
        ["iot", "arduino", "sensors", "python"],
        "beginner",
        "iot",
        "4 weeks",
        ["Python basics"]
    ),
    Course(
        "Full Stack JavaScript",
        "Coursera",
        ["javascript", "react", "node.js", "mongodb", "express"],
        "intermediate",
        "web",
        "10 weeks",
        ["HTML", "CSS"]
    ),
    Course(
        "Statistics for Data Science",
        "edX",
        ["statistics", "probability", "data analysis"],
        "beginner",
        "data",
        "4 weeks",
        ["Math basics"]
    ),
    Course(
        "Natural Language Processing",
        "Coursera",
        ["python", "nlp", "ml", "deep learning"],
        "advanced",
        "ai",
        "8 weeks",
        ["Machine Learning", "Python"]
    ),
    Course(
        "DevOps with Docker & Kubernetes",
        "Udemy",
        ["docker", "kubernetes", "linux", "aws"],
        "intermediate",
        "cloud",
        "6 weeks",
        ["Linux", "AWS basics"]
    ),
    Course(
        "React Frontend Development",
        "Udemy",
        ["react", "javascript", "html", "css"],
        "intermediate",
        "web",
        "6 weeks",
        ["JavaScript", "HTML", "CSS"]
    ),
    Course(
        "SQL & Database Design",
        "Coursera",
        ["sql", "databases", "data modeling"],
        "beginner",
        "data",
        "4 weeks",
        []
    ),
]