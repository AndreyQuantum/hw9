from fastapi import APIRouter, HTTPException

from api.dependencies.db import session_deps
from repositories.course_repository import CourseRepository

app = APIRouter()

@app.get("/courses")
def get_courses(db_session: session_deps) -> list[str]:
    result = CourseRepository().get_courses(db_session)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Courses not found")

