from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.callbacks import AdminCallbacks
from app.storage.settings_storage import settings_storage


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


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Меню настроек CRM."""

    keyboard = [
        [
            InlineKeyboardButton(
                "📥 Экспорт Excel",
                callback_data=AdminCallbacks.EXPORT_EXCEL,
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 Очистка базы",
                callback_data=AdminCallbacks.CLEAR_DB,
            )
        ],
        [
            InlineKeyboardButton(
                "📧 SMTP-настройки",
                callback_data=AdminCallbacks.SMTP_SETTINGS,
            )
        ],
        [
            InlineKeyboardButton(
                "🔔 Уведомления",
                callback_data=AdminCallbacks.TELEGRAM_NOTIFY,
            )
        ],
        [
            InlineKeyboardButton(
                "👤 Администраторы",
                callback_data=AdminCallbacks.ADMIN_MANAGE,
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 Главное меню",
                callback_data=AdminCallbacks.BACK,
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_notifications_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура управления уведомлениями."""

    bot_settings = settings_storage.get()

    tg_status = "✅ Вкл" if bot_settings.get("telegram_notifications", True) else "❌ Выкл"
    email_status = "✅ Вкл" if bot_settings.get("email_notifications", True) else "❌ Выкл"

    keyboard = [
        [
            InlineKeyboardButton(
                f"📱 Telegram: {tg_status}",
                callback_data=AdminCallbacks.TOGGLE_TELEGRAM,
            )
        ],
        [
            InlineKeyboardButton(
                f"📧 Email: {email_status}",
                callback_data=AdminCallbacks.TOGGLE_EMAIL,
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Назад",
                callback_data=AdminCallbacks.SETTINGS,
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_clear_db_confirm_keyboard() -> InlineKeyboardMarkup:
    """Подтверждение очистки базы."""

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Да, очистить",
                callback_data=AdminCallbacks.CLEAR_DB_CONFIRM,
            ),
            InlineKeyboardButton(
                "❌ Отмена",
                callback_data=AdminCallbacks.SETTINGS,
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
