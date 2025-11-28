from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from models.models import Student
from repositories.student_repository import StudentRepository
from schemas.student import CreateStudent


class StudentService:
    @staticmethod
    def get_students(db_session: Session,faculty: str | None):
        result = StudentRepository().get_students(faculty, db_session)
        if result:
            return result
        raise HTTPException(status_code=404, detail="Students not found")

    @staticmethod
    def create_student(db_session: Session,student: CreateStudent) -> Student:
        student_to_create = Student(**student.model_dump())
        return StudentRepository().create_student(student_to_create, db_session)

    @staticmethod
    def delete_student(student_id: int,db_session: Session):
        return StudentRepository().delete_student(student_id, db_session)

    @staticmethod
    def delete_student_bulk(cls,ids: list[int], db_session: Session):
        for student_id in ids:
            cls.delete_student(student_id, db_session)