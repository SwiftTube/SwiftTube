from customtkinter import filedialog
import customtkinter as ctk

from core.settings_manager import set_setting_value
from core.resource_manager import UIResources

folder_path_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/folder_icon_light.png",
    dark_path = "assets/icons/feather/folder_icon_dark.png",
    size = (18, 16)
)

class SettingSwitchOptionWidget(ctk.CTkFrame):

    def __init__(self, parent, icon, name, description, button_command):
        super().__init__(
            master = parent,
            border_color = ["#D9D9D9", "#282B30"],
            fg_color = ["#FAFAFA", "#1E2124"],
            corner_radius = 5,
            border_width = 1,
            height = 62
        )

        option_icon = ctk.CTkLabel(
            master = self,
            image = icon,
            text = ""
        )

        option_icon.pack(side = "left", padx = 24, pady = 14)

        text_holder = ctk.CTkFrame(
            master = self,
            fg_color = ["#FAFAFA", "#1E2124"],
            height = 50
        )

        text_holder.pack(side = "left")

        self.option_name = ctk.CTkLabel(
            master = text_holder,
            text_color = ["#2A2D36", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            anchor = "w",
            text = name,
            height = 13,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            )
        )

        self.option_name.pack(side = "top", fill = "x")

        self.option_description = ctk.CTkLabel(
            master = text_holder,
            text_color = "#9BA4AF",
            fg_color = ["#FAFAFA", "#1E2124"],
            text = description,
            anchor = "w",
            height = 13,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            )
        )

        self.option_description.pack(side = "top", fill = "x")

        self.option_switch = ctk.CTkSwitch(
            master = self,
            border_color = ["#D9D9D9", "#478EFA"],
            button_color = ["#A4A4A4", "#FAFAFA"],
            fg_color = ["#D9D9D9", "#282B30"],
            progress_color = "#478EFA",
            command = button_command,
            border_width = 0,
            height = 10,
            width = 20,
            text = ""
        )

        self.option_switch.pack(side = "right", padx = 14)

    def get_switch_state(self) -> (int | str):
        switch_state = self.option_switch.get()
        return switch_state

    def toggle_switch(self, state: int) -> None:
        if state == 0:
            self.option_switch.deselect()

        else:
            self.option_switch.select()
    
    def configure(self, title: str, description: str) -> None:
        self.option_name.configure(text = title)
        self.option_description.configure(text = description)

class SettingSelectionOptionWidget(ctk.CTkFrame):

    def __init__(self, parent, icon, name, description, button_command, options, default_value = None):
        super().__init__(
            master = parent,
            border_color = ["#D9D9D9", "#282B30"],
            fg_color = ["#FAFAFA", "#1E2124"],
            corner_radius = 5,
            border_width = 1,
            height = 62
        )

        option_icon = ctk.CTkLabel(
            master = self,
            image = icon,
            text = ""
        )

        option_icon.pack(side = "left", padx = 24, pady = 14)

        text_holder = ctk.CTkFrame(
            master = self,
            fg_color = ["#FAFAFA", "#1E2124"],
            height = 50
        )

        text_holder.pack(side = "left")

        self.option_name = ctk.CTkLabel(
            master = text_holder,
            text_color = ["#2A2D36", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            anchor = "w",
            text = name,
            height = 13,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            )
        )

        self.option_name.pack(side = "top", fill = "x")

        self.option_description = ctk.CTkLabel(
            master = text_holder,
            text_color = "#9BA4AF",
            fg_color = ["#FAFAFA", "#1E2124"],
            text = description,
            anchor = "w",
            height = 13,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            )
        )

        self.option_description.pack(side = "top", fill = "x")

        def optionmenu_callback(_):
            button_command()

        optionmenu_var = ctk.StringVar(value = default_value)

        border_color_for_option_menu = ctk.CTkFrame(
            master = self,
            fg_color = ["#D9D9D9", "#282B30"],
            border_color = ["#D9D9D9", "#282B30"],
            corner_radius = 5,
            border_width = 1
        )

        border_color_for_option_menu.pack(side = "right", padx = 14)

        self.option_menu = ctk.CTkOptionMenu(
            master = border_color_for_option_menu,
            dropdown_hover_color = ["#D9D9D9", "#282B30"],
            dropdown_fg_color = ["#FAFAFA", "#1E2124"],
            button_color = ["#FAFAFA", "#1E2124"],
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            command = optionmenu_callback,
            variable = optionmenu_var,

            dynamic_resizing = True,
            corner_radius = 5,
            values = options,
            hover = False,

            dropdown_font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            ),
            
            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            )
        )

        self.option_menu.pack(pady = 2, padx = 2)

    def get_option_value(self):
        return self.option_menu.get()

    def change_option_value(self, value) -> None:
        self.option_menu.set(value)

    def configure(self, title: str, description: str) -> None:
        self.option_name.configure(text = title)
        self.option_description.configure(text = description)

class SettingPathSelectionWidget(ctk.CTkFrame):

    def __init__(self, parent, icon, name, description, default_path):
        super().__init__(
            master = parent,
            border_color = ["#D9D9D9", "#282B30"],
            fg_color = ["#FAFAFA", "#1E2124"],
            corner_radius = 5,
            border_width = 1,
            height = 62
        )


        option_icon = ctk.CTkLabel(
            master = self,
            image = icon,
            text = ""
        )

        option_icon.pack(side = "left", padx = 24, pady = 14)

        text_holder = ctk.CTkFrame(
            master = self,
            fg_color = ["#FAFAFA", "#1E2124"],
            height = 50
        )

        text_holder.pack(side = "left")

        self.option_name = ctk.CTkLabel(
            master = text_holder,
            text_color = ["#2A2D36", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
            anchor = "w",
            text = name,
            height = 13,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            )
        )

        self.option_name.pack(side = "top", fill = "x")

        self.option_description = ctk.CTkLabel(
            master = text_holder,
            text_color = "#9BA4AF",
            fg_color = ["#FAFAFA", "#1E2124"],
            text = description,
            anchor = "w",
            height = 13,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 13
            )
        )

        self.option_description.pack(side = "top", fill = "x")

        def get_folder_path():
            path = filedialog.askdirectory()

            if not path or path == "":
                return

            path_var.set(path)

            set_setting_value("download_settings", "download_path", value = path)

        select_path_button = ctk.CTkButton(
            master = self,
            image = folder_path_icon,
            fg_color = ["#D9D9D9", "#282B30"],
            text_color = "#FAFAFA",
            command = get_folder_path,
            hover = False,
            text = "",
            height = 30,
            width = 30
        )

        select_path_button.pack(side = "right", padx = 14)

        path_var = ctk.StringVar(value = default_path)

        path_display = ctk.CTkEntry(
            master = self,
            corner_radius = 5,
            fg_color = ["#D9D9D9", "#282B30"],
            border_color = ["#D9D9D9", "#282B30"],
            state = "disabled",
            text_color = ["#A4A4A4", "#9BA4AF"],
            textvariable = path_var,
            width = 200
        )

        path_display.pack(side = "right")

    def configure(self, title: str, description: str) -> None:
        self.option_name.configure(text = title)
        self.option_description.configure(text = description)
