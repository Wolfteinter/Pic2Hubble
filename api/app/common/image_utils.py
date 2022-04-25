import random
from typing import Tuple

from PIL import Image


def get_average_per_channel(img: Image) -> Tuple[float, float, float]:
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


def is_square(image: Image) -> bool:
    width, height = image.size

    return height == width


def redim_image(img, max_dim=1500):
    width, height = img.width, img.height

    if not width > max_dim and not height > max_dim:
        return img

    if height > width:
        hpercent = (max_dim / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        res = img.resize((wsize, max_dim), Image.ANTIALIAS)
    else:
        wpercent = (max_dim/float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        res = img.resize((max_dim, hsize), Image.ANTIALIAS)

    return res