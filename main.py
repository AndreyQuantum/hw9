import csv
import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from api.student import app as student_router
from api.student import database_interaction
from api.grade import app as grade_router
from api.courses import app as courses_router
from models import Student

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    with open("students.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = Student(
                last_name=row["Фамилия"],
                name=row["Имя"],
                faculty=row["Факультет"],
                course=row["Курс"],
                grade=row["Оценка"]
            )
            database_interaction.create_student(student)
    yield
    database_interaction.engine.dispose()
    os.remove("students.db")

app = FastAPI(lifespan=lifespan)

app.include_router(router=student_router, prefix="/students")
app.include_router(router=grade_router, prefix="/grades")
app.include_router(router=courses_router, prefix="/courses")