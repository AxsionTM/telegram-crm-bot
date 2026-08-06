from app.storage.excel_storage import ExcelStorage


class ExcelService:

    def __init__(self):
        self.storage = ExcelStorage()

    def save_application(
        self,
        name: str,
        phone: str,
        description: str,
    ) -> int:

        return self.storage.save_application(
            name=name,
            phone=phone,
            description=description,
        )


excel_service = ExcelService()