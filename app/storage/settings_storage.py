import json
from pathlib import Path


DATA_DIR = Path("app/data")
SETTINGS_FILE = DATA_DIR / "bot_settings.json"

DEFAULT_SETTINGS = {
    "telegram_notifications": True,
    "email_notifications": True,
}


class SettingsStorage:
    """Хранение настроек бота (уведомления и т.д.)."""

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not SETTINGS_FILE.exists():
            self._save(DEFAULT_SETTINGS.copy())

    def _load(self) -> dict:
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # На случай старых файлов — подставляем значения по умолчанию
                for key, value in DEFAULT_SETTINGS.items():
                    data.setdefault(key, value)
                return data
        except Exception:
            return DEFAULT_SETTINGS.copy()

    def _save(self, data: dict) -> None:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get(self) -> dict:
        return self._load()

    def set(self, key: str, value) -> dict:
        data = self._load()
        data[key] = value
        self._save(data)
        return data

    def toggle(self, key: str) -> dict:
        data = self._load()
        data[key] = not data.get(key, True)
        self._save(data)
        return data


settings_storage = SettingsStorage()
