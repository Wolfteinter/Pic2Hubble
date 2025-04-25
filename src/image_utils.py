from functools import lru_cache
from typing import Tuple

from PIL import Image


def get_average_per_channel(img: Image) -> Tuple[float]:
    """Given an image, calculates R-average, G-average, and B-average values for
    each RGB channel. Returns a tuple with the 3 averages."""
    r, g, b = 0, 0, 0
    area = img.width * img.height

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))

            r += pixel[0]
            g += pixel[1]
            b += pixel[2]

    if not area:
        area = 1

    return (r / area, g / area, b / area)


@lru_cache(maxsize=1000)
def read_image(filepath: str) -> Image:
    """Read image from disk, use cache when it's possible."""
    return Image.open(filepath)


def resize_image(img: Image.Image, max_size: int = 1500) -> Image.Image:
    """Resize a PIL Image so its longest side is exactly max_size, preserving aspect ratio.
    This will upscale images smaller than max_size and downscale images larger than max_size.
    """
    width, height = img.size
    # Compute scaling factor so that the longest side becomes max_size
    scale = max_size / float(max(width, height))
    new_size = (int(round(width * scale)), int(round(height * scale)))

    # Use high-quality resampling filter
    return img.resize(new_size, Image.LANCZOS)
