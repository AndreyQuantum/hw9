import uuid
from typing import Any

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

from models import Student, Base


class DatabaseInteraction:
    engine = create_engine("sqlite:///students.db", echo=True)
    Base.metadata.create_all(engine)

    def create_student(self, student: Student) -> Student:
        with Session(self.engine) as session:
            session.add(student)
            session.commit()
            session.refresh(student)
        return student

    def create_students(self, students: list[Student]) -> list[Student]:
        with Session(self.engine) as session:
            session.add_all(students)
            session.commit()
        return students

    def get_students(self, faculty: str | None) -> list[Student]:
        statement = select(Student)
        if faculty:
            statement.where(Student.faculty == faculty)
        with Session(self.engine) as session:
            return list(session.scalars(statement))

    def get_courses(self) -> list[str]:
        with Session(self.engine) as session:
            unique_faculties = session.query(Student.course).distinct().all()
            return [faculty[0] for faculty in unique_faculties]

    def update_student(self, student_id: uuid.UUID ,student_data: dict) -> Student:
        with Session(self.engine) as session:
            student = self.get_student_by_id(session, student_id)
            for key,value in student_data.items():
                setattr(student,key,value)
            session.commit()
            session.refresh(student)
            return student

    def get_student_by_id(self, session: Session, student_id: uuid.UUID) -> Any | None:
        return session.scalar(select(Student).where(Student.id == student_id))

    def delete_student(self, student_id: uuid.UUID) -> Student:
        with Session(self.engine) as session:
            student = self.get_student_by_id(session, student_id)
            session.delete(student)
            session.commit()
            return student

    def get_middle_grade(self) -> float:
        with Session(self.engine) as session:
            return float(session.query(func.avg(Student.grade)).scalar())
