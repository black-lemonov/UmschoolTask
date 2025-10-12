import os

import dotenv

dotenv.load_dotenv()


def get_bot_token() -> str:
    return os.getenv("BOT_TOKEN")


def get_base_api() -> str:
    return "http://127.0.0.1:8000"
