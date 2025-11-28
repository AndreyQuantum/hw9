import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.auth import auth_router
from api.dependencies.token import auth_security
from api.student import app as student_router
from api.grade import app as grade_router
from api.courses import app as courses_router
from api.user import user_app
from models.base import Base
from repositories.base import engine
from repositories.student_repository import StudentRepository

from tasks.import_from_csv import export_students_from_csv
from pathlib import Path


def init_db():
    Base.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    init_db()

    await export_students_from_csv(path_to_csv=Path("students.csv"))
    yield
    engine.dispose()
    os.remove("students.db")

app = FastAPI(lifespan=lifespan)

app.include_router(router=auth_router, prefix="/auth",tags=["auth"])

app.include_router(router=student_router, prefix="/student", tags=["student"], dependencies=[auth_security])
app.include_router(router=grade_router, prefix="/grade", tags=["grade"], dependencies=[auth_security])
app.include_router(router=courses_router, prefix="/course",tags=["course"], dependencies=[auth_security])
app.include_router(router=user_app, prefix="/user",tags=["user"])
