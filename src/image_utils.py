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
