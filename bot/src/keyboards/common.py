from aiogram.utils.formatting import Text


def get_start_message() -> Text:
    welcome_text = Text(
        "Привет! ✨\n\n"
        "Я бот для просмотра баллов по ЕГЭ.\n\n"
        "Вот что я умею:\n"
        "📝 /register — регистрация\n"
        "➕ /enter_scores — добавить предмет и баллы\n"
        "📊 /view_scores — посмотреть все свои предметы\n\n"
        "Жми /register, чтобы начать!"
    )
    return welcome_text
