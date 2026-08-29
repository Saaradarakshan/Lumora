from sqlalchemy import Column, Integer, String, Text
from .database import Base

class CourseModel(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    platform = Column(String)
    skills = Column(Text)  # Comma-separated or JSON string
    difficulty = Column(String)
    domain = Column(String)
    duration = Column(String)
    prerequisites = Column(Text)  # Comma-separated or JSON string
    url = Column(String, default="")

class InternshipModel(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    skills = Column(Text)  # Comma-separated or JSON string
    level = Column(String)
    domain = Column(String)
    mode = Column(String)

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    goal = Column(String)
    experience_level = Column(String)
    skills = Column(Text)
    hours_per_day = Column(Integer)
