# ============================================================
# finlearn.py — Financial Education & Learning Module
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# --- Dummy course data ---
courses = [
    {
        "id": 1,
        "title": "Basics of Stock Market",
        "description": "Learn how the stock market works, exchanges, and indices.",
        "category": "Stocks",
        "level": "Beginner",
        "duration": "2 Hours"
    },
    {
        "id": 2,
        "title": "Mutual Funds & SIPs",
        "description": "Understand SIPs, NAV, and how mutual funds can grow your wealth.",
        "category": "Mutual Funds",
        "level": "Intermediate",
        "duration": "3 Hours"
    },
    {
        "id": 3,
        "title": "Government Policies & Schemes",
        "description": "Explore government-backed schemes like NPS, PPF, and Sukanya Samriddhi.",
        "category": "Policies",
        "level": "Beginner",
        "duration": "1.5 Hours"
    }
]

# --- Models ---
class CourseProgress(BaseModel):
    email: str
    course_id: int
    completed: bool

# Temporary store (replace with DB later)
user_progress = {}

# --- Routes ---
@router.get("/courses")
def get_all_courses():
    return {"available_courses": courses}

@router.get("/course/{course_id}")
def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")

@router.post("/progress")
def mark_progress(data: CourseProgress):
    user_progress.setdefault(data.email, {})
    user_progress[data.email][data.course_id] = data.completed
    return {"message": f"Progress saved for {data.email} on course {data.course_id}"}

@router.get("/progress/{email}")
def get_progress(email: str):
    return user_progress.get(email, {})
