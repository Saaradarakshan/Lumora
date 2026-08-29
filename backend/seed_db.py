import sys
import os
import json

# Add parent directory to path so we can import old modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine, Base, SessionLocal
from backend.models import CourseModel, InternshipModel
from course_database import COURSES
from PathPilot import INTERNSHIPS

def seed_data():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Seed Courses
    if db.query(CourseModel).count() == 0:
        print("Seeding courses...")
        for course in COURSES:
            db_course = CourseModel(
                name=course.name,
                platform=course.platform,
                skills=json.dumps(course.skills),
                difficulty=course.difficulty,
                domain=course.domain,
                duration=course.duration,
                prerequisites=json.dumps(course.prerequisites),
                url=course.url
            )
            db.add(db_course)
    else:
        print("Courses already seeded.")

    # Seed Internships
    if db.query(InternshipModel).count() == 0:
        print("Seeding internships...")
        for intern in INTERNSHIPS:
            db_intern = InternshipModel(
                title=intern.title,
                company=intern.company,
                skills=json.dumps(intern.skills),
                level=intern.level,
                domain=intern.domain,
                mode=intern.mode
            )
            db.add(db_intern)
    else:
        print("Internships already seeded.")

    db.commit()
    db.close()
    print("Database seeding completed.")

if __name__ == "__main__":
    seed_data()
