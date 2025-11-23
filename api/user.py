from fastapi import APIRouter

from api.dependencies import session_deps
from repositories.user_repository import UserRepository
from schemas.user import CreateUser, GetUser

user_app = APIRouter()

@user_app.post("/register")
def register_user(user_data: CreateUser, db_session: session_deps) -> GetUser:
    return UserRepository().create_user(user_data, db_session)