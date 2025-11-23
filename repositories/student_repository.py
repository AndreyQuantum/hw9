import uuid
from typing import Any

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models.models import Student


class StudentRepository:

    def create_student(self, student: Student, session: Session) -> Student:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student

    def create_students(self, students: list[Student], session: Session) -> list[Student]:
        session.add_all(students)
        session.commit()
        return students

    def get_students(self, faculty: str | None, session: Session) -> list[Student]:
        statement = select(Student)
        if faculty:
            statement.where(Student.faculty == faculty)
        return list(session.scalars(statement))


    def update_student(self, student_id: uuid.UUID ,student_data: dict, session: Session) -> Student:
        student = self.get_student_by_id(session, student_id)
        for key,value in student_data.items():
            setattr(student,key,value)
        session.commit()
        session.refresh(student)
        return student

    def get_student_by_id(self, session: Session, student_id: uuid.UUID) -> Any | None:
        return session.scalar(select(Student).where(Student.id == student_id))

    def delete_student(self, student_id: uuid.UUID, session: Session) -> Student:
        student = self.get_student_by_id(session, student_id)
        session.delete(student)
        session.commit()
        return student
