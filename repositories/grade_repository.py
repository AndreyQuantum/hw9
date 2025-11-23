from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.models import Student


class GradeRepository:
    def get_middle_grade(self, session: Session) -> float:
        value = session.execute(select(func.avg(Student.grade))).scalar()
        return float(value) if value is not None else None