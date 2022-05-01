import random

from PIL import Image

from api.app.common.constants import DIM_WINDOW
from api.app.common.image_utils import get_average_per_channel
from api.app.common.utils import compute_nearest_images


class AlgoPict2X:
    def __init__(self, dataset, metadata, k: int = 3) -> None:
        self.dataset = dataset
        self.metadata = metadata
        self.k = k

    def build(self, img: Image) -> Image:
        n, m = img.height, img.width

        for y in range(0, n, DIM_WINDOW):
            for x in range(0, m, DIM_WINDOW):
                left = x
                upper = y
                right = min(m-1, x+DIM_WINDOW)
                lower = min(n-1, y+DIM_WINDOW)
                window = img.crop((left, upper, right, lower))

                avg = get_average_per_channel(window)
                nearest_image_names = compute_nearest_images(self.metadata, avg, self.k)
                nearest_image_name = random.choice(nearest_image_names)

                for i in enumerate(range(upper, lower)):
                    for j in enumerate(range(left, right)):
                        new_pixel = self.dataset[nearest_image_name].getpixel(
                            (j[0], i[0])
                        )
                        img.putpixel((j[1], i[1]), value=new_pixel)

        return img
