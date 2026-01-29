import customtkinter as ctk

class BackgroundMessage(ctk.CTkFrame):
        
    def __init__(self, master, title: str, description: str, image: ctk.CTkImage):
        super().__init__(
            master,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        background_message_image = ctk.CTkLabel(
            master = self,
            image = image,
            text = ""
        )

        background_message_image.pack(side = "left", padx = 40)

        self.background_message_text_frame = ctk.CTkFrame(
            master = self,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.background_message_text_frame.pack(side = "left")

        self.background_message_title = ctk.CTkLabel(
            master = self.background_message_text_frame,
            text = title,
            text_color = "#5796F4",
            justify = "left",

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 23
            )
        )

        self.background_message_title.pack(side = "top")

        self.background_message_description = ctk.CTkLabel(
            master = self.background_message_text_frame,
            text_color = "#9BA4AF",
            text = description,
            justify = "left",

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 15
            )
        )

        self.background_message_description.pack(side = "top")

    def configure(self, **kwargs):
        super().configure(**kwargs)