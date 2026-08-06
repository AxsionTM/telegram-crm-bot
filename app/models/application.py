from dataclasses import dataclass


@dataclass(slots=True)
class Application:
    """Модель заявки."""

    id: int
    date: str

    name: str
    phone: str
    description: str

    status: str