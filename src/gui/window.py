import customtkinter as ctk

from gui.interface.downloads_window import DownloadsInterface
from gui.interface.settings_window import SettingsInterface
from gui.interface.search_window import SearchInterface
from gui.widgets.side_bar import SideBarWidget

from core.settings_manager import get_setting_value
from core.metadata import __version__
from core.utils import resource_path

class MainWindow(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            master = parent,
            border_color = "#282B30",
            fg_color = ["#FAFAFA", "#1E2124"],
            border_width = 0.5,
            corner_radius = 0
        )

        self.place(
            relheight = 1,
            relwidth = 1,
            x = 0,
            y = 0
        )

        self.downloads_interface = DownloadsInterface(parent = self)
        self.settings_interface = SettingsInterface(parent = self)
        self.search_interface = SearchInterface(parent = self)

        self.search_interface.pack(
            side = "left",
            fill = "both",
            expand = True
        )

        global QUEUE_FRAME
        global UPDATE_FUNC
        
        QUEUE_FRAME = self.downloads_interface.queue_frame
        UPDATE_FUNC = self.downloads_interface.update_window

        self.current_frame = self.search_interface

        def change_interface(new_frame: ctk.CTkFrame):
            self.current_frame.pack_forget()
            self.current_frame = new_frame
            self.current_frame.pack(
                side = "left",
                fill = "both",
                expand = True
            )

        global SIDE_BAR
        SIDE_BAR = SideBarWidget(
            parent = self,
            interfaces = [
                lambda: change_interface(self.search_interface),
                lambda: change_interface(self.downloads_interface),
                lambda: change_interface(self.settings_interface)
            ]
        )

        SIDE_BAR.pack(
            side = "right",
            fill = "y"
        )

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(f"SwiftTube a{__version__}")
        self.iconbitmap(resource_path("assets/app.ico"))
        self.geometry("800x455")
        self.minsize(800, 455)

        self.wm_attributes("-transparentcolor", "grey")

        if get_setting_value(category = "appearance_settings", setting = "dark_theme"):
            ctk.set_appearance_mode("dark")

        else:
            ctk.set_appearance_mode("light")

        self.main_window = MainWindow(self)
        self.mainloop()
