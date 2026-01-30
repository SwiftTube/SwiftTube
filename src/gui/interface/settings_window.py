import customtkinter as ctk
from PIL import Image

from gui.widgets.settings_option import (
    SettingSelectionOptionWidget,
    SettingPathSelectionWidget,
    SettingSwitchOptionWidget
)

from gui.widgets.update_message import UpdateMessageWidget

from core.settings_manager import get_setting_value, set_setting_value
from core.language_manager import language_manager
from core.metadata import is_there_a_new_release
from core.utils import resource_path

class SettingsInterface(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            master = parent,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.language_manager = language_manager
        self.language_manager.subscribe(self.update_language)

        self.update_message_widget = UpdateMessageWidget(parent = self)

        if is_there_a_new_release():
            self.update_message_widget.pack(
                side = "top",
                fill = "x",
                padx = 10,
                pady = 5
            )

        self.settings_scrollable_frame = ctk.CTkScrollableFrame(
            master = self,
            scrollbar_button_hover_color = ["#A4A4A4", "#4C5158"],
            scrollbar_button_color = ["#D9D9D9", "#282B30"],
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.settings_scrollable_frame.pack(
            side = "left",
            fill = "both",
            expand = True,
            padx = 10
        )

        moon_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/feather/moon_icon_light.png")),
            dark_image = Image.open(resource_path("assets/icons/feather/moon_icon_dark.png")),
            size = (15, 15)
        )

        film_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/feather/film_icon_light.png")),
            dark_image = Image.open(resource_path("assets/icons/feather/film_icon_dark.png")),
            size = (15, 15)
        )

        search_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/feather/globe_icon_light.png")),
            dark_image = Image.open(resource_path("assets/icons/feather/globe_icon_dark.png")),
            size = (15, 15)
        )

        search_limit_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/material/search_limit_icon_light.png")),
            dark_image = Image.open(resource_path("assets/icons/material/search_limit_icon_dark.png")),
            size = (18, 14)
        )

        path_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/material/path_icon_light.png")),
            dark_image = Image.open(resource_path("assets/icons/material/path_icon_dark.png")),
            size = (18, 18)
        )

        self.general_settings_title_frame = ctk.CTkFrame(
            master = self.settings_scrollable_frame,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.general_settings_title_frame.pack(side = "top", fill = "x")

        self.settings_title_label = ctk.CTkLabel(
            master = self.general_settings_title_frame,
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            text = self.language_manager.get_text("general_settings"),

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 20
            )
        )

        self.settings_title_label.pack(side = "left", padx = 10, pady = 10)

        def change_language_option_command():
            new_value = self.change_language_option.get_option_value()
            self.language_manager.set_language(self.language_manager.language_map[new_value])
            set_setting_value("general_settings", "language", value = self.language_manager.language_map[new_value])

        self.change_language_option = SettingSelectionOptionWidget(
            parent = self.settings_scrollable_frame,
            description = self.language_manager.get_text("change_language_desc"),
            options = list(self.language_manager.language_map.keys()),
            icon = search_icon,
            name = self.language_manager.get_text("language"),
            button_command = change_language_option_command,
            default_value = self.language_manager.get_language_name(self.language_manager.current_language)
        )

        self.change_language_option.pack(fill = "x", padx = 10, pady = 5)

        self.appearance_settings_title_frame = ctk.CTkFrame(
            master = self.settings_scrollable_frame,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.appearance_settings_title_frame.pack(side = "top", fill = "x")

        self.appearance_title_label = ctk.CTkLabel(
            master = self.appearance_settings_title_frame,
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            text = self.language_manager.get_text("appearance_settings"),

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 20
            )
        )

        self.appearance_title_label.pack(side = "left", padx = 10, pady = 10)

        def change_application_theme():
            if get_setting_value("appearance_settings", "dark_theme"):
                ctk.set_appearance_mode("light")
                new_value = False

            else:
                ctk.set_appearance_mode("dark")
                new_value = True

            set_setting_value("appearance_settings", "dark_theme", value = new_value)

        self.dark_theme_option = SettingSwitchOptionWidget(
            parent = self.settings_scrollable_frame,
            icon = moon_icon,
            name = self.language_manager.get_text("dark_theme"),
            description = self.language_manager.get_text("dark_theme_desc"),
            button_command = change_application_theme
        )

        self.dark_theme_option.toggle_switch(
            state = get_setting_value(
                category = "appearance_settings",
                setting = "dark_theme"
            )
        )

        self.dark_theme_option.pack(fill = "x", padx = 10, pady = 5)

        self.video_settings_title_frame = ctk.CTkFrame(
            master = self.settings_scrollable_frame,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.video_settings_title_frame.pack(side = "top", fill = "x")

        self.video_title_label = ctk.CTkLabel(
            master = self.video_settings_title_frame,
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            text = self.language_manager.get_text("download_settings"),

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 20
            )
        )

        self.video_title_label.pack(side = "left", padx = 10, pady = 10)

        self.download_path_selection = SettingPathSelectionWidget(
           parent = self.settings_scrollable_frame,
           icon = path_icon,
           name = self.language_manager.get_text("download_path"),
           description = self.language_manager.get_text("download_path_desc"),
           default_path = get_setting_value("download_settings", "download_path")
        )

        self.download_path_selection.pack(fill = "x", padx = 10, pady = 5)

        self.search_settings_title_frame = ctk.CTkFrame(
            master = self.settings_scrollable_frame,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.search_settings_title_frame.pack(side = "top", fill = "x")

        self.search_title_label = ctk.CTkLabel(
            master = self.search_settings_title_frame,
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            text = self.language_manager.get_text("search_settings"),

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 20
            )
        )

        self.search_title_label.pack(side = "left", padx = 10, pady = 10)

        def search_limit_option_command():
            new_value = int(self.search_limit_option.get_option_value())
            set_setting_value("search_settings", "search_limit", value = new_value)

        self.search_limit_option = SettingSelectionOptionWidget(
            parent = self.settings_scrollable_frame,
            icon = search_limit_icon,
            name = self.language_manager.get_text("search_limit"),
            description = self.language_manager.get_text("search_limit_desc"),
            button_command = search_limit_option_command,
            options = [str(i) for i in range(10, 0, -1)]
        )

        self.search_limit_option.pack(fill = "x", padx = 10, pady = 5)

        self.search_limit_option.change_option_value(
            value = get_setting_value("search_settings", "search_limit")
        )

        def load_video_thumbnail_option_command():
            if get_setting_value("search_settings", "load_video_thumbnail"):
                new_value = False

            else:
                new_value = True

            set_setting_value("search_settings", "load_video_thumbnail", value = new_value)

        self.load_video_thumbnail_option = SettingSwitchOptionWidget(
            parent = self.settings_scrollable_frame,
            icon = film_icon,
            name = self.language_manager.get_text("load_thumbnail"),
            description = self.language_manager.get_text("load_thumbnail_desc"),
            button_command = load_video_thumbnail_option_command
        )

        self.load_video_thumbnail_option.toggle_switch(
            state = get_setting_value(
                category = "search_settings",
                setting = "load_video_thumbnail"
            )
        )

        self.load_video_thumbnail_option.pack(fill = "x", padx = 10, pady = 5)
    
    def update_language(self):
        self.appearance_title_label.configure(text = self.language_manager.get_text("appearance_settings"))
        self.settings_title_label.configure(text = self.language_manager.get_text("general_settings"))
        self.video_title_label.configure(text = self.language_manager.get_text("download_settings"))
        self.search_title_label.configure(text = self.language_manager.get_text("search_settings"))

        self.change_language_option.configure(
            title = self.language_manager.get_text("language"),
            description = self.language_manager.get_text("change_language_desc")
        )

        self.dark_theme_option.configure(
            title = self.language_manager.get_text("dark_theme"),
            description = self.language_manager.get_text("dark_theme_desc")
        )

        self.download_path_selection.configure(
            title = self.language_manager.get_text("download_path"),
            description = self.language_manager.get_text("download_path_desc")
        )

        self.search_limit_option.configure(
            title = self.language_manager.get_text("search_limit"),
            description = self.language_manager.get_text("search_limit_desc")
        )
