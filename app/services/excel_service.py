from pathlib import Path

from app.models.application import Application
from app.storage.excel_storage import ExcelStorage


class ExcelService:
    """Сервис работы с заявками через Excel."""

    def __init__(self):
        self.storage = ExcelStorage()

    def create(
        self,
        name: str,
        phone: str,
        description: str,
    ) -> Application:
        return self.storage.create(
            name=name,
            phone=phone,
            description=description,
        )

    def get_all(self) -> list[Application]:
        return self.storage.get_all()

    def get_by_id(self, application_id: int) -> Application | None:
        return self.storage.get_by_id(application_id)

    def update_status(self, application_id: int, status: str) -> Application | None:
        return self.storage.update_status(application_id, status)

    def delete(self, application_id: int) -> bool:
        return self.storage.delete(application_id)

    def clear_all(self) -> int:
        return self.storage.clear_all()

    def get_file_path(self) -> Path:
        return self.storage.get_file_path()


excel_service = ExcelService()
