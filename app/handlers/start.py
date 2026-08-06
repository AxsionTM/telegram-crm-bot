from telegram import Update
from telegram.ext import ContextTypes

from app.keyboards.main_menu import get_main_menu


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Команда /start."""

    await update.message.reply_text(
        text=(
            "👋 Добро пожаловать!\n\n"
            "Это CRM-система для приёма заявок.\n\n"
            "Выберите действие:"
        ),
        reply_markup=get_main_menu(),
    )
