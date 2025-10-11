import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import clear_mappers

from src.adapters.orm import mapper_registry, start_mappers


@pytest_asyncio.fixture
async def in_memory_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(in_memory_db):
    start_mappers()

    yield async_sessionmaker(bind=in_memory_db, expire_on_commit=False)

    clear_mappers()


@pytest_asyncio.fixture
async def session(session_factory):
    async with session_factory() as session:
        yield session
