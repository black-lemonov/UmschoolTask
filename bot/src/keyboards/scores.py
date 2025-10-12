from aiogram import types
from aiogram.utils.formatting import as_key_value, as_list, as_section, Text


def get_subjects_keyboard(subjects: list[str]) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=s, callback_data=s)] for s in subjects
        ]
    )
    return keyboard


def get_records_list(records: dict[str, int]) -> Text:
    if records:
        subjects_list = as_list(
            *[as_key_value(name, score) for name, score in records.items()]
        )
    else:
        subjects_list = "Пусто"
    
    content = as_section(
        "Ваши предметы:",
        subjects_list
    )
    return content
