import customtkinter as ctk

from core.language_manager import language_manager
from core.resource_manager import UIResources

update_icon = UIResources.get_icon(
    light_path = "assets/icons/material/update_icon.png",
    dark_path = "assets/icons/material/update_icon.png",
    size = (30, 30)
)

class UpdateMessageWidget(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            master = parent,
            fg_color = "#478EFA",
            corner_radius = 5,
            height = 100
        )

        language_manager.subscribe(self.update_language)
        self.build_widget()

    def build_widget(self):
        text_frame = ctk.CTkFrame(
            master = self,
            fg_color = "#478EFA",
        )

        text_frame.pack(side = "left", padx = 20, pady = 10)

        self.new_update_title = ctk.CTkLabel(
            master = text_frame,
            text_color = "#FAFAFA",
            fg_color = "#478EFA",
            anchor = "w",
            text = language_manager.get_text("update_available_title"),

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 15
            )
        )

        self.new_update_title.pack(side = "top", fill = "x")

        self.new_update_description = ctk.CTkLabel(
            master = text_frame,
            text_color = "#FAFAFA",
            fg_color = "#478EFA",
            anchor = "w",
            text = language_manager.get_text("update_available_subtitle"),

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            )
        )

        self.new_update_description.pack(side = "top", fill = "x")

        update_icon_label = ctk.CTkLabel(
            master = self,
            image = update_icon,
            text = ""
        )

        update_icon_label.pack(side = "right", padx = 24, pady = 14)

    def update_language(self):
        self.new_update_title.configure(
            text = language_manager.get_text("update_available_title")
        )

        self.new_update_description.configure(
            text = language_manager.get_text("update_available_subtitle")
        )