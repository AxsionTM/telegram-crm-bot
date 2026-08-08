from app.models.application import Application


def format_application_list(
    applications: list[Application],
    page: int,
    total_pages: int,
) -> str:
    """Форматирует список заявок для сообщения."""

    if not applications:
        return (
            "📋 <b>CRM • Заявки</b>\n\n"
            "❌ Ничего не найдено."
        )

    text = "📋 <b>CRM • Заявки</b>\n\n"

    for app in applications:
        text += (
            f"<b>#{app.id}</b> · {app.name}\n"
            f"📞 {app.phone}\n"
            f"📌 {app.status}\n"
            "──────────────\n"
        )

    text += f"\nСтраница {page} из {total_pages}"
    return text


def format_application_detail(application: Application) -> str:
    """Форматирует детальную карточку заявки."""

    return (
        f"📋 <b>Заявка #{application.id}</b>\n\n"
        f"👤 <b>Имя:</b> {application.name}\n"
        f"📞 <b>Телефон:</b> {application.phone}\n\n"
        f"📝 <b>Описание:</b>\n{application.description}\n\n"
        f"📌 <b>Статус:</b> {application.status}\n"
        f"📅 <b>Дата:</b> {application.date}"
    )
