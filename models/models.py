from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from models.base import Base


class Student(Base):

    __tablename__ = "student"
    name: Mapped[str]
    last_name: Mapped[str]
    faculty: Mapped[str]
    course: Mapped[str]
    grade: Mapped[int]

