from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

class Base(DeclarativeBase):
    pass

class Student(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    last_name: Mapped[str]
    faculty: Mapped[str]
    course: Mapped[str]
    grade: Mapped[int]