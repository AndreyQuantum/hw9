from pathlib import Path

from fastapi import HTTPException, APIRouter, BackgroundTasks
from starlette.requests import Request

from models.models import Student
from api.dependencies.db import session_deps
from api.dependencies.token import auth_deps
from repositories.student_repository import StudentRepository
from schemas.student import CreateStudent, GetStudent
from services.redis_cache_service import RedisCache
from services.student_service import StudentService
from tasks.import_from_csv import export_students_from_csv

app = APIRouter()

cache = RedisCache()


@app.get("/")
@cache.cache()
async def get_students(db_session: session_deps, request: Request,faculty: str | None = None):
    return StudentService.get_students(db_session, faculty)

@app.post("/")
@cache.invalidate()
async def create_student(student: CreateStudent,db_session: session_deps, request: Request) -> GetStudent:

    return StudentService.create_student(student=student,db_session=db_session)

@app.post("/import/csv")
@cache.invalidate()
async def import_students(path_to_file: Path ,
                          background_tasks: BackgroundTasks, request: Request):
    background_tasks.add_task(export_students_from_csv, path_to_csv=path_to_file)

@app.delete("/bulk")
@cache.invalidate()
async def delete_students(student_ids: list[int],background_tasks: BackgroundTasks, db_session: session_deps, request: Request):
    background_tasks.add_task(StudentService.delete_student_bulk, StudentService,student_ids, db_session)


@app.put("/{student_id}")
@cache.invalidate()
async def update_student(student_id: int, student: CreateStudent, db_session: session_deps, request: Request) -> GetStudent:
    updated_dict = student.model_dump(exclude_unset=True)
    return StudentRepository().update_student(student_id, updated_dict, db_session)

@app.delete("/{student_id}")
@cache.invalidate()
async def delete_student(student_id: int, db_session: session_deps, request: Request) -> GetStudent:
    return StudentRepository().delete_student(student_id, db_session)
