from telegram import Bot

from app.config.settings import settings
from app.models.application import Application


class TelegramService:
    """Отправка уведомлений в Telegram."""

    async def send_new_application(
        self,
        application: Application,
    ):

        bot = Bot(settings.bot_token)

        text = (
            "🆕 Новая заявка\n\n"
            f"🆔 #{application.id}\n\n"
            f"👤 {application.name}\n\n"
            f"📞 {application.phone}\n\n"
            f"📝\n{application.description}\n\n"
            f"📌 {application.status}"
        )

        await bot.send_message(
            chat_id=settings.owner_id,
            text=text,
        )


telegram_service = TelegramService()