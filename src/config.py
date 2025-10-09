import os

from dotenv import load_dotenv

load_dotenv()


def get_postgres_url() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "54321")
    password = os.getenv("DB_PASSWORD", "password")
    user = os.getenv("DB_USER", "umschool")
    db_name = os.getenv("DB_NAME", "umschool")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
