import json
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, ml_engine, gemini_agent
from .database import get_db, engine, SessionLocal
from course_database import COURSES
from PathPilot import INTERNSHIPS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lumora-api")

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lumora API",
    description="Intelligent Learning Path and Career Navigation Backend API",
    version="1.1.0"
)

# CORS middleware for local development and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def auto_seed_db():
    """Ensure database has initial courses and internships seeded."""
    db = SessionLocal()
    try:
        if db.query(models.CourseModel).count() == 0:
            logger.info("Seeding initial courses into database...")
            for course in COURSES:
                db_course = models.CourseModel(
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
            db.commit()
            logger.info(f"Seeded {len(COURSES)} courses.")

        if db.query(models.InternshipModel).count() == 0:
            logger.info("Seeding initial internships into database...")
            for intern in INTERNSHIPS:
                db_intern = models.InternshipModel(
                    title=intern.title,
                    company=intern.company,
                    skills=json.dumps(intern.skills),
                    level=intern.level,
                    domain=intern.domain,
                    mode=intern.mode
                )
                db.add(db_intern)
            db.commit()
            logger.info(f"Seeded {len(INTERNSHIPS)} internships.")
    except Exception as e:
        logger.error(f"Error during auto-seeding: {e}")
        db.rollback()
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    auto_seed_db()

@app.get("/")
def root():
    return {
        "status": "healthy",
        "message": "Lumora AI Navigation API is operational",
        "docs": "/docs"
    }

@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    courses_count = db.query(models.CourseModel).count()
    internships_count = db.query(models.InternshipModel).count()
    return {
        "status": "online",
        "courses_available": courses_count,
        "internships_available": internships_count
    }

@app.post("/api/recommend-courses", response_model=List[schemas.CourseResponse])
def recommend_courses(request: schemas.UserProfileRequest, db: Session = Depends(get_db)):
    courses = db.query(models.CourseModel).all()
    recommendations = ml_engine.get_recommendations(
        courses, 
        request.user_skills, 
        request.experience_level, 
        request.domain_pref or "any", 
        is_internship=False
    )
    
    response = []
    for rec in recommendations:
        course = rec["item"]
        response.append(schemas.CourseResponse(
            id=course.id,
            name=course.name,
            platform=course.platform,
            difficulty=course.difficulty,
            domain=course.domain,
            duration=course.duration,
            match_percentage=rec["percentage"],
            matched_skills=rec["matched_skills"]
        ))
    return response

@app.post("/api/recommend-internships", response_model=List[schemas.InternshipResponse])
def recommend_internships(request: schemas.UserProfileRequest, db: Session = Depends(get_db)):
    internships = db.query(models.InternshipModel).all()
    recommendations = ml_engine.get_recommendations(
        internships, 
        request.user_skills, 
        request.experience_level, 
        request.domain_pref or "any", 
        is_internship=True
    )
    
    response = []
    for rec in recommendations:
        intern = rec["item"]
        response.append(schemas.InternshipResponse(
            id=intern.id,
            title=intern.title,
            company=intern.company,
            level=intern.level,
            domain=intern.domain,
            mode=intern.mode,
            match_percentage=rec["percentage"],
            matched_skills=rec["matched_skills"]
        ))
    return response

@app.post("/api/generate-career-advice")
def generate_career_advice(request: schemas.AdviceRequest):
    advice = gemini_agent.generate_advice(
        request.user_skills,
        request.goal,
        request.experience_level,
        request.top_recommendation
    )
    return {"advice": advice}
