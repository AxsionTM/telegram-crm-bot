from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from app.config.settings import settings

from app.handlers.start import start
from app.handlers.contacts import contacts

from app.handlers.application import (
    start_application,
    get_name,
    get_phone,
    get_description,
)

from app.handlers.admin import (
    admin_panel,
    callback_handler,
    search_text_handler,
)

from app.states.application_states import (
    NAME,
    PHONE,
    DESCRIPTION,
)

from app.utils.logger import setup_logger


def main() -> None:
    """Запуск Telegram CRM Bot."""

    setup_logger()

    app = (
        Application.builder()
        .token(settings.bot_token)
        .build()
    )

    # ==========================
    # Команды
    # ==========================

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))

    # ==========================
    # Главное меню
    # ==========================

    app.add_handler(
        MessageHandler(
            filters.Regex("^ℹ️ Контакты$"),
            contacts,
        )
    )

    # ==========================
    # Диалог оформления заявки
    # ==========================

    application_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^📝 Оставить заявку$"),
                start_application,
            )
        ],
        states={
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name,
                )
            ],
            PHONE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_phone,
                )
            ],
            DESCRIPTION: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_description,
                )
            ],
        },
        fallbacks=[],
    )

    app.add_handler(application_handler)

    # ==========================
    # CRM Callback кнопки
    # ==========================

    app.add_handler(CallbackQueryHandler(callback_handler))

    # ==========================
    # Текстовый поиск в админке
    # (работает только когда search_mode установлен)
    # ==========================

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            search_text_handler,
        )
    )

    print("✅ Telegram CRM Bot started.")

    app.run_polling()


if __name__ == "__main__":
    main()
