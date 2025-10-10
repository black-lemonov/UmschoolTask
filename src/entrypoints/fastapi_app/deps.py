from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import get_postgres_url

engine = create_engine(get_postgres_url())
session_factory = sessionmaker(bind=engine)


def get_session():
    yield session_factory()


SessionDep = Annotated[Session, Depends(get_session)]
