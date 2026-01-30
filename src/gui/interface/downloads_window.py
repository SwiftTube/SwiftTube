import customtkinter as ctk
from PIL import Image

from gui.widgets.background_message import BackgroundMessage

from core.language_manager import language_manager
from core.utils import resource_path

class DownloadsInterface(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            master = parent,
            fg_color = ["#FAFAFA", "#1E2124"],
        )

        language_manager.subscribe(self.update_language)

        start_download_image = ctk.CTkImage(
            light_image = Image.open(resource_path("assets/start_downloading_background.png")),
            dark_image = Image.open(resource_path("assets/start_downloading_background.png")),
            size = (219, 190)
        )

        self.queue_frame = ctk.CTkScrollableFrame(
            master = self,
            scrollbar_button_hover_color = ["#A4A4A4", "#4C5158"],
            scrollbar_button_color = ["#D9D9D9" ,"#282B30"],
            fg_color = ["#FAFAFA", "#1E2124"],
        )

        self.start_downloading_frame = BackgroundMessage(
            master = self,
            title = language_manager.get_text("explore_empty_title"),
            description = language_manager.get_text("explore_empty_subtitle"),
            image = start_download_image
        )

        self.start_downloading_frame.pack(
            expand = True,
            side = "top",
            padx = 10,
            pady = 4
        )

    def update_window(self, queue):
        if queue == 0:
            self.start_downloading_frame.pack(
                expand = True,
                side = "top",
                padx = 10,
                pady = 4
            )

            self.queue_frame.pack_forget()

        else:
            self.queue_frame.pack(
                expand = True,
                fill = "both",
                side = "top",
                padx = 10,
                pady = 4
            )

            self.start_downloading_frame.pack_forget()

    def update_language(self):
        self.start_downloading_frame.background_message_title.configure(
            text = language_manager.get_text("explore_empty_title")
        )

        self.start_downloading_frame.background_message_description.configure(
            text = language_manager.get_text("explore_empty_subtitle")
        )

        for child in self.queue_frame.winfo_children():
            if hasattr(child, "update_language"):
                child.update_language()