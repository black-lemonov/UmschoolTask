import os

from dotenv import load_dotenv

load_dotenv()


def get_postgres_url() -> str:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    password = os.getenv("DB_PASSWORD")
    user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def get_alembic_postgres_url() -> str:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    password = os.getenv("DB_PASSWORD")
    user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_test_postgres_url() -> str:
    host = "localhost"
    port = "54321"
    password = "123"
    user = "test"
    db_name = "test"
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
