from telegram import Update
from telegram.ext import ContextTypes

from app.states.application_states import (
    NAME,
    PHONE,
    DESCRIPTION,
    END,
)

from app.keyboards.cancel_keyboard import get_cancel_keyboard
from app.keyboards.main_menu import get_main_menu

from app.utils.validators import is_valid_phone

from app.services.excel_service import excel_service
from app.services.notification_service import notification_service


async def start_application(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Начало оформления заявки."""

    context.user_data.clear()

    await update.message.reply_text(
        text=(
            "📝 Оформление заявки\n\n"
            "Введите ваше имя:"
        ),
        reply_markup=get_cancel_keyboard(),
    )

    return NAME


async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Получение имени."""

    text = update.message.text.strip()

    if text == "⬅️ Отмена":
        context.user_data.clear()

        await update.message.reply_text(
            "❌ Оформление заявки отменено.",
            reply_markup=get_main_menu(),
        )

        return END

    context.user_data["name"] = text

    await update.message.reply_text(
        "📞 Введите номер телефона:"
    )

    return PHONE


async def get_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Получение телефона."""

    text = update.message.text.strip()

    if text == "⬅️ Отмена":
        context.user_data.clear()

        await update.message.reply_text(
            "❌ Оформление заявки отменено.",
            reply_markup=get_main_menu(),
        )

        return END

    if not is_valid_phone(text):
        await update.message.reply_text(
            "❌ Неверный номер телефона.\n\n"
            "Пример:\n"
            "+79991234567"
        )

        return PHONE

    context.user_data["phone"] = text

    await update.message.reply_text(
        "📝 Опишите вашу заявку:"
    )

    return DESCRIPTION


async def get_description(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Получение описания заявки."""

    text = update.message.text.strip()

    if text == "⬅️ Отмена":
        context.user_data.clear()

        await update.message.reply_text(
            "❌ Оформление заявки отменено.",
            reply_markup=get_main_menu(),
        )

        return END

    context.user_data["description"] = text

    # Создаём заявку
    application = excel_service.create(
        name=context.user_data["name"],
        phone=context.user_data["phone"],
        description=context.user_data["description"],
    )

    # Отправляем все уведомления
    await notification_service.notify(application)

    # Сообщение пользователю
    await update.message.reply_text(
        text=(
            f"✅ Заявка №{application.id} успешно создана!\n\n"
            f"👤 Имя: {application.name}\n"
            f"📞 Телефон: {application.phone}\n"
            f"📝 Заявка:\n"
            f"{application.description}\n\n"
            "📨 Мы свяжемся с вами в ближайшее время."
        ),
        reply_markup=get_main_menu(),
    )

    context.user_data.clear()

    return END