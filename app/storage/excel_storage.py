from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook


DATA_DIR = Path("app/data")
EXCEL_FILE = DATA_DIR / "applications.xlsx"


class ExcelStorage:
    """Работа с Excel файлом заявок."""

    HEADERS = [
        "ID",
        "Date",
        "Name",
        "Phone",
        "Description",
        "Status",
    ]

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._create_if_not_exists()

    def _create_if_not_exists(self):
        if EXCEL_FILE.exists():
            return

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Applications"

        sheet.append(self.HEADERS)

        workbook.save(EXCEL_FILE)

    def _load(self):
        return load_workbook(EXCEL_FILE)

    def get_next_id(self) -> int:
        workbook = self._load()
        sheet = workbook.active

        return sheet.max_row

    def save_application(
        self,
        name: str,
        phone: str,
        description: str,
    ) -> int:

        workbook = self._load()
        sheet = workbook.active

        application_id = self.get_next_id()

        sheet.append(
            [
                application_id,
                datetime.now().strftime("%d.%m.%Y %H:%M"),
                name,
                phone,
                description,
                "NEW",
            ]
        )

        workbook.save(EXCEL_FILE)

        return application_id