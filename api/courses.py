from fastapi import APIRouter, HTTPException

from api.dependencies.db import session_deps
from repositories.course_repository import CourseRepository
from services.redis_cache_service import RedisCache

app = APIRouter()
cache = RedisCache()

@app.get("/courses")
@cache.cache()
def get_courses(db_session: session_deps) -> list[str]:
    result = CourseRepository().get_courses(db_session)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Courses not found")

