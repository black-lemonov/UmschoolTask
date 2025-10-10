import os

from dotenv import load_dotenv

load_dotenv()


def get_postgres_url() -> str:
    host = "db"
    port = "5432"
    password = os.getenv("DB_PASSWORD", "password")
    user = os.getenv("DB_USER", "umschool")
    db_name = os.getenv("DB_NAME", "umschool")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
