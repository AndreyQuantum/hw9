import csv
import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from api.student import app as student_router
from api.grade import app as grade_router
from api.courses import app as courses_router
from api.user import user_app
from models.base import Base
from models.models import Student
from repositories.base import get_session, engine
from repositories.student_repository import StudentRepository
from sqlalchemy.orm import Session

def init_db():
    import models.models
    import models.user
    Base.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    init_db()
    student_repository = StudentRepository()

    with open("students.csv", "r") as f, Session(engine) as session:
        reader = csv.DictReader(f)
        for row in reader:
            student = Student(
                last_name=row["Фамилия"],
                name=row["Имя"],
                faculty=row["Факультет"],
                course=row["Курс"],
                grade=row["Оценка"]
            )
            student_repository.create_student(student, session)
    yield
    engine.dispose()
    os.remove("students.db")

app = FastAPI(lifespan=lifespan)

app.include_router(router=student_router, prefix="/student", tags=["student"])
app.include_router(router=grade_router, prefix="/grade", tags=["grade"])
app.include_router(router=courses_router, prefix="/course",tags=["course"])
app.include_router(router=user_app, prefix="/user",tags=["user"])