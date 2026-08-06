from telegram.ext import (
    Application,
    CommandHandler,
)

from app.config.settings import settings
from app.handlers.start import start
from app.utils.logger import setup_logger


def main() -> None:
    """Запуск Telegram CRM Bot."""

    setup_logger()

    app = Application.builder().token(settings.bot_token).build()

    # Команда /start
    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    print("✅ Telegram CRM Bot started.")

    app.run_polling()


if __name__ == "__main__":
    main()