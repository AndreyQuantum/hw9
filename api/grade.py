from fastapi import HTTPException, APIRouter
from starlette.requests import Request

from api.dependencies.db import session_deps
from repositories.grade_repository import GradeRepository
from services.redis_cache_service import RedisCache

app = APIRouter()
cache = RedisCache()

@app.get("/grade/middle")
@cache.cache()
async def get_middle_grade(db_session: session_deps, request: Request) -> float:
    result = GradeRepository().get_middle_grade(db_session)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Grades not found")