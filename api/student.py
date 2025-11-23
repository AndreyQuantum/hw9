from fastapi import HTTPException, APIRouter

from models.models import Student
from api.dependencies import session_deps
from repositories.student_repository import StudentRepository
from schemas.student import CreateStudent, GetStudent

app = APIRouter()


@app.get("/")
def get_students(db_session: session_deps,faculty: str | None = None):
    result = StudentRepository().get_students(faculty, db_session)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Students not found")

@app.post("/")
def create_student(student: CreateStudent,db_session: session_deps) -> GetStudent:
    student_to_create = Student(**student.model_dump())
    return StudentRepository().create_student(student_to_create, db_session)

@app.put("/{student_id}")
def update_student(student_id: int, student: CreateStudent, db_session: session_deps) -> GetStudent:
    updated_dict = student.model_dump(exclude_unset=True)
    return StudentRepository().update_student(student_id, updated_dict, db_session)

@app.delete("/{student_id}")
def delete_student(student_id: int, db_session: session_deps) -> GetStudent:
    return StudentRepository().delete_student(student_id, db_session)
