from fastapi import FastAPI

from db_interaction import DatabaseInteraction

app = FastAPI()

@app.get("/students")
def get_students(faculty: str|None):
    DatabaseInteraction().get_students(faculty)

@app.get("/courses")
def get_courses():
    pass

@app.get("/grade/middle")
def get_middle_grade():
    pass