class AdminCallbacks:
    """Константы callback_data для админ-панели."""

    # Главное меню
    APPLICATIONS = "applications"
    STATISTICS = "statistics"
    SETTINGS = "settings"
    BACK = "back"

    # Пагинация
    NEXT_PAGE = "next_page"
    PREV_PAGE = "prev_page"

    # Поиск
    SEARCH_MENU = "search_menu"
    SEARCH_ID = "search_id"
    SEARCH_NAME = "search_name"
    SEARCH_PHONE = "search_phone"

    # Фильтры
    FILTER_MENU = "filter_menu"
    FILTER_ALL = "filter_all"
    FILTER_NEW = "filter_new"
    FILTER_PROGRESS = "filter_progress"
    FILTER_DONE = "filter_done"
    FILTER_CANCELLED = "filter_cancelled"
    CLEAR_FILTERS = "clear_filters"

    # Настройки
    EXPORT_EXCEL = "export_excel"
    CLEAR_DB = "clear_db"
    CLEAR_DB_CONFIRM = "clear_db_confirm"
    SMTP_SETTINGS = "smtp_settings"
    TELEGRAM_NOTIFY = "telegram_notify"
    ADMIN_MANAGE = "admin_manage"

    # Переключатели уведомлений
    TOGGLE_TELEGRAM = "toggle_telegram"
    TOGGLE_EMAIL = "toggle_email"

    # Прочее
    IGNORE = "ignore"
