from fastapi import HTTPException, APIRouter
from starlette.requests import Request

from models.models import Student
from api.dependencies.db import session_deps
from api.dependencies.token import auth_deps
from repositories.student_repository import StudentRepository
from schemas.student import CreateStudent, GetStudent
from services.redis_cache_service import RedisCache

app = APIRouter()

cache = RedisCache()


@app.get("/")
@cache.cache()
async def get_students(db_session: session_deps, request: Request,faculty: str | None = None):
    result = StudentRepository().get_students(faculty, db_session)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Students not found")

@app.post("/")
@cache.invalidate()
async def create_student(student: CreateStudent,db_session: session_deps, request: Request) -> GetStudent:
    student_to_create = Student(**student.model_dump())
    return StudentRepository().create_student(student_to_create, db_session)

@app.put("/{student_id}")
@cache.invalidate()
async def update_student(student_id: int, student: CreateStudent, db_session: session_deps, request: Request) -> GetStudent:
    updated_dict = student.model_dump(exclude_unset=True)
    return StudentRepository().update_student(student_id, updated_dict, db_session)

@app.delete("/{student_id}")
@cache.invalidate()
async def delete_student(student_id: int, db_session: session_deps, request: Request) -> GetStudent:
    return StudentRepository().delete_student(student_id, db_session)
