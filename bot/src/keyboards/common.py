from aiogram.utils.formatting import as_key_value, as_list, as_section, Text


def get_start_message() -> Text:
    return as_section(
        "Привет 👋 Я бот для просмотра баллов по ЕГЭ!",
        as_section(
            "Мои команды:",
            as_list(
                as_key_value("/register", " Регистрация"),
                as_key_value("/view_scores", " Смотреть баллы"),
                as_key_value("/enter_scores", " Добавить предмет"),
            ),
        ),
    )
