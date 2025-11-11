import csv

from fastapi import FastAPI, HTTPException

from db_interaction import DatabaseInteraction
from models import Student
from schemas import CreateStudent

app = FastAPI()
database_interaction = DatabaseInteraction()

def populate_db_from_file():
    with open("students.csv", "r") as f:
        reader = csv.DictReader(f)
        students_to_create = []
        for row in reader:
            students_to_create.append(Student(
                last_name=row["Фамилия"],
                name=row["Имя"],
                faculty=row["Факультет"],
                course=row["Курс"],
                grade=row["Оценка"]
            ))
        database_interaction.create_students(students_to_create)

populate_db_from_file()
@app.get("/students")
def get_students(faculty: str | None = None):
    result = database_interaction.get_students(faculty)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Students not found")

@app.post("/students")
def create_student(student: CreateStudent):
    student_to_create = Student(**student.model_dump())
    database_interaction.create_student(student_to_create)

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