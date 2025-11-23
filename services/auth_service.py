import datetime
from typing import Any

import jwt
from passlib.hash import argon2
from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository
from services.password_service import PasswordService


class AuthService:

    password_service = PasswordService()

    def authenticate_user(self, email: str, password: str, db_session: Session) -> Any | None:
        user_data = UserRepository().get_user_by_email(email,db_session=db_session)
        if user_data and self.password_service.verify_password(password, user_data.hashed_password):
            return user_data
        return None

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

