import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src import config
from src.handlers import common, register, scores


async def main():
    bot = Bot(token=config.get_bot_token())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(common.router, register.router, scores.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
