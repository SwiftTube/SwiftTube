from PIL import Image, ImageDraw
from typing import Tuple

def create_image_with_rounded_corners(image: Image, radius: int) -> Image.Image:
    rounded_corner_added_image = image

    circle_mask = Image.new('L', (radius * 2, radius * 2), 0)
    draw_circle = ImageDraw.Draw(circle_mask)

    draw_circle.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=255)
    alpha_mask = Image.new('L', rounded_corner_added_image.size, 255)

    w, h = rounded_corner_added_image.size

    alpha_mask.paste(circle_mask.crop(
        (0, 0, radius, radius)), (0, 0)
    )

    alpha_mask.paste(circle_mask.crop(
        (0, radius, radius, radius * 2)), (0, h - radius)
    )

    alpha_mask.paste(circle_mask.crop(
        (radius, 0, radius * 2, radius)), (w - radius, 0)
    )

    alpha_mask.paste(circle_mask.crop(
        (radius, radius, radius * 2, radius * 2)), (w - radius, h - radius)
    )

    rounded_corner_added_image.putalpha(alpha_mask)

    return rounded_corner_added_image

def resize_image(image: Image, size: Tuple[int, int]) -> Image.Image:
    resized_image = image.resize(size, Image.Resampling.LANCZOS)
    return resized_image
