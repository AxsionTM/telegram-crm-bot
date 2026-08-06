from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook

from app.models.application import Application


DATA_DIR = Path("app/data")
EXCEL_FILE = DATA_DIR / "applications.xlsx"


class ExcelStorage:
    """Работа с Excel-файлом заявок."""

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

    def create(
        self,
        name: str,
        phone: str,
        description: str,
    ) -> Application:

        workbook = self._load()
        sheet = workbook.active

        application = Application(
            id=self.get_next_id(),
            date=datetime.now().strftime("%d.%m.%Y %H:%M"),
            name=name,
            phone=phone,
            description=description,
            status="NEW",
        )

        sheet.append(
            [
                application.id,
                application.date,
                application.name,
                application.phone,
                application.description,
                application.status,
            ]
        )

        workbook.save(EXCEL_FILE)

        return application

    def get_all(self) -> list[Application]:

        workbook = self._load()
        sheet = workbook.active

        applications = []

        for row in sheet.iter_rows(min_row=2, values_only=True):

            applications.append(
                Application(
                    id=row[0],
                    date=row[1],
                    name=row[2],
                    phone=row[3],
                    description=row[4],
                    status=row[5],
                )
            )

        return applications

    def get_by_id(
        self,
        application_id: int,
    ) -> Application | None:

        applications = self.get_all()

        for application in applications:

            if application.id == application_id:
                return application

        return None