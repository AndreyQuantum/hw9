from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from api.dependencies import session_deps
from schemas.auth import Token
from services.auth_service import AuthService

auth_router = APIRouter()


@auth_router.post("/token")
def login_for_access_token(
        db_session: session_deps,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    auth_service = AuthService()

    user = auth_service.authenticate_user(email = form_data.username.lower(),
                                          password=form_data.password,
                                          db_session=db_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=10
    )
    access_token = auth_service.create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")