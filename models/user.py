from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class User(Base):

    __tablename__ = "user"

    full_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = True
