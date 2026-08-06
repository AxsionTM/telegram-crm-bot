from app.models.application import Application
from app.storage.excel_storage import ExcelStorage


class ExcelService:

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

    def get_by_id(
        self,
        application_id: int,
    ) -> Application | None:

        return self.storage.get_by_id(application_id)


excel_service = ExcelService()