import os

from core.settings_manager import create_template_file, SETTINGS_FILE, APP_FOLDER

from gui.window import App

if __name__ == "__main__":
    if not os.path.exists(APP_FOLDER):
        os.mkdir(APP_FOLDER)

    if not os.path.exists(SETTINGS_FILE):
        create_template_file(SETTINGS_FILE)

    aplication_object = App()
