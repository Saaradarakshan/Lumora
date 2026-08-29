from pydantic import BaseModel
from typing import List, Optional

class UserProfileRequest(BaseModel):
    user_skills: List[str]
    goal: str
    experience_level: str
    domain_pref: Optional[str] = "any"

class CourseResponse(BaseModel):
    id: int
    name: str
    platform: str
    difficulty: str
    domain: str
    duration: str
    match_percentage: float
    matched_skills: List[str]
    
class InternshipResponse(BaseModel):
    id: int
    title: str
    company: str
    level: str
    domain: str
    mode: str
    match_percentage: float
    matched_skills: List[str]

class AdviceRequest(BaseModel):
    user_skills: List[str]
    goal: str
    experience_level: str
    top_recommendation: str
