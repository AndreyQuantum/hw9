# repository.py
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from model import Student, Base


class DatabaseInteraction:
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)

    def create_student(self, student: Student) -> Student:
        with Session(self.engine) as session:
            session.add(student)
            session.commit()
        return student

    def get_students(self, faculty: str | None) -> list[Student]:
        statement = select(Student)
        if faculty:
            statement.where(Student.faculty == faculty)
        with Session(self.engine) as session:
            return list(session.scalars(statement))

