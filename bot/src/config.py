import os

import dotenv

dotenv.load_dotenv()


def get_bot_token() -> str:
    return os.getenv("BOT_TOKEN")


def get_base_api() -> str:
    return "http://backend:5000"
