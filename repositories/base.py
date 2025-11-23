from sqlalchemy import create_engine

from models.base import Base
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///students.db", echo=True)
Base.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

