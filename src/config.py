import os

from dotenv import load_dotenv

load_dotenv()


def get_postgres_url() -> str:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    password = os.getenv("DB_PASSWORD")
    user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
