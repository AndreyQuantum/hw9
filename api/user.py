from fastapi import APIRouter
from starlette.requests import Request

from api.dependencies.db import session_deps
from repositories.user_repository import UserRepository
from schemas.user import CreateUser, GetUser
from services.redis_cache_service import RedisCache

user_app = APIRouter()
cache = RedisCache()

@user_app.post("/register")
async def register_user(user_data: CreateUser, db_session: session_deps, request: Request) -> GetUser:
    return UserRepository().create_user(user_data, db_session)