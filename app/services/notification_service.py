import logging

from app.models.application import Application
from app.services.telegram_service import telegram_service
from app.services.email_service import email_service
from app.storage.settings_storage import settings_storage


logger = logging.getLogger(__name__)


class NotificationService:
    """Центр отправки уведомлений."""

    async def notify(self, application: Application) -> None:
        """Отправить уведомления согласно настройкам."""

        bot_settings = settings_storage.get()

        # Telegram
        if bot_settings.get("telegram_notifications", True):
            try:
                await telegram_service.send_new_application(application)
                logger.info(f"Telegram уведомление отправлено (#{application.id})")
            except Exception:
                logger.exception("Ошибка отправки Telegram уведомления")
        else:
            logger.info(f"Telegram уведомления отключены (#{application.id})")

        # Email
        if bot_settings.get("email_notifications", True):
            try:
                success = email_service.send_new_application(application)
                if success:
                    logger.info(f"Email отправлен (#{application.id})")
                else:
                    logger.warning(f"Email не отправлен (#{application.id})")
            except Exception:
                logger.exception("Ошибка отправки Email")
        else:
            logger.info(f"Email уведомления отключены (#{application.id})")


notification_service = NotificationService()
