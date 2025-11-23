from models.models import Student
from repositories.base import get_session


class CourseRepository:

    def get_courses(self, db_session) -> list[str]:
        unique_faculties = db_session.query(Student.course).distinct().all()
        return [faculty[0] for faculty in unique_faculties]