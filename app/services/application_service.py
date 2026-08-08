
from app.services.excel_service import excel_service
from app.models.filter_state import FilterState


class ApplicationService:
    """Работа с заявками CRM."""

    def get_filtered(
        self,
        filters: FilterState,
    ):

        applications = excel_service.get_all()

        # ----------------------------
        # Поиск по ID
        # ----------------------------

        if filters.search_id:

            applications = [
                application
                for application in applications
                if str(application.id) == filters.search_id
            ]

        # ----------------------------
        # Поиск по имени
        # ----------------------------

        if filters.search_name:

            applications = [
                application
                for application in applications
                if filters.search_name.lower()
                in application.name.lower()
            ]

        # ----------------------------
        # Поиск по телефону
        # ----------------------------

        if filters.search_phone:

            applications = [
                application
                for application in applications
                if filters.search_phone
                in application.phone
            ]

        # ----------------------------
        # Статусы
        # ----------------------------

        if filters.statuses:

            applications = [
                application
                for application in applications
                if application.status in filters.statuses
            ]

        return applications

    # ------------------------------------

    def get_page(
        self,
        applications,
        page: int,
        page_size: int = 10,
    ):

        start = (page - 1) * page_size

        end = start + page_size

        return applications[start:end]

    # ------------------------------------

    def pages_count(
        self,
        applications,
        page_size: int = 10,
    ):

        if not applications:

            return 1

        return (len(applications) + page_size - 1) // page_size


application_service = ApplicationService()