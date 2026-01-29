# from typing import Literal
import json
import os

APP_FOLDER = os.path.join(os.path.expanduser('~'), "Documents", "SwiftTube")
SETTINGS_FILE = os.path.join(APP_FOLDER, "settings.json")

DEFAULT_DOWNLOADS_FOLDER = os.path.join(APP_FOLDER, "downloads")

settings_template = {
    "settings": {
        "general_settings": {
            "language": "en-EN"
        },

        "appearance_settings": {
            "dark_theme": True,
            "oled_mode": False
        },

        "download_settings": {
            "download_path": DEFAULT_DOWNLOADS_FOLDER,
            "default_download_quality": "Highest quality",
            "automatic_download": False,
            "reload_download": True
        },

        "search_settings": {
            "search_limit": 10,
            "load_video_thumbnail": True
        }
    }
}

def load_file(file_path):
    with open(file_path, "r", encoding = "utf-8") as object_file:
        objects_database = json.load(object_file)
        return objects_database

def save_file(data, file_path):
    with open(file_path, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4)

def create_template_file(file_path):
    save_file(settings_template, file_path = file_path)

def get_setting_value(category, setting):
    settings = load_file(file_path = SETTINGS_FILE)
    return settings["settings"][category][setting]

def set_setting_value(category, setting, value) -> None:
    settings = load_file(file_path = SETTINGS_FILE)
    settings["settings"][category][setting] = value

    save_file(settings, SETTINGS_FILE)

# def get_file_quantity(source: Literal["video", "audio", "playlist"]):
#     path = os.path.join(APP_FOLDER, source.capitalize())
#     files_quantity = len(os.listdir(path))

#     return files_quantity
