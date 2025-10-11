import asyncio
import aiohttp
import logging
import os
import sys

import dotenv
from aiogram import Bot, Dispatcher
from aiogram import filters
from aiogram import types 
from aiogram.utils.formatting import (
    as_list, as_key_value
)


dp = Dispatcher()


BASE_API = "http://127.0.0.1:8000"


@dp.message(filters.CommandStart())
async def start(message: types.Message):
    content = as_list(
        "Команды:",
        as_key_value("/start", " информация о боте"),
        as_key_value("/register <Имя> <Фамилия>", " регистрация"),
        as_key_value("/view_scores", " просмотр баллов по предметам"),
        as_key_value("/enter_scores <Предмет> <Баллы>", " добавление баллов"),
        marker=" "
    )
    await message.answer(
        "Привет, этот бот умеет сохранять баллы ЕГЭ",
    )
    await message.answer(
        **content.as_kwargs()
    )       


@dp.message(filters.Command("register"))
async def register(message: types.Message, command: filters.CommandObject):
    async with aiohttp.ClientSession() as session:
        firstname, lastname = command.args.split(' ')
        async with session.post(
            f"{BASE_API}/signup", json={
                "studentid": message.from_user.id,
                "firstname": firstname,
                "lastname": lastname
            }
        ) as response:
            if response.status == 200:
                await message.answer("Успешно")
            else:
                data = await response.json()
                await message.answer(f"Ошибка: {data["msg"]}")


@dp.message(filters.Command("enter_scores"))
async def enter_scores(message: types.Message, command: filters.CommandObject):
    async with aiohttp.ClientSession() as session:
        subjectname, score = command.args.split(' ')
        async with session.post(
            f"{BASE_API}/records", json={
                "subjectname": subjectname,
                "score": int(score),
                "studentid": message.from_user.id
            }
        ) as response:
            if response.status == 200:
                await message.answer("Запись добавлена")
            else:
                data = await response.json()
                await message.answer(f"Ошибка: {data["msg"]}")


@dp.message(filters.Command("view_scores"))
async def view_scores(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BASE_API}/scores",
            params={"studentid": message.from_user.id}
        ) as response:
            data = await response.json()
            if response.status == 200:
                scores_list = as_list(
                    *[as_key_value(name, score) for name, score in data.items()]
                )
                await message.answer(
                    **scores_list.as_kwargs()
                )
            else:
                await message.answer(
                    f"Ошибка: {data["msg"]}"
                )


async def main():
    dotenv.load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
