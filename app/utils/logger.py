import logging


def setup_logger() -> None:
    """Настройка логирования проекта."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)