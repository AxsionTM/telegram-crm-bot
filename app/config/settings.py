from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Settings:
    bot_token: str
    owner_id: int

    email_address: str
    email_password: str

    smtp_server: str
    smtp_port: int


settings = Settings(
    bot_token=os.getenv("BOT_TOKEN", ""),
    owner_id=int(os.getenv("OWNER_ID", "0")),

    email_address=os.getenv("EMAIL_ADDRESS", ""),
    email_password=os.getenv("EMAIL_PASSWORD", ""),

    smtp_server=os.getenv("SMTP_SERVER", ""),
    smtp_port=int(os.getenv("SMTP_PORT", "587")),
)