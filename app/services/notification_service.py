from telegram import Bot

from app.config.settings import settings
from app.models.application import Application


class NotificationService:
    """Отправка уведомлений владельцу."""

    async def send_new_application(
        self,
        application: Application,
    ) -> None:

        bot = Bot(settings.bot_token)

        text = (
            "🆕 Новая заявка\n\n"
            f"🆔 #{application.id}\n"
            f"👤 {application.name}\n"
            f"📞 {application.phone}\n\n"
            f"📝 {application.description}\n\n"
            f"📌 Статус: {application.status}"
        )

        await bot.send_message(
            chat_id=settings.owner_id,
            text=text,
        )


notification_service = NotificationService()