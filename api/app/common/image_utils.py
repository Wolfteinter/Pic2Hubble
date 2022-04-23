import random
from typing import Tuple

from PIL import Image


def get_average_per_channel(img: Image, n: int = None) -> Tuple[float, float, float]:
    r, g, b = 0, 0, 0

    if n:
        for _ in range(n):
            x = random.randint(0, img.width-1)
            y = random.randint(0, img.height-1)
            pixel = img.getpixel((x, y))

            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
        
        return (r / n, g / n, b / n)

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


def is_square(image: Image) -> bool:
    width, height = image.size

    return height == width