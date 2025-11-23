from fastapi import HTTPException, APIRouter

from repositories.base import session_deps
from repositories.grade_repository import GradeRepository

app = APIRouter()

@app.get("/grade/middle")
def get_middle_grade(db_session: session_deps) -> float:
    result = GradeRepository().get_middle_grade(db_session)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Grades not found")