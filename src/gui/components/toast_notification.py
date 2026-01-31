import customtkinter as ctk
from typing import Literal

from core.resource_manager import UIResources

types = Literal["error", "information", "warning", "success"]

information_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/information_icon.png",
    dark_path = "assets/icons/feather/information_icon.png",
    size = (15, 15)
)

error_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/error_icon.png",
    dark_path = "assets/icons/feather/error_icon.png",
    size = (15, 15)
)

warning_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/warning_icon.png",
    dark_path = "assets/icons/feather/warning_icon.png",
    size = (15, 15)
)

check_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/check_icon.png",
    dark_path = "assets/icons/feather/check_icon.png",
    size = (12, 10)
)

class ClipboardCopiedWidget(ctk.CTkFrame):

    def __init__(self, parent, message, notification_type: types):
        super().__init__(
            master = parent,
            corner_radius = 5,
            border_width = 1,
            height = 100,
            width = 400
        )


        if notification_type == "error":
            notification_color = "#F45759"
            notification_icon = error_icon

        elif notification_type == "information":
            notification_color = "#5796F4"
            notification_icon = information_icon

        elif notification_type == "warning":
            notification_color = "#F4A257"
            notification_icon = warning_icon

        elif notification_type == "success":
            notification_color = "#37AE59"
            notification_icon = check_icon

        else:
            notification_color = None
            notification_icon = None

        self.copied_label = ctk.CTkLabel(
            master = self,
            fg_color = notification_color,
            image = notification_icon,
            text_color = "#FAFAFA",
            text = "  " + message,
            corner_radius = 5,
            compound = "left",
            width = 100,
            height = 25,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 11
            )
        )

        self.copied_label.pack(expand = True, fill = "both")

        self.already_active = False

    def notify(self):
        if not self.already_active:
            self.master.after(0, self._show_and_hide)

    def _show_and_hide(self):
        if not self.winfo_ismapped():
            self.pack(side = "bottom", pady = 10)

        self.already_active = True
        self.after(2000, self._hide)

    def _hide(self):
        if self.winfo_ismapped():
            self.pack_forget()

        self.already_active = False

    def configure(self, **kwargs):
        super().configure(**kwargs)
