from sqlalchemy.orm import Session

from models.user import User
from schemas.user import CreateUser
from services.password_service import PasswordService


class UserRepository:
    def create_user(self, user: CreateUser, db_session: Session) -> User:
        created_user = User(**user.model_dump(exclude={"password"}))
        created_user.hashed_password = PasswordService().hash_password(user.password)
        db_session.add(created_user)
        db_session.commit()
        db_session.refresh(created_user)
        return created_user
