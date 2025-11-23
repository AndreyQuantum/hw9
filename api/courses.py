from fastapi import APIRouter, HTTPException

from api.student import database_interaction

app = APIRouter()

@app.get("/courses")
def get_courses() -> list[str]:
    result = database_interaction.get_courses()
    if result:
        return result
    raise HTTPException(status_code=404, detail="Courses not found")

