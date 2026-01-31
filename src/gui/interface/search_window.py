import threading

from tkinter import TclError
import customtkinter as ctk
from PIL import Image

from gui.widgets.background_message import BackgroundMessage
from gui.widgets.video_search import VideoSearchWidget
from gui.components.tags import FilterComponent

from core.youtube_manager import fetch_video_information, search_video_on_yt
from core.utils import format_visits, resource_path
from core.settings_manager import get_setting_value
from core.language_manager import language_manager
from core.resource_manager import UIResources

search_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/search_icon.png",
    dark_path = "assets/icons/feather/search_icon.png",
    size = (16, 16)
)

clear_icon = UIResources.get_icon(
    light_path = "assets/icons/feather/x_icon_white.png",
    dark_path = "assets/icons/feather/x_icon_white.png",
    size = (10, 10)
)

couldnt_find_result_image = ctk.CTkImage(
    light_image = Image.open(resource_path("assets/couldnt_find_result_background.png")),
    dark_image = Image.open(resource_path("assets/couldnt_find_result_background.png")),
    size = (265, 197)
)

start_searching_image = ctk.CTkImage(
    light_image = Image.open(resource_path("assets/start_searching_background.png")),
    dark_image = Image.open(resource_path("assets/start_searching_background.png")),
    size = (250, 227)
)

class SearchInterface(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            master = parent,
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        language_manager.subscribe(self.update_language)

        search_frame = ctk.CTkFrame(
            master = self,
            fg_color = ["#FAFAFA", "#1E2124"],
            corner_radius = 0,
            height = 42
        )

        search_frame.pack(
            side = "top",
            fill = "x"
        )

        self.search_bar = ctk.CTkEntry(
            master = search_frame,
            placeholder_text = language_manager.get_text("search_placeholder"),
            placeholder_text_color = ["#9BA4AF", "#9BA4AF"],
            fg_color = ["#D9D9D9", "#282B30"],
            corner_radius = 5,
            border_width = 0,
            height = 32,

            font = ctk.CTkFont(
                family = "Mada",
                weight = "normal",
                size = 11
            )
        )

        self.search_bar.pack(
            side = "left",
            expand = True,
            fill = "x",
            padx = 20
        )

        def clear_search_bar():
            self.search_bar.delete(0, ctk.END)
            separator_frame.focus()

        clear_entry = ctk.CTkButton(
            master = self.search_bar,
            fg_color = ["#D9D9D9", "#282B30"],
            command = clear_search_bar,
            image = clear_icon,
            hover = False,
            height = 10,
            width = 10,
            text = ""
        )

        clear_entry.place(
            anchor = "center",
            relx = 0.97,
            rely = 0.5
        )

        filter_button = FilterComponent(
            parent = search_frame
        )

        filter_button.pack(
            side = "left"
        )

        def search_function():
            search_query = self.search_bar.get()

            search_thread = threading.Thread(
                target = search_videos,
                args = (search_query,)
            )

            search_thread.start()

        search_button = ctk.CTkButton(
            master = search_frame,
            command = search_function,
            fg_color = "#5796F4",
            image = search_icon,
            corner_radius = 5,
            height = 32,
            width = 32,
            text = ""
        )

        search_button.pack(
            side = "left",
            pady = 10,
            padx = 20
        )

        separator_frame = ctk.CTkFrame(
            master = self,
            fg_color = ["#D9D9D9", "#282B30"],
            corner_radius = 0,
            height = 2
        )

        separator_frame.pack(
            side = "top",
            fill = "x",
            padx = 10
        )

        self.videos_in_videosframe: list = []

        videos_frame = ctk.CTkScrollableFrame(
            master = self,
            scrollbar_button_hover_color = ("#A4A4A4", "#4C5158"),
            scrollbar_button_color = ("#D9D9D9", "#282B30"),
            fg_color = ["#FAFAFA", "#1E2124"]
        )

        self.couldnt_find_result = False

        self.couldnt_find_result_frame = BackgroundMessage(
            master = self,
            title = language_manager.get_text("search_empty_title"),
            description = language_manager.get_text("search_empty_subtitle"),
            image = couldnt_find_result_image
        )
        
        self.start_searching_frame = BackgroundMessage(
            master = self,
            title = language_manager.get_text("explore_empty_title"),
            description = language_manager.get_text("explore_empty_subtitle"),
            image = start_searching_image
        )

        self.start_searching_frame.pack(
            expand = True,
            side = "top",
            padx = 10,
            pady = 4
        )

        def create_video_component(url):
            video_info = fetch_video_information(url)

            video_component = VideoSearchWidget(
                parent = videos_frame,
                views = format_visits(video_info["views"]),
                image_url = video_info["thumbnail_url"],
                video_title = video_info["title"],
                channel = video_info["author"],
                url = url
            )

            video_component.pack(
                fill = "x",
                padx = 1,
                pady = 4
            )

            self.videos_in_videosframe.append(video_component)

        def search_videos(query: str):
            self.start_searching_frame.pack_forget()

            videos_frame.pack(
                expand = True,
                fill = "both",
                side = "top",
                padx = 10,
                pady = 4
            )

            if self.couldnt_find_result:
                self.couldnt_find_result_frame.pack_forget()

                videos_frame.pack(
                    expand = True,
                    fill = "both",
                    side = "top",
                    padx = 10,
                    pady = 4
                )

                self.couldnt_find_result = False

            for frame in self.videos_in_videosframe[:]:
                try:
                    frame.destroy()
                    self.videos_in_videosframe.remove(frame)

                except TclError as fast_draw_error:
                    # print(fast_draw_error)
                    pass

            self.videos_in_videosframe = []

            if not query.startswith("https://"):
                try:
                    search_results = search_video_on_yt(
                        user_query = query,
                        limit = get_setting_value("search_settings", "search_limit")
                    )

                    for _, video_url in enumerate(search_results):
                        video_thread = threading.Thread(
                            target = create_video_component,
                            args = (video_url,)
                        )

                        video_thread.start()

                except (IndexError, TypeError) as exception:
                    print(exception)
                    videos_frame.pack_forget()

                    if not self.couldnt_find_result:
                        self.couldnt_find_result_frame.pack(
                            expand = True,
                            side = "top",
                            padx = 10,
                            pady = 4
                        )

                        self.couldnt_find_result = True

                except TclError as fast_draw_error:
                    # print(fast_draw_error)
                    pass

                finally:
                    search_results = None

            else:
                create_video_component(query)

    def update_language(self):
        self.search_bar.configure(placeholder_text = language_manager.get_text("search_placeholder"))

        self.couldnt_find_result_frame.background_message_title.configure(
            text = language_manager.get_text("search_empty_title")
        )

        self.couldnt_find_result_frame.background_message_description.configure(
            text = language_manager.get_text("search_empty_subtitle")
        )
        
        self.start_searching_frame.background_message_title.configure(
            text = language_manager.get_text("explore_empty_title")
        )

        self.start_searching_frame.background_message_description.configure(
            text = language_manager.get_text("explore_empty_subtitle")
        )

        for video_widget in self.videos_in_videosframe:
            video_widget.update_language()