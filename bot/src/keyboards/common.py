from aiogram.utils.formatting import Text


def get_start_message() -> Text:
    welcome_text = Text(
        "Привет! ✨\n\n"
        "Я бот для просмотра баллов по ЕГЭ.\n\n"
        "Вот что я умею:\n"
        "📝 /register — представиться боту\n"
        "➕ /enter_scores — добавить новый балл\n"
        "📊 /view_scores — посмотреть всю свою статистику\n\n"
        "Жми /register, чтобы начать!"
    )
    return welcome_text
