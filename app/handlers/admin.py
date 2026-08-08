from pathlib import Path

from telegram import Update, InputFile
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.config.settings import settings
from app.keyboards.admin_inline import (
    get_admin_panel,
    get_settings_keyboard,
    get_clear_db_confirm_keyboard,
)
from app.keyboards.application_list import (
    get_application_list_keyboard,
    get_search_keyboard,
    get_filter_keyboard,
    get_application_keyboard,
)
from app.services.application_service import application_service
from app.services.excel_service import excel_service
from app.services.filter_service import filter_service
from app.utils.application_formatter import (
    format_application_list,
    format_application_detail,
)
from app.utils.callbacks import AdminCallbacks


# ============================================================
# Главное меню админки
# ============================================================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /admin — вход в CRM-панель."""

    if update.effective_user.id != settings.owner_id:
        await update.message.reply_text("⛔ У вас нет доступа.")
        return

    filter_service.clear(update.effective_user.id)

    await update.message.reply_text(
        text=(
            "👨‍💼 <b>CRM Панель администратора</b>\n\n"
            "Добро пожаловать.\n\n"
            "Выберите необходимый раздел."
        ),
        reply_markup=get_admin_panel(),
        parse_mode=ParseMode.HTML,
    )


# ============================================================
# Основной обработчик inline-кнопок
# ============================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка всех callback-кнопок админ-панели."""

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id != settings.owner_id:
        await query.answer("Нет доступа.", show_alert=True)
        return

    data = query.data

    # ---------- Главное меню ----------
    if data == AdminCallbacks.BACK:
        filter_service.clear(user_id)
        await query.edit_message_text(
            text=(
                "👨‍💼 <b>CRM Панель администратора</b>\n\n"
                "Добро пожаловать.\n\n"
                "Выберите раздел."
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=get_admin_panel(),
        )
        return

    # ---------- Список заявок ----------
    if data == AdminCallbacks.APPLICATIONS:
        await _show_applications(query, user_id)
        return

    # ---------- Пагинация ----------
    if data == AdminCallbacks.NEXT_PAGE:
        filters = filter_service.get(user_id)
        applications = application_service.get_filtered(filters)
        total_pages = application_service.pages_count(applications)

        if filters.page < total_pages:
            filters.page += 1

        await _show_applications(query, user_id)
        return

    if data == AdminCallbacks.PREV_PAGE:
        filters = filter_service.get(user_id)

        if filters.page > 1:
            filters.page -= 1

        await _show_applications(query, user_id)
        return

    # ---------- Статистика ----------
    if data == AdminCallbacks.STATISTICS:
        applications = excel_service.get_all()

        total = len(applications)
        new_count = sum(1 for a in applications if a.status == "Новая")
        progress_count = sum(1 for a in applications if a.status == "В работе")
        done_count = sum(1 for a in applications if a.status == "Завершена")
        cancelled_count = sum(1 for a in applications if a.status == "Отменена")

        await query.edit_message_text(
            text=(
                "📊 <b>Статистика CRM</b>\n\n"
                f"📋 Всего заявок: <b>{total}</b>\n\n"
                f"🟢 Новые: <b>{new_count}</b>\n"
                f"🟡 В работе: <b>{progress_count}</b>\n"
                f"✅ Завершённые: <b>{done_count}</b>\n"
                f"❌ Отменённые: <b>{cancelled_count}</b>"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=get_admin_panel(),
        )
        return

    # ---------- Настройки (меню) ----------
    if data == AdminCallbacks.SETTINGS:
        await query.edit_message_text(
            text=(
                "⚙️ <b>Настройки CRM</b>\n\n"
                "Выберите раздел настроек."
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=get_settings_keyboard(),
        )
        return

    # ---------- Экспорт Excel ----------
    if data == AdminCallbacks.EXPORT_EXCEL:
        file_path = excel_service.get_file_path()

        if not file_path.exists():
            await query.answer("Файл не найден.", show_alert=True)
            return

        applications = excel_service.get_all()

        with open(file_path, "rb") as document_file:
            await query.message.reply_document(
                document=InputFile(document_file, filename="applications.xlsx"),
                caption=(
                    f"📥 <b>Экспорт заявок</b>\n\n"
                    f"Всего записей: <b>{len(applications)}</b>"
                ),
                parse_mode=ParseMode.HTML,
            )

        await query.answer("Файл отправлен ✅")
        return

    # ---------- Очистка базы (подтверждение) ----------
    if data == AdminCallbacks.CLEAR_DB:
        count = len(excel_service.get_all())

        await query.edit_message_text(
            text=(
                "🗑 <b>Очистка базы</b>\n\n"
                f"Сейчас в базе: <b>{count}</b> заявок.\n\n"
                "⚠️ Это действие <b>нельзя отменить</b>.\n"
                "Все заявки будут удалены.\n\n"
                "Вы уверены?"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=get_clear_db_confirm_keyboard(),
        )
        return

    # ---------- Очистка базы (подтверждено) ----------
    if data == AdminCallbacks.CLEAR_DB_CONFIRM:
        deleted = excel_service.clear_all()

        await query.edit_message_text(
            text=(
                "🗑 <b>База очищена</b>\n\n"
                f"Удалено заявок: <b>{deleted}</b>"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=get_settings_keyboard(),
        )
        return

    # ---------- SMTP-настройки ----------
    if data == AdminCallbacks.SMTP_SETTINGS:
        login = settings.email_login or "—"
        receiver = settings.email_receiver or "—"
        server = settings.smtp_server or "—"
        port = settings.smtp_port or "—"

        await query.edit_message_text(
            text=(
                "📧 <b>SMTP-настройки</b>\n\n"
                f"📤 Отправитель: <code>{login}</code>\n"
                f"📥 Получатель: <code>{receiver}</code>\n"
                f"🖥 Сервер: <code>{server}</code>\n"
                f"🔌 Порт: <code>{port}</code>\n\n"
                "ℹ️ Изменить настройки можно в файле <code>.env</code>"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=get_settings_keyboard(),
        )
        return

    # ---------- Telegram-уведомления ----------
    if data == AdminCallbacks.TELEGRAM_NOTIFY:
        owner = settings.owner_id or "—"

        await query.edit_message_text(
            text=(
                "🔔 <b>Telegram-уведомления</b>\n\n"
                f"Администратор (chat_id): <code>{owner}</code>\n\n"
                "✅ Уведомления о новых заявках <b>включены</b>.\n\n"
                "При создании заявки бот автоматически "
                "отправляет сообщение администратору."
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=get_settings_keyboard(),
        )
        return

    # ---------- Управление администраторами ----------
    if data == AdminCallbacks.ADMIN_MANAGE:
        owner = settings.owner_id or "—"

        await query.edit_message_text(
            text=(
                "👤 <b>Администраторы</b>\n\n"
                f"Текущий администратор:\n"
                f"<code>{owner}</code>\n\n"
                "ℹ️ Сейчас поддерживается один администратор.\n"
                "Изменить можно в файле <code>.env</code> "
                "(переменная <code>OWNER_ID</code>)."
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=get_settings_keyboard(),
        )
        return

    # ---------- Меню поиска ----------
    if data == AdminCallbacks.SEARCH_MENU:
        await query.edit_message_text(
            text="🔎 <b>Поиск заявок</b>\n\nВыберите тип поиска.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_search_keyboard(),
        )
        return

    # ---------- Выбор типа поиска ----------
    if data == AdminCallbacks.SEARCH_ID:
        context.user_data["search_mode"] = "id"
        await query.edit_message_text(
            text="🔎 <b>Поиск по ID</b>\n\nОтправьте номер заявки.",
            parse_mode=ParseMode.HTML,
        )
        return

    if data == AdminCallbacks.SEARCH_NAME:
        context.user_data["search_mode"] = "name"
        await query.edit_message_text(
            text="👤 <b>Поиск по имени</b>\n\nВведите имя клиента.",
            parse_mode=ParseMode.HTML,
        )
        return

    if data == AdminCallbacks.SEARCH_PHONE:
        context.user_data["search_mode"] = "phone"
        await query.edit_message_text(
            text="📞 <b>Поиск по телефону</b>\n\nВведите номер телефона.",
            parse_mode=ParseMode.HTML,
        )
        return

    # ---------- Меню фильтров ----------
    if data == AdminCallbacks.FILTER_MENU:
        await query.edit_message_text(
            text="🎯 <b>Фильтр заявок</b>\n\nВыберите статус.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_filter_keyboard(),
        )
        return

    # ---------- Применение фильтров ----------
    if data == AdminCallbacks.FILTER_ALL:
        filters = filter_service.get(user_id)
        filters.statuses.clear()
        filters.page = 1
        await _show_applications(query, user_id)
        return

    if data == AdminCallbacks.FILTER_NEW:
        await _apply_status_filter(query, user_id, "Новая")
        return

    if data == AdminCallbacks.FILTER_PROGRESS:
        await _apply_status_filter(query, user_id, "В работе")
        return

    if data == AdminCallbacks.FILTER_DONE:
        await _apply_status_filter(query, user_id, "Завершена")
        return

    if data == AdminCallbacks.FILTER_CANCELLED:
        await _apply_status_filter(query, user_id, "Отменена")
        return

    if data == AdminCallbacks.CLEAR_FILTERS:
        filters = filter_service.get(user_id)
        filters.page = 1
        filters.search_id = ""
        filters.search_name = ""
        filters.search_phone = ""
        filters.statuses.clear()
        await _show_applications(query, user_id)
        return

    # ---------- Открытие заявки ----------
    if data.startswith("open:"):
        application_id = int(data.split(":")[1])
        application = excel_service.get_by_id(application_id)

        if not application:
            await query.answer("Заявка не найдена.", show_alert=True)
            return

        await query.edit_message_text(
            text=format_application_detail(application),
            parse_mode=ParseMode.HTML,
            reply_markup=get_application_keyboard(application.id),
        )
        return

    # ---------- Смена статуса ----------
    if data.startswith("status:"):
        parts = data.split(":")
        application_id = int(parts[1])
        status = parts[2]

        application = excel_service.update_status(application_id, status)

        if not application:
            await query.answer("Заявка не найдена.", show_alert=True)
            return

        await query.edit_message_text(
            text=format_application_detail(application),
            parse_mode=ParseMode.HTML,
            reply_markup=get_application_keyboard(application.id),
        )
        await query.answer(f"Статус изменён на «{status}»")
        return

    # ---------- Удаление заявки ----------
    if data.startswith("delete:"):
        application_id = int(data.split(":")[1])
        success = excel_service.delete(application_id)

        if success:
            await query.answer("Заявка удалена.")
            await _show_applications(query, user_id)
        else:
            await query.answer("Не удалось удалить заявку.", show_alert=True)
        return

    # ---------- Игнор (кнопка страницы) ----------
    if data == AdminCallbacks.IGNORE:
        return

    # ---------- Неизвестная команда ----------
    await query.answer("Неизвестная команда.", show_alert=True)


# ============================================================
# Обработчик текстового поиска
# ============================================================

async def search_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает текст, когда админ в режиме поиска."""

    if update.effective_user.id != settings.owner_id:
        return

    search_mode = context.user_data.get("search_mode")
    if not search_mode:
        return

    text = update.message.text.strip()
    filters = filter_service.get(update.effective_user.id)

    filters.search_id = ""
    filters.search_name = ""
    filters.search_phone = ""
    filters.page = 1

    if search_mode == "id":
        filters.search_id = text
    elif search_mode == "name":
        filters.search_name = text
    elif search_mode == "phone":
        filters.search_phone = text

    context.user_data.pop("search_mode", None)

    applications = application_service.get_filtered(filters)
    total_pages = application_service.pages_count(applications)
    page = application_service.get_page(applications, filters.page)

    await update.message.reply_text(
        text=format_application_list(page, filters.page, total_pages),
        parse_mode=ParseMode.HTML,
        reply_markup=get_application_list_keyboard(page, filters.page, total_pages),
    )


# ============================================================
# Вспомогательные функции
# ============================================================

async def _show_applications(query, user_id: int) -> None:
    """Показывает список заявок с учётом текущих фильтров."""

    filters = filter_service.get(user_id)
    applications = application_service.get_filtered(filters)
    total_pages = application_service.pages_count(applications)
    page = application_service.get_page(applications, filters.page)

    await query.edit_message_text(
        text=format_application_list(page, filters.page, total_pages),
        parse_mode=ParseMode.HTML,
        reply_markup=get_application_list_keyboard(page, filters.page, total_pages),
    )


async def _apply_status_filter(query, user_id: int, status: str) -> None:
    """Применяет фильтр по одному статусу."""

    filters = filter_service.get(user_id)
    filters.page = 1
    filters.statuses.clear()
    filters.statuses.add(status)
    await _show_applications(query, user_id)