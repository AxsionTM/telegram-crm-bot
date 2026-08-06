import re


def is_valid_phone(phone: str) -> bool:
    """
    Проверяет корректность номера телефона.
    """

    phone = phone.replace(" ", "")

    pattern = r"^\+?\d{10,15}$"

    return bool(re.fullmatch(pattern, phone))