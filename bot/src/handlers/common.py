from aiogram import Router, filters, types

from src.keyboards import common as keyboards

router = Router()


@router.message(filters.CommandStart())
async def start(message: types.Message):
    start_message = keyboards.get_start_message()
    await message.answer(**start_message.as_kwargs())
