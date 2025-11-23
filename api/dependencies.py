from typing import Annotated

from fastapi.params import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models.user import User
from repositories.base import get_session
from services.auth_service import AuthService, oauth2_scheme

session_deps = Annotated[Session, Depends(get_session)]



def login_by_token(
        db_session: session_deps,
        token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    auth_utils = AuthService()
    return auth_utils.get_current_user(
        token=token,
        db_session=db_session
    )

auth_security = Security(login_by_token)

auth_deps = Annotated[User, auth_security]