import customtkinter as ctk
from PIL import Image

from core.utils import resource_path

class UIResources:
    _icons: dict = {}

    @classmethod
    def get_icon(cls, light_path: str, dark_path: str | None, size: tuple[int, int]) -> ctk.CTkImage:
        dark_path = dark_path or light_path

        key = (light_path, dark_path, size)

        if key not in cls._icons:
            try:
                light_img = Image.open(resource_path(light_path))
                dark_img = Image.open(resource_path(dark_path))

                cls._icons[key] = ctk.CTkImage(
                    light_image = light_img,
                    dark_image = dark_img,
                    size = size
                )

            except FileNotFoundError as e:
                raise FileNotFoundError(f"Icon files not found: {light_path}, {dark_path}") from e

        return cls._icons[key]
