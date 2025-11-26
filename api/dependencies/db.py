from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from repositories.base import get_session

session_deps = Annotated[Session, Depends(get_session)]
