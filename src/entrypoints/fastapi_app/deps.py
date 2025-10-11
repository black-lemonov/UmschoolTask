from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import get_postgres_url

engine = create_async_engine(get_postgres_url())
session_factory = async_sessionmaker(bind=engine)


async def get_session():
    async with session_factory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
