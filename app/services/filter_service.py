from app.models.filter_state import FilterState


class FilterService:
    """Управление фильтрами CRM."""

    def __init__(self):

        self.filters: dict[int, FilterState] = {}

    def get(
        self,
        user_id: int,
    ) -> FilterState:

        if user_id not in self.filters:

            self.filters[user_id] = FilterState()

        return self.filters[user_id]

    def clear(
        self,
        user_id: int,
    ):

        self.filters[user_id] = FilterState()


filter_service = FilterService()