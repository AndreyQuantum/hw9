import datetime
from typing import Any, Annotated

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import argon2
from sqlalchemy.orm import Session
from starlette import status

from models.user import User
from repositories.user_repository import UserRepository
from services.password_service import PasswordService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
)
oauth2_scheme_deps = Annotated[str, Depends(oauth2_scheme)]

class AuthService:

    password_service = PasswordService()
    user_repository = UserRepository()
    def authenticate_user(self, email: str, password: str, db_session: Session) -> Any | None:
        user_data = UserRepository().get_user_by_email(email,db_session=db_session)
        if user_data and self.password_service.verify_password(password, user_data.hashed_password):
            return user_data
        return None

    def get_current_user(
            self,
            token: oauth2_scheme_deps,
            db_session: Session
    ) -> User:

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        payload = jwt.decode(
            token, "test_secret_key", algorithms=["HS256"]
        )
        subject: str | None = payload.get("sub")
        if subject is None:
            raise credentials_exception

        user = self.user_repository.get_user_by_id(subject, db_session=db_session)
        if not user:
            raise credentials_exception

        return user

    def create_access_token(
            self,
            *,
            subject: str,
            expires_delta: datetime.timedelta = datetime.timedelta(minutes=15),
    ) -> str:
        to_encode: dict = {"sub": subject}
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            "test_secret_key",
            algorithm="HS256",
        )
        return encoded_jwt

