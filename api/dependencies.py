from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from models.user import User
from repositories.base import get_session
from services.auth_service import AuthService

session_deps = Annotated[Session, Depends(get_session)]

async def get_current_user_dependency(
        db_session: session_deps,
        token: Annotated[str, Depends(User)],
) -> User:
    auth_utils = AuthService()
    return await auth_utils.authenticate_user(
        token=token
    )