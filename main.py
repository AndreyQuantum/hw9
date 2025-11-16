import csv
import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from repository import DatabaseInteraction
from models import Student
from schemas import CreateStudent, GetStudent
database_interaction = DatabaseInteraction()


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

@app.get("/students")
def get_students(faculty: str | None = None):
    result = database_interaction.get_students(faculty)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Students not found")

@app.post("/students")
def create_student(student: CreateStudent) -> GetStudent:
    student_to_create = Student(**student.model_dump())
    return database_interaction.create_student(student_to_create)

@app.put("/students/{student_id}")
def update_student(student_id: int, student: CreateStudent) -> GetStudent:
    updated_dict = student.model_dump(exclude_unset=True)
    return database_interaction.update_student(student_id, updated_dict)

@app.delete("/students/{student_id}")
def delete_student(student_id: int) -> GetStudent:
    return database_interaction.delete_student(student_id)

@app.get("/courses")
def get_courses() -> list[str]:
    result = database_interaction.get_courses()
    if result:
        return result
    raise HTTPException(status_code=404, detail="Courses not found")

@app.get("/grade/middle")
def get_middle_grade() -> float:
    result = database_interaction.get_middle_grade()
    if result:
        return result
    raise HTTPException(status_code=404, detail="Grades not found")