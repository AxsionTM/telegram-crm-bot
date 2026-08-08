from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.utils.callbacks import AdminCallbacks


def get_applications_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🔎 Поиск",
                callback_data=AdminCallbacks.SEARCH_MENU,
            ),
            InlineKeyboardButton(
                "🎯 Фильтр",
                callback_data=AdminCallbacks.FILTER_MENU,
            ),
        ],

        [
            InlineKeyboardButton(
                "⬅️",
                callback_data=AdminCallbacks.PREV_PAGE,
            ),
            InlineKeyboardButton(
                "➡️",
                callback_data=AdminCallbacks.NEXT_PAGE,
            ),
        ],

        [
            InlineKeyboardButton(
                "🔙 Назад",
                callback_data=AdminCallbacks.BACK,
            ),
        ],

    ]

    return InlineKeyboardMarkup(keyboard)