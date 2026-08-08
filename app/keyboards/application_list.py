from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.models.application import Application
from app.utils.callbacks import AdminCallbacks


def get_application_list_keyboard(
    applications: list[Application],
    page: int,
    total_pages: int,
) -> InlineKeyboardMarkup:
    """Клавиатура списка заявок с кнопками открытия каждой заявки."""

    keyboard = []

    # Кнопки заявок текущей страницы
    for app in applications:
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"#{app.id} · {app.name} · {app.status}",
                    callback_data=f"open:{app.id}",
                )
            ]
        )

    # Поиск и фильтр
    keyboard.append(
        [
            InlineKeyboardButton(
                "🔎 Поиск",
                callback_data=AdminCallbacks.SEARCH_MENU,
            ),
            InlineKeyboardButton(
                "🎯 Фильтр",
                callback_data=AdminCallbacks.FILTER_MENU,
            ),
        ]
    )

    # Пагинация
    keyboard.append(
        [
            InlineKeyboardButton(
                "⬅️",
                callback_data=AdminCallbacks.PREV_PAGE,
            ),
            InlineKeyboardButton(
                f"{page}/{total_pages}",
                callback_data=AdminCallbacks.IGNORE,
            ),
            InlineKeyboardButton(
                "➡️",
                callback_data=AdminCallbacks.NEXT_PAGE,
            ),
        ]
    )

    # Назад
    keyboard.append(
        [
            InlineKeyboardButton(
                "🏠 Главное меню",
                callback_data=AdminCallbacks.BACK,
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def get_search_keyboard() -> InlineKeyboardMarkup:
    """Меню выбора типа поиска."""

    keyboard = [
        [
            InlineKeyboardButton(
                "🆔 По ID",
                callback_data=AdminCallbacks.SEARCH_ID,
            )
        ],
        [
            InlineKeyboardButton(
                "👤 По имени",
                callback_data=AdminCallbacks.SEARCH_NAME,
            )
        ],
        [
            InlineKeyboardButton(
                "📞 По телефону",
                callback_data=AdminCallbacks.SEARCH_PHONE,
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Назад",
                callback_data=AdminCallbacks.APPLICATIONS,
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_filter_keyboard() -> InlineKeyboardMarkup:
    """Меню фильтрации по статусу."""

    keyboard = [
        [
            InlineKeyboardButton(
                "📋 Все",
                callback_data=AdminCallbacks.FILTER_ALL,
            )
        ],
        [
            InlineKeyboardButton(
                "🟢 Новая",
                callback_data=AdminCallbacks.FILTER_NEW,
            ),
            InlineKeyboardButton(
                "🟡 В работе",
                callback_data=AdminCallbacks.FILTER_PROGRESS,
            ),
        ],
        [
            InlineKeyboardButton(
                "✅ Завершена",
                callback_data=AdminCallbacks.FILTER_DONE,
            ),
            InlineKeyboardButton(
                "❌ Отменена",
                callback_data=AdminCallbacks.FILTER_CANCELLED,
            ),
        ],
        [
            InlineKeyboardButton(
                "🗑 Сбросить фильтры",
                callback_data=AdminCallbacks.CLEAR_FILTERS,
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Назад",
                callback_data=AdminCallbacks.APPLICATIONS,
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_application_keyboard(application_id: int) -> InlineKeyboardMarkup:
    """Клавиатура детального просмотра заявки."""

    keyboard = [
        [
            InlineKeyboardButton(
                "🟢 Новая",
                callback_data=f"status:{application_id}:Новая",
            ),
            InlineKeyboardButton(
                "🟡 В работе",
                callback_data=f"status:{application_id}:В работе",
            ),
        ],
        [
            InlineKeyboardButton(
                "✅ Завершена",
                callback_data=f"status:{application_id}:Завершена",
            ),
            InlineKeyboardButton(
                "❌ Отменена",
                callback_data=f"status:{application_id}:Отменена",
            ),
        ],
        [
            InlineKeyboardButton(
                "🗑 Удалить",
                callback_data=f"delete:{application_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 К списку",
                callback_data=AdminCallbacks.APPLICATIONS,
            ),
            InlineKeyboardButton(
                "🏠 Меню",
                callback_data=AdminCallbacks.BACK,
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
