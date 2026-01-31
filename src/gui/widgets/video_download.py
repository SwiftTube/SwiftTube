from tkinter import TclError
import threading
import tempfile
import shutil
import time
import os

from PIL import Image, ImageOps, UnidentifiedImageError
from pytubefix import YouTube, request, exceptions
import customtkinter as ctk
import requests

from gui.components.toast_notification import ClipboardCopiedWidget

from core.utils import format_bytes, sanitize_filename, resource_path
from core.image_manager import create_image_with_rounded_corners
from core.settings_manager import get_setting_value
from core.language_manager import language_manager
from core.resource_manager import UIResources

filesize_icon_blue = UIResources.get_icon(
    light_path = "assets/icons/material/filesize_icon_blue.png",
    dark_path = "assets/icons/material/filesize_icon_blue.png",
    size = (10, 9)
)

filesize_icon_orange = UIResources.get_icon(
    light_path = "assets/icons/material/filesize_icon_orange.png",
    dark_path = "assets/icons/material/filesize_icon_orange.png",
    size = (10, 9)
)

download_speed_icon_blue = UIResources.get_icon(
    light_path = "assets/icons/material/download_speed_icon_blue.png",
    dark_path = "assets/icons/material/download_speed_icon_blue.png",
    size = (10, 9)
)

download_speed_icon_orange = UIResources.get_icon(
    light_path = "assets/icons/material/download_speed_icon_orange.png",
    dark_path = "assets/icons/material/download_speed_icon_orange.png",
    size = (10, 9)
)

download_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/download_icon.png",
    dark_path = "assets/icons/feather/download_icon.png",
    size = (10, 11)
)

pause_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/pause_icon.png",
    dark_path = "assets/icons/feather/pause_icon.png",
    size = (7, 8)
)

resume_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/resume_icon.png",
    dark_path = "assets/icons/feather/resume_icon.png",
    size = (7, 9)
)

views_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/views_icon.png",
    dark_path = "assets/icons/feather/views_icon.png",
    size = (10, 10)
)

thumbnail = resource_path("assets/cant_load_thumbnail.png")

class VideoDownloadWidget(ctk.CTkFrame):

    def __init__(self, parent, image_url, video_title, channel, views, url, filesizes):
        super().__init__(
            master = parent,
            border_color = ["#D9D9D9", "#282B30"],
            fg_color = ["#FAFAFA", "#1E2124"],
            corner_radius = 5,
            border_width = 1,
            height = 90
        )

        self.filesizes = filesizes
        self.stop_download = False

        response = requests.get(image_url, timeout = 10)

        if response.status_code == 200:
            try:
                with tempfile.NamedTemporaryFile(delete = False, suffix = '.png') as temp_file:
                    temp_file.write(response.content)
                    image = Image.open(temp_file.name)

                    gray_image = ImageOps.grayscale(image)
                    bbox = gray_image.getbbox()

                    if bbox:
                        image = image.crop(bbox)

            except (FileNotFoundError, UnidentifiedImageError):
                pass
                
            thumbnail = create_image_with_rounded_corners(image, 30)

        available_qualities = [q for q in self.filesizes.keys() if q != "audio"]

        def quality_sort_key(q):
            return int(q.replace("p", ""))

        default_quality = get_setting_value(
            "download_settings",
            "default_download_quality"
        )

        if default_quality not in available_qualities:
            default_quality = max(available_qualities, key=quality_sort_key)

        self.current_quality = ctk.StringVar(value=default_quality)

        video_image = ctk.CTkImage(
            light_image = thumbnail,
            dark_image = thumbnail,
            size = (129, 71)
        )


        video_thumbnail = ctk.CTkLabel(
            master = self,
            image = video_image,
            corner_radius = 5,
            text = ""
        )

        video_thumbnail.pack(
            side = "left",
            padx = 10,
            pady = 10
        )

        video_information_frame = ctk.CTkFrame(
            master = self,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        video_information_frame.pack(
            fill = "both",
            expand = True,
            side = "top",
            pady = 10,
            padx = 2
        )

        video_title_label = ctk.CTkLabel(
            master = video_information_frame,
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#FAFAFA", "#1E2124"],
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
            text = f"{channel}  •  {views}  ",
            text_color = "#9BA4AF",
            fg_color = ["#FAFAFA", "#1E2124"],
            image = views_icon,
            compound = "right",
            anchor = "w",
            height = 11,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 11,
            )
        )

        video_information.pack(
            side = "top",
            fill = "x"
        )

        self.filesize_label = ctk.CTkLabel(
            master = video_information_frame,
            text = f"  {language_manager.get_text('file_size')}: {format_bytes(self.filesizes[self.current_quality.get()])}", # cambiar esto
            image = filesize_icon_blue,
            text_color = "#5796F4",
            fg_color = ["#D9D9D9", "#282B30"],
            corner_radius = 5,
            compound = "left",
            height = 20,
            width = 94,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 11
            )
        )

        self.filesize_label.pack(
            side = "left",
            pady = 4
        )

        self.download_speed_label = ctk.CTkLabel(
            master = video_information_frame,
            image = download_speed_icon_blue,
            text_color = "#5796F4",
            fg_color = ["#D9D9D9", "#282B30"],
            text = "  00 MB/s",
            corner_radius = 5,
            compound = "left",
            height = 20,
            width = 20,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "bold",
                size = 11
            )
        )

        media_quality_var = ctk.StringVar(
            value = get_setting_value(
                "download_settings",
                "default_download_quality"
            )
        )

        option_values = [
            f"{q} - {format_bytes(self.filesizes[q])}"
            for q in available_qualities
        ]

        if "audio" in self.filesizes:
            option_values.append(
                f"MP3 - {format_bytes(self.filesizes['audio'])}"
            )

        media_quality = ctk.CTkOptionMenu(
            master = video_information_frame,
            dropdown_hover_color = ["#D9D9D9", "#282B30"],
            dropdown_fg_color = ["#FAFAFA", "#1E2124"],
            button_color = ["#D9D9D9", "#282B30"],
            text_color = ["#1E2124", "#FAFAFA"],
            fg_color = ["#D9D9D9", "#282B30"],
            command = None,
            variable = media_quality_var,
            values = option_values,
            corner_radius = 5,
            hover = False,
            height = 20,
            width = 115,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 12
            )
        )

        progress_bar = ctk.CTkProgressBar(
            master = video_information_frame,
            fg_color = ["#D9D9D9", "#282B30"],
            progress_color = "#5796F4",
            corner_radius = 7,
            height = 20,
            width = 150
        )

        progress_bar.set(0)

        def start_download():
            progress_bar.pack(side = "right", pady = 4)
            media_quality.pack_forget()

            action_button.configure(command = pause_download)
            action_button.configure(image = pause_icon)

            self.download_speed_label.pack(
                side = "left",
                pady = 4,
                padx = 6
            )

            try:
                from gui.window import UPDATE_FUNC, QUEUE_FRAME

                youtube_object = YouTube(url)

                if media_quality_var.get().startswith("MP3"):
                    stream = youtube_object.streams.get_audio_only()
                    file_size = self.filesizes["audio"]
                    file_extension = "mp3"
                
                else:
                    selected_quality = media_quality_var.get().split(" - ")[0]
                    stream = youtube_object.streams.get_by_resolution(selected_quality)
                    file_size = self.filesizes[selected_quality]
                    file_extension = stream.mime_type.split("/")[-1]

                sanitized_title = sanitize_filename(video_title)
                file_name = f"{sanitized_title}.{file_extension}"

                with open(file_name, "wb") as video_file:
                    stream = request.stream(stream.url)
                    downloaded_bytes = 0
                    start_time = time.time()

                    while True:

                        if self.stop_download:
                            time.sleep(2)
                            continue

                        file_chunk = next(stream, None)

                        if file_chunk:
                            video_file.write(file_chunk)
                            downloaded_bytes += len(file_chunk)

                            elapsed_time = time.time() - start_time

                            if elapsed_time > 0.1:
                                download_speed = format_bytes(int(downloaded_bytes / elapsed_time))
                                self.download_speed_label.configure(text = f"  {download_speed}/s")

                            progress_percent = downloaded_bytes / file_size
                            progress_bar.set(progress_percent)

                            self.master.update_idletasks()

                        else:
                            # There is no more chunks, download completed.
                            break

                shutil.move(
                    src = file_name,
                    dst = os.path.join(
                        get_setting_value("download_settings", "download_path"),
                        file_name
                    )
                )

                action_button.configure(state = "disabled")
                progress_bar.set(100)
                self.destroy()

                UPDATE_FUNC(len(QUEUE_FRAME.winfo_children()))

                success_notification = ClipboardCopiedWidget(
                    parent = self.master.master.master.master.master.master,
                    message = language_manager.get_text("success_download"),
                    notification_type = "success"
                )

                threading.Thread(target = success_notification.notify).start()

                action_button.configure(state = "disabled")
                action_button.configure(fg_color = "#F45759")
                progress_bar.configure(progress_color = "#F45759")

            except (exceptions.LiveStreamError, exceptions.VideoUnavailable) as streaming_error:
                error_notification = ClipboardCopiedWidget(
                    parent = self.master.master.master.master.master.master,
                    message = language_manager.get_text("error_cant_download"),
                    notification_type = "error"
                )

                threading.Thread(target = error_notification.notify).start()

                action_button.configure(state = "disabled")
                action_button.configure(fg_color = "#F45759")
                progress_bar.configure(progress_color = "#F45759")

            except TclError as _:
                pass

        def pause_download():
            self.stop_download = True

            action_button.configure(image = resume_icon)
            action_button.configure(command = resume_download)
            action_button.configure(fg_color = "#F4A257")

            self.filesize_label.configure(image = filesize_icon_orange)
            self.filesize_label.configure(text_color = "#F4A257")

            self.download_speed_label.configure(image = download_speed_icon_orange)
            self.download_speed_label.configure(text_color = "#F4A257")
            progress_bar.configure(progress_color = "#F4A257")

        def resume_download():
            self.stop_download = False

            action_button.configure(image = pause_icon)
            action_button.configure(command = pause_download)
            action_button.configure(fg_color = "#5796F4")

            self.filesize_label.configure(image = filesize_icon_blue)
            self.filesize_label.configure(text_color = "#5796F4")

            self.download_speed_label.configure(image = download_speed_icon_blue)
            self.download_speed_label.configure(text_color = "#5796F4")

            progress_bar.configure(progress_color = "#5796F4")

        action_button = ctk.CTkButton(
            master = video_information_frame,
            image = download_icon,
            fg_color = "#5796F4",
            corner_radius = 5,
            hover = False,
            height = 20,
            width = 20,
            text = "",

            command = lambda: threading.Thread(
                target = start_download,
                daemon = True
            ).start()
        )

        action_button.pack(
            side = "right",
            padx = 10,
            pady = 4
        )

        media_quality.pack(
            side = "right",
            pady = 4
        )

    def configure(self, **kwargs):
        super().configure(**kwargs)

    def update_language(self):
        self.filesize_label.configure(
            text = f"  {language_manager.get_text('file_size')}: {format_bytes(self.filesizes[self.current_quality.get()])}"
        )