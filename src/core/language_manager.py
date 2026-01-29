from pathlib import Path
import json

from core.settings_manager import get_setting_value
from core.utils import resource_path

class LanguageManager:

    def __init__(self, locales_path = "assets/lang"):
        self.locales_path = Path(resource_path(locales_path))

        try:
            default_language = get_setting_value("general_settings", "language")

        except Exception:
            default_language = "en-EN"

        self.current_language = default_language
        self.translations = {}
        self.subscribers = []

        self.language_map = {
            "English": "en-EN",
            "Español": "es-ES",
            "Français": "fr-FR",
            "Deutsch": "de-DE",
            "Italiano": "it-IT",
            "Português": "pt-PT",
            "Português (Brasil)": "pt-BR",
            "Русский": "ru-RU",
            "中文 (简体)": "zh-CN",
            "日本語": "ja-JP",
            "한국어": "ko-KR",
        }

        self.load_languages()

    def load_languages(self):
        for file in self.locales_path.glob("*.json"):

            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                lang_code = list(data.keys())[0]
                self.translations[lang_code] = data[lang_code]

    def get_language_name(self, lang_code: str) -> str:
        for name, code in self.language_map.items():
            if code == lang_code:
                return name
            
        return "Unknown"

    def set_language(self, lang_code: str):
        if lang_code not in self.translations:
            return

        self.current_language = lang_code
        self.notify_subscribers()

    def get_text(self, key: str) -> str:
        return self.translations[self.current_language].get(key, key)

    def subscribe(self, callback):
        if callback not in self.subscribers:
            self.subscribers.append(callback)

    def notify_subscribers(self):
        for callback in self.subscribers:
            callback()

language_manager = LanguageManager()
