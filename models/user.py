from sqlalchemy.orm import Mapped

from models.base import Base


class User(Base):

    __tablename__ = "user"

    full_name: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = True
