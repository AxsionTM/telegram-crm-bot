from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Settings:
    """Настройки приложения."""

    bot_token: str
    owner_id: int

    # Email
    email_login: str
    email_password: str
    email_receiver: str

    # SMTP
    smtp_server: str
    smtp_port: int


settings = Settings(
    bot_token=os.getenv("BOT_TOKEN", ""),
    owner_id=int(os.getenv("OWNER_ID", "0")),

    email_login=os.getenv("EMAIL_LOGIN", ""),
    email_password=os.getenv("EMAIL_PASSWORD", ""),
    email_receiver=os.getenv("EMAIL_RECEIVER", ""),

    smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    smtp_port=int(os.getenv("SMTP_PORT", "587")),
)