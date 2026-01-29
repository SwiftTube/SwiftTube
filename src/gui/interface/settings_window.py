import customtkinter as ctk
from PIL import Image

from gui.widgets.settings_option import (
    SettingSelectionOptionWidget,
    SettingPathSelectionWidget,
    SettingSwitchOptionWidget
)

from core.settings_manager import get_setting_value, set_setting_value
from core.language_manager import language_manager
from core.utils import resource_path

class SettingsInterface(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            master = parent,
            fg_color = ["#FAFAFA", "#1E2124"]
        )
        
        language_manager.subscribe(self.update_language)

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

        # quality_icon = ctk.CTkImage(
        #     light_image = Image.open(resource_path("assets/icons/material/quality_icon_light.png")),
        #     dark_image = Image.open(resource_path("assets/icons/material/quality_icon_dark.png")),
        #     size = (18, 18)
        # )

        # auto_download_icon = ctk.CTkImage(
        #     light_image = Image.open(resource_path("assets/icons/material/auto_download_icon_light.png")),
        #     dark_image = Image.open(resource_path("assets/icons/material/auto_download_icon_dark.png")),
        #     size = (18, 18)
        # )

        # reload_download_icon = ctk.CTkImage(
        #     light_image = Image.open(resource_path("assets/icons/material/reload_download_icon_light.png")),
        #     dark_image = Image.open(resource_path("assets/icons/material/reload_download_icon_dark.png")),
        #     size = (18, 18)
        # )

        search_limit_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/material/search_limit_icon_light.png")),
            dark_image = Image.open(resource_path("assets/icons/material/search_limit_icon_dark.png")),
            size = (18, 14)
        )

        # oled_icon = ctk.CTkImage(
        #     light_image = Image.open(resource_path("assets/icons/material/oled_icon_light.png")),
        #     dark_image = Image.open(resource_path("assets/icons/material/oled_icon_dark.png")),
        #     size = (18, 18)
        # )

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
            text = language_manager.get_text("general_settings"),

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 20
            )
        )

        self.settings_title_label.pack(side = "left", padx = 10, pady = 10)

        def change_language_option_command():
            new_value = self.change_language_option.get_option_value()
            language_manager.set_language(language_manager.language_map[new_value])
            set_setting_value("general_settings", "language", value = language_manager.language_map[new_value])

        self.change_language_option = SettingSelectionOptionWidget(
            parent = self.settings_scrollable_frame,
            description = language_manager.get_text("change_language_desc"),
            options = list(language_manager.language_map.keys()),
            icon = search_icon,
            name = language_manager.get_text("language"),
            button_command = change_language_option_command,
            default_value = language_manager.get_language_name(language_manager.current_language)
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
            text = language_manager.get_text("appearance_settings"),

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
            name = language_manager.get_text("dark_theme"),
            description = language_manager.get_text("dark_theme_desc"),
            button_command = change_application_theme
        )

        self.dark_theme_option.toggle_switch(
            state = get_setting_value(
                category = "appearance_settings",
                setting = "dark_theme"
            )
        )

        self.dark_theme_option.pack(fill = "x", padx = 10, pady = 5)

        # oled_mode_option = SettingSwitchOptionWidget(
        #     parent = settings_scrollable_frame,
        #     icon = oled_icon,
        #     name = "OLED mode",
        #     description = "Makes the app dark theme pitch black",
        #     button_command = None
        # )

        # oled_mode_option.pack(fill = "x", padx = 10, pady = 5)

        self.video_settings_title_frame = ctk.CTkFrame(
            master = self.settings_scrollable_frame,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.video_settings_title_frame.pack(side = "top", fill = "x")

        self.video_title_label = ctk.CTkLabel(
            master = self.video_settings_title_frame,
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            text = language_manager.get_text("download_settings"),

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
           name = language_manager.get_text("download_path"),
           description = language_manager.get_text("download_path_desc"),
           default_path = get_setting_value("download_settings", "download_path")
        )

        self.download_path_selection.pack(fill = "x", padx = 10, pady = 5)

        # def download_quality_option_command():
        #     new_value = download_quality_option.get_option_value()
        #     set_setting_value("download_settings", "default_download_quality", value = new_value)

        # download_quality_option = SettingSelectionOptionWidget(
        #     parent = settings_scrollable_frame,
        #     icon = quality_icon,
        #     name = "Default download quality",
        #     description = "Select the default quality when downloading",
        #     button_command = download_quality_option_command,
        #     options = ["Highest quality", "Lowest quality", "Audio only"]
        # )

        # download_quality_option.pack(fill = "x", padx = 10, pady = 5)

        # download_quality_option.change_option_value(
        #     value = get_setting_value("download_settings", "default_download_quality")
        # )

        # automatic_download_option = SettingSwitchOptionWidget(
        #     parent = settings_scrollable_frame,
        #     icon = auto_download_icon,
        #     name = "Automatic download",
        #     description = "Enable automatic download for added videos",
        #     button_command = None
        # )

        # automatic_download_option.pack(fill = "x", padx = 10, pady = 5)

        # def reload_download_option_command():
        #     if get_setting_value("download_settings", "reload_download"):
        #         new_value = False

        #     else:
        #         new_value = True

        #     set_setting_value("download_settings", "reload_download", value = new_value)

        # reload_download_option = SettingSwitchOptionWidget(
        #     parent = settings_scrollable_frame,
        #     icon = reload_download_icon,
        #     name = "Reload download",
        #     description = "Reload download when videos fail downloading",
        #     button_command = reload_download_option_command
        # )

        # reload_download_option.toggle_switch(
        #     state = get_setting_value(
        #         category = "download_settings",
        #         setting = "reload_download"
        #     )
        # )

        # reload_download_option.pack(fill = "x", padx = 10, pady = 5)

        self.search_settings_title_frame = ctk.CTkFrame(
            master = self.settings_scrollable_frame,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.search_settings_title_frame.pack(side = "top", fill = "x")

        self.search_title_label = ctk.CTkLabel(
            master = self.search_settings_title_frame,
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            text = language_manager.get_text("search_settings"),

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
            name = language_manager.get_text("search_limit"),
            description = language_manager.get_text("search_limit_desc"),
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
            name = language_manager.get_text("load_thumbnail"),
            description = language_manager.get_text("load_thumbnail_desc"),
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
        self.appearance_title_label.configure(text = language_manager.get_text("appearance_settings"))
        self.settings_title_label.configure(text = language_manager.get_text("general_settings"))
        self.video_title_label.configure(text = language_manager.get_text("download_settings"))
        self.search_title_label.configure(text = language_manager.get_text("search_settings"))

        self.change_language_option.configure(
            title = language_manager.get_text("language"),
            description = language_manager.get_text("change_language_desc")
        )

        self.dark_theme_option.configure(
            title = language_manager.get_text("dark_theme"),
            description = language_manager.get_text("dark_theme_desc")
        )

        self.download_path_selection.configure(
            title = language_manager.get_text("download_path"),
            description = language_manager.get_text("download_path_desc")
        )

        self.search_limit_option.configure(
            title = language_manager.get_text("search_limit"),
            description = language_manager.get_text("search_limit_desc")
        )

        self.load_video_thumbnail_option.configure(
            title = language_manager.get_text("load_thumbnail"),
            description = language_manager.get_text("load_thumbnail_desc")
        )
        