from dataclasses import dataclass, field


@dataclass
class FilterState:
    """Текущее состояние фильтров CRM."""

    page: int = 1

    search_id: str = ""

    search_name: str = ""

    search_phone: str = ""

    statuses: set[str] = field(default_factory=set)