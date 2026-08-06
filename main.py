from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.config.settings import settings

from app.handlers.start import start
from app.handlers.application import (
    start_application,
    get_name,
    get_phone,
    get_description,
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

    app = Application.builder().token(
        settings.bot_token
    ).build()

    # /start
    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    # Диалог оформления заявки
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

    print("✅ Telegram CRM Bot started.")

    app.run_polling()


if __name__ == "__main__":
    main()