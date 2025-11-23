from fastapi import HTTPException, APIRouter

from api.student import database_interaction

app = APIRouter()

@app.get("/grade/middle")
def get_middle_grade() -> float:
    result = database_interaction.get_middle_grade()
    if result:
        return result
    raise HTTPException(status_code=404, detail="Grades not found")