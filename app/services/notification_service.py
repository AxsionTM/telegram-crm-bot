import logging

from app.models.application import Application

from app.services.telegram_service import telegram_service
from app.services.email_service import email_service


logger = logging.getLogger(__name__)


class NotificationService:
    """Центр отправки уведомлений."""

    async def notify(
        self,
        application: Application,
    ) -> None:
        """Отправить все уведомления."""

        # Telegram
        try:
            await telegram_service.send_new_application(
                application,
            )

            logger.info(
                f"Telegram уведомление отправлено (#{application.id})"
            )

        except Exception:
            logger.exception(
                "Ошибка отправки Telegram уведомления"
            )

        # Email
        try:
            success = email_service.send_new_application(
                application,
            )

            if success:
                logger.info(
                    f"Email отправлен (#{application.id})"
                )
            else:
                logger.warning(
                    f"Email не отправлен (#{application.id})"
                )

        except Exception:
            logger.exception(
                "Ошибка отправки Email"
            )


notification_service = NotificationService()