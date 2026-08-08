from telegram import Bot
from telegram.constants import ParseMode

from app.config.settings import settings
from app.models.application import Application


class TelegramService:
    """Отправка уведомлений в Telegram."""

    async def send_new_application(self, application: Application) -> None:
        bot = Bot(settings.bot_token)

        text = (
            "🆕 <b>Новая заявка</b>\n"
            "━━━━━━━━━━━━━━\n\n"
            f"🆔 <b>№{application.id}</b>\n"
            f"👤 <b>Имя:</b> {application.name}\n"
            f"📞 <b>Телефон:</b> {application.phone}\n\n"
            f"📝 <b>Описание:</b>\n"
            f"{application.description}\n\n"
            f"📌 <b>Статус:</b> {application.status}\n"
            f"📅 <b>Дата:</b> {application.date}"
        )

        await bot.send_message(
            chat_id=settings.owner_id,
            text=text,
            parse_mode=ParseMode.HTML,
        )


telegram_service = TelegramService()
