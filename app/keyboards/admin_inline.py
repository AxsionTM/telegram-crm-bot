from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.callbacks import AdminCallbacks


def get_admin_panel() -> InlineKeyboardMarkup:
    """Главное меню CRM."""

    keyboard = [
        [
            InlineKeyboardButton(
                "📋 Заявки",
                callback_data=AdminCallbacks.APPLICATIONS,
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Статистика",
                callback_data=AdminCallbacks.STATISTICS,
            )
        ],
        [
            InlineKeyboardButton(
                "⚙️ Настройки",
                callback_data=AdminCallbacks.SETTINGS,
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
