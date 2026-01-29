from webbrowser import open as openurl

from CTkToolTip import CTkToolTip
import customtkinter as ctk
from PIL import Image

from core.language_manager import language_manager
from core.utils import resource_path

class SideBarWidget(ctk.CTkFrame):

    def __init__(self, parent, interfaces: list):
        super().__init__(
            master = parent,
            border_color = ("#D9D9D9", "#282B30"),
            fg_color = ("#FAFAFA", "#1E2124"),
            border_width = 0.5,
            corner_radius = 0,
            width = 50
        )

        language_manager.subscribe(self.update_language)

        self.notification_already_active = False
        self.interfaces = interfaces

        explore_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/material/explore_icon_dark.png")),
            dark_image = Image.open(resource_path("assets/icons/material/explore_icon_dark.png")),
            size = (20, 20)
        )

        download_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/feather/download_icon.png")),
            dark_image = Image.open(resource_path("assets/icons/feather/download_icon.png")),
            size = (18, 18)
        )

        github_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/feather/github_icon.png")),
            dark_image = Image.open(resource_path("assets/icons/feather/github_icon.png")),
            size = (16, 18)
        )

        settings_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/feather/settings_icon.png")),
            dark_image = Image.open(resource_path("assets/icons/feather/settings_icon.png")),
            size = (18, 18)
        )

        red_dot_icon = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/icons/red_dot.png")),
            dark_image = Image.open(resource_path("assets/icons/red_dot.png")),
            size = (4, 4)
        )

        search_button = ctk.CTkButton(
            master = self,
            hover_color = ("#A4A4A4", "#40454D"),
            fg_color = ("#D9D9D9", "#282B30"),
            command = interfaces[0],
            image = explore_icon,
            corner_radius = 5,
            height = 32,
            width = 32,
            text = ""
        )

        self.search_button_tooltip = CTkToolTip(
            widget = search_button,
            message = language_manager.get_text("search_panel"),
            corner_radius = 5,
            delay = 0.5
        )

        search_button.pack(
            side = "top",
            pady = 10,
            padx = 10
        )

        queue_button = ctk.CTkButton(
            master = self,
            command = self.remove_red_dot_notification,
            hover_color = ("#A4A4A4", "#40454D"),
            fg_color = ("#D9D9D9", "#282B30"),
            image = download_icon,
            corner_radius = 5,
            height = 32,
            width = 32,
            text = ""
        )

        self.notification_red_dot = ctk.CTkLabel(
            master = queue_button,
            image = red_dot_icon,
            corner_radius = 100,
            height = 1,
            width = 1,
            text = ""
        )

        self.queue_button_tooltip = CTkToolTip(
            widget = queue_button,
            message = language_manager.get_text("download_queue"),
            corner_radius = 5,
            delay = 0.5
        )

        queue_button.pack(
            side = "top",
            padx = 10,
            pady = 6
        )

        settings_button = ctk.CTkButton(
            master = self,
            hover_color = ("#A4A4A4", "#40454D"),
            fg_color = ("#D9D9D9", "#282B30"),
            command = interfaces[2],
            image = settings_icon,
            corner_radius = 5,
            height = 32,
            width = 32,
            text = ""
        )

        self.settings_button_tooltip = CTkToolTip(
            widget = settings_button,
            message = language_manager.get_text("settings"),
            corner_radius = 5,
            delay = 0.5
        )

        settings_button.pack(
            side = "bottom",
            pady = 10,
            padx = 10
        )

        github_button = ctk.CTkButton(
            master = self,
            command = lambda: openurl("https://www.github.com/SwiftTube/"),
            hover_color = ("#A4A4A4", "#40454D"),
            fg_color = ("#D9D9D9", "#282B30"),
            image = github_icon,
            corner_radius = 5,
            height = 32,
            width = 32,
            text = ""
        )

        self.github_button_tooltip = CTkToolTip(
            widget = github_button,
            message = language_manager.get_text("repository"),
            corner_radius = 5,
            delay = 0.5
        )

        github_button.pack(
            side = "bottom",
            padx = 10,
            pady = 6
        )

    def remove_red_dot_notification(self):
        if self.notification_already_active:
            self.notification_red_dot.place_forget()
            self.notification_already_active = False

        self.interfaces[1]()

    def add_red_dot_notification(self):
        if not self.notification_already_active:
            self.notification_red_dot.place(rely = 0.15, relx = 0.7)
            self.notification_already_active = True

    def update_language(self):
        self.search_button_tooltip.configure(message = language_manager.get_text("search_panel"))
        self.queue_button_tooltip.configure(message = language_manager.get_text("download_queue"))
        self.settings_button_tooltip.configure(message = language_manager.get_text("settings"))
        self.github_button_tooltip.configure(message = language_manager.get_text("repository"))
