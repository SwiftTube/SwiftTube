import threading

import customtkinter as ctk

from core.resource_manager import UIResources
from .toast_notification import ClipboardCopiedWidget

x_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/x_icon.png",
    dark_path = "assets/icons/feather/x_icon.png",
    size = (10, 10)
)

mini_tags_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/tag_icon.png",
    dark_path = "assets/icons/feather/tag_icon.png",
    size = (12, 12)
)

tags_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/tag_icon.png",
    dark_path = "assets/icons/feather/tag_icon.png",
    size = (18, 18)
)

class FilterComponent(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            master = parent,
            border_color = "#5796F4",
            fg_color = ["#FAFAFA", "#282B30"],
            corner_radius = 5,
            border_width = 1,
            height = 32,
            width = 32
        )

        widgets_in_component: list = []
        widgets_in_component.append(self)


        def add_tags():
            error_notification = ClipboardCopiedWidget(
                parent = self.master.master.master.master.master,
                message = "This feature is not available now.",
                notification_type = "warning"
            )

            threading.Thread(target = error_notification.notify).start()

            self.configure(height = 32)
            self.configure(width = 65)

            tags_button.pack_forget()

            delete_tags_button.pack(
                side = "right",
                expand = True,
                padx = 2,
                pady = 2
            )

            round_frame.pack(
                side = "right",
                expand = True,
                pady = 2
            )

            mini_tags_image.pack(
                side = "right",
                expand = True,
                padx = 6,
                pady = 2
            )

            tags_count.place(
                relx = 0.43,
                rely = 0.19
            )

        tags_button = ctk.CTkButton(
            master = self,
            fg_color = ["#FAFAFA", "#282B30"],
            command = add_tags,
            corner_radius = 5,
            image = tags_icon,
            hover = False,
            height = 20,
            width = 20,
            text = ""
        )

        tags_button.pack(
            expand = True,
            fill = "both",
            pady = 4,
            padx = 4
        )

        widgets_in_component.append(tags_button)

        def delete_tags():
            delete_tags_button.pack_forget()
            mini_tags_image.pack_forget()
            round_frame.pack_forget()
            tags_count.place_forget()

            tags_button.pack(
                expand = True,
                fill = "both",
                pady = 4,
                padx = 4
            )

        delete_tags_button = ctk.CTkButton(
            master = self,
            command = delete_tags,
            fg_color = ["#D9D9D9", "#282B30"],
            image = x_icon,
            hover = False,
            height = 10,
            width = 10,
            text = ""
        )

        widgets_in_component.append(delete_tags_button)

        round_frame = ctk.CTkFrame(
            master = self,
            corner_radius = 100,
            fg_color = "#5796F4",
            height = 20,
            width = 20
        )

        widgets_in_component.append(round_frame)

        mini_tags_image = ctk.CTkLabel(
            master = self,
            image = mini_tags_icon,
            text = ""
        )

        widgets_in_component.append(mini_tags_image)

        tags_count = ctk.CTkLabel(
            master = self,
            text_color = "#FAFAFA",
            fg_color = "#5796F4",
            bg_color = "#5796F4",
            height = 14,
            text = "3",

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 12
            )
        )

        widgets_in_component.append(tags_count)

        def hovering_button():
            delete_tags_button.configure(fg_color = ["#BFDDFF", "#154285"])
            tags_button.configure(fg_color = ["#BFDDFF", "#154285"])
            self.configure(fg_color = ["#BFDDFF", "#154285"])

        def left_button():
            delete_tags_button.configure(fg_color = ["#FAFAFA", "#282B30"])
            tags_button.configure(fg_color = ["#FAFAFA", "#282B30"])
            self.configure(fg_color = ["#FAFAFA", "#282B30"])

        for widget in widgets_in_component:
            widget.bind(
                "<Enter>",
                lambda event: hovering_button()
            )

            widget.bind(
                "<Leave>",
                lambda event: left_button()
            )
