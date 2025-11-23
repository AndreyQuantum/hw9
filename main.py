import csv
import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from api.student import app as student_router
from api.grade import app as grade_router
from api.courses import app as courses_router
from models.models import Student
from repositories.base import get_session, engine
from repositories.student_repository import StudentRepository


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    student_repository = StudentRepository()
    from sqlalchemy.orm import Session
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

app.include_router(router=student_router, prefix="/students", tags=["students"])
app.include_router(router=grade_router, prefix="/grades", tags=["grades"])
app.include_router(router=courses_router, prefix="/courses",tags=["courses"])