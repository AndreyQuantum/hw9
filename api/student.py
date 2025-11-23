import csv
import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, APIRouter

from repository import StudentRepository
from models import Student
from schemas import CreateStudent, GetStudent
database_interaction = StudentRepository()

app = APIRouter()


@app.get("/")
def get_students(faculty: str | None = None):
    result = database_interaction.get_students(faculty)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Students not found")

@app.post("/")
def create_student(student: CreateStudent) -> GetStudent:
    student_to_create = Student(**student.model_dump())
    return database_interaction.create_student(student_to_create)

@app.put("/{student_id}")
def update_student(student_id: int, student: CreateStudent) -> GetStudent:
    updated_dict = student.model_dump(exclude_unset=True)
    return database_interaction.update_student(student_id, updated_dict)

@app.delete("/{student_id}")
def delete_student(student_id: int) -> GetStudent:
    return database_interaction.delete_student(student_id)
