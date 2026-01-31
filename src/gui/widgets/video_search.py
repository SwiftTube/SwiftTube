from webbrowser import open as openurl
import threading
import tempfile

from pyperclip import copy as copy_link
from PIL import Image, ImageOps, UnidentifiedImageError
import customtkinter as ctk

import requests

from gui.components.toast_notification import ClipboardCopiedWidget
from gui.widgets.video_download import VideoDownloadWidget

from core.image_manager import create_image_with_rounded_corners
from core.youtube_manager import fetch_video_information
from core.settings_manager import get_setting_value
from core.language_manager import language_manager
from core.resource_manager import UIResources
from core.utils import resource_path

link_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/link_icon.png",
    dark_path = "assets/icons/feather/link_icon.png",
    size = (12, 6)
)

copy_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/copy_icon.png",
    dark_path = "assets/icons/feather/copy_icon.png",
    size = (10, 10)
)

plus_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/plus_icon.png",
    dark_path = "assets/icons/feather/plus_icon.png",
    size = (8, 8)
)

views_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/views_icon.png",
    dark_path = "assets/icons/feather/views_icon.png",
    size = (10, 10)
)

thumbnail = resource_path("assets/cant_load_thumbnail.png")

class VideoSearchWidget(ctk.CTkFrame):

    def __init__(self, parent, image_url, video_title, channel, views, url):
        super().__init__(
            master = parent,
            border_color = ("#D9D9D9", "#282B30"),
            fg_color = ["#FAFAFA", "#1E2124"],
            corner_radius = 5,
            border_width = 1,
            height = 90
        )

        response = requests.get(image_url, timeout = 10)

        if get_setting_value(
            category = "search_settings",
            setting = "load_video_thumbnail"):

            if response.status_code == 200:
                try:
                    with tempfile.NamedTemporaryFile(delete = False, suffix = '.png') as temp_file:
                        temp_file.write(response.content)
                        image = Image.open(temp_file.name)

                        gray_image = ImageOps.grayscale(image)
                        bbox = gray_image.getbbox()

                        if bbox:
                            image = image.crop(bbox)
                
                    thumbnail = create_image_with_rounded_corners(image, 30)

                except UnidentifiedImageError:
                    # print("Could not identify image format. Using default thumbnail.")
                    pass

        if get_setting_value(
            category = "search_settings",
            setting = "load_video_thumbnail"):

            video_image = ctk.CTkImage(
                light_image = thumbnail,
                dark_image = thumbnail,
                size = (129, 71)
            )


        if get_setting_value(
            category = "search_settings",
            setting = "load_video_thumbnail"):

            video_thumbnail = ctk.CTkLabel(
                master = self,
                image = video_image,
                corner_radius = 5,
                text = ""
            )

        video_information_padding = 2
        add_to_downloads_padding = 10

        if get_setting_value(
            category = "search_settings",
            setting = "load_video_thumbnail"):

            video_thumbnail.pack(
                side = "left",
                padx = 10,
                pady = 10
            )

        else:
            video_information_padding = 10
            add_to_downloads_padding = 2

        video_information_frame = ctk.CTkFrame(
            master = self,
            fg_color =  ["#FAFAFA", "#1E2124"]
        )

        video_information_frame.pack(
            fill = "both",
            expand = True,
            side = "top",
            pady = 10,
            padx = video_information_padding
        )

        video_title_label = ctk.CTkLabel(
            master = video_information_frame,
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color =  ["#FAFAFA", "#1E2124"],
            text = video_title,
            compound = "left",
            anchor = "w",
            height = 16,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 15,
            )
        )

        video_title_label.pack(
            side = "top",
            fill = "x"
        )

        video_information = ctk.CTkLabel(
            master = video_information_frame,
            fg_color =  ["#FAFAFA", "#1E2124"],
            text = f"{channel}  •  {views}  ",
            text_color = "#9BA4AF",
            image = views_icon,
            compound = "right",
            anchor = "w",
            height = 11,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 11
            )
        )

        video_information.pack(
            side = "top",
            fill = "x"
        )

        self.watch_video_button = ctk.CTkButton(
            master = video_information_frame,
            hover_color = ["#A4A4A4", "#40454D"],
            fg_color = ["#D9D9D9", "#282B30"],
            command = lambda: openurl(url),
            text_color = "#5796F4",
            text = language_manager.get_text("watch_video"),
            corner_radius = 5,
            image = link_icon,
            compound = "left",
            height = 20,
            width = 94,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 10
            )
        )

        self.watch_video_button.pack(
            side = "left",
            pady = 4
        )

        self.snackbar = ClipboardCopiedWidget(
            parent = self.master.master.master.master.master.master, #
            message = language_manager.get_text("copied_link"),
            notification_type = "information"
        )

        def copy_link_and_notify():
            copy_link(url)
            threading.Thread(target = self.snackbar.notify).start()

        copy_video_button = ctk.CTkButton(
            master = video_information_frame,
            hover_color = ["#A4A4A4", "#40454D"],
            fg_color = ["#D9D9D9", "#282B30"],
            command = copy_link_and_notify,
            corner_radius = 5,
            image = copy_icon,
            height = 20,
            width = 20,
            text = ""
        )

        copy_video_button.pack(
            side = "left",
            pady = 4,
            padx = 6
        )

        self.queue_snackbar = ClipboardCopiedWidget(
            parent = self.master.master.master.master.master.master,
            message = language_manager.get_text("added_to_queue"),
            notification_type = "information"
        )

        def add_video_and_notify():
            from gui.window import UPDATE_FUNC
            from gui.window import QUEUE_FRAME
            from gui.window import SIDE_BAR

            UPDATE_FUNC(len(QUEUE_FRAME.winfo_children()) + 1)

            threading.Thread(target = self.queue_snackbar.notify).start()
            SIDE_BAR.add_red_dot_notification()

            video_information_fetch = fetch_video_information(url)

            filesizes: dict = video_information_fetch["filesize"]
            filesizes["audio"] = video_information_fetch["audio"]

            video_component = VideoDownloadWidget(
                parent = QUEUE_FRAME,
                image_url = image_url,
                video_title = video_title,
                channel = channel,
                filesizes = filesizes,
                views = views,
                url = url
            )

            video_component.pack(
                fill = "x",
                padx = 1,
                pady = 4
            )

        self.add_to_downloads_button = ctk.CTkButton(
            master = video_information_frame,
            command = add_video_and_notify,
            text = language_manager.get_text("add_to_downloads"),
            hover_color = ["#A4A4A4", "#40454D"],
            fg_color = ["#D9D9D9", "#282B30"],
            text_color = "#5796F4",
            compound = "right",
            corner_radius = 5,
            image = plus_icon,
            height = 20,
            width = 115,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 10
            )
        )

        self.add_to_downloads_button.pack(
            side = "right",
            padx = add_to_downloads_padding,
            pady = 4
        )

    def update_language(self):
        self.watch_video_button.configure(
            text = language_manager.get_text("watch_video")
        )

        self.add_to_downloads_button.configure(
            text = language_manager.get_text("add_to_downloads")
        )
