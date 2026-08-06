from telegram import Update
from telegram.ext import ContextTypes


async def contacts(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Раздел контактов."""

    text = (
        "ℹ️ Контактная информация\n\n"
        "📞 Телефон:\n"
        "+7 (999) 999-99-99\n\n"
        "📧 Email:\n"
        "example@gmail.com\n\n"
        "💬 Telegram:\n"
        "@username\n\n"
        "🕒 Работаем ежедневно\n"
        "09:00 — 21:00"
    )

    await update.message.reply_text(text)