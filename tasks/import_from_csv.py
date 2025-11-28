import csv
from pathlib import Path

from sqlalchemy.orm import Session

from models.models import Student
from repositories.base import engine
from repositories.student_repository import StudentRepository


async def export_students_from_csv( path_to_csv: Path):
    student_repository = StudentRepository()
    with open(path_to_csv, "r") as f, Session(engine) as session:
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
