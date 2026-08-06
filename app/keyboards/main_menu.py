from telegram import ReplyKeyboardMarkup


def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню пользователя."""

    keyboard = [
        ["📝 Оставить заявку"],
        ["ℹ️ Контакты"],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )