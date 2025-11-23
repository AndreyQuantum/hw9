from fastapi import APIRouter

user_app = APIRouter()

@user_app.post("/register")
def register_user():
    return {"user": "admin"}