import logging
import smtplib

from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.settings import settings
from app.models.application import Application


logger = logging.getLogger(__name__)


TEMPLATE_PATH = Path("app/templates/new_application.html")


class EmailService:
    """Сервис отправки Email уведомлений."""

    def _render_template(
        self,
        application: Application,
    ) -> str:
        """Подготавливает HTML шаблон."""

        html = TEMPLATE_PATH.read_text(
            encoding="utf-8"
        )

        html = html.replace(
            "{{id}}",
            str(application.id),
        )

        html = html.replace(
            "{{date}}",
            application.date,
        )

        html = html.replace(
            "{{name}}",
            application.name,
        )

        html = html.replace(
            "{{phone}}",
            application.phone,
        )

        html = html.replace(
            "{{description}}",
            application.description,
        )

        html = html.replace(
            "{{status}}",
            application.status,
        )

        return html

    def send_new_application(
        self,
        application: Application,
    ) -> bool:
        """Отправляет HTML письмо."""

        try:

            message = MIMEMultipart("alternative")

            message["From"] = settings.email_login
            message["To"] = settings.email_receiver
            message["Subject"] = (
                f"🆕 Новая заявка №{application.id}"
            )

            html = self._render_template(
                application,
            )

            message.attach(
                MIMEText(
                    html,
                    "html",
                    "utf-8",
                )
            )

            with smtplib.SMTP(
                settings.smtp_server,
                settings.smtp_port,
            ) as server:

                server.ehlo()

                server.starttls()

                server.ehlo()

                server.login(
                    settings.email_login,
                    settings.email_password,
                )

                server.send_message(message)

            logger.info(
                f"Email успешно отправлен (#{application.id})"
            )

            return True

        except Exception:

            logger.exception(
                "Ошибка отправки Email"
            )

            return False


email_service = EmailService()