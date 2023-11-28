import random

from PIL import Image

from src.constants import DIM_WINDOW
from src.image_utils import get_average_per_channel, read_image


class AlgoGraphPict2X:
    def __init__(self, dataset, metadata, nodes, graph):
        self.dataset = dataset
        self.metadata = metadata
        self.nodes = nodes
        self.graph = graph
        self.k = 3
        self.res = ""
    
    def __search(self, node, r, g, b):
        if len(node.images) > 0:
            self.res = random.choice(node.images)
        if r > node.r_range[1]:
            return self.__search(node.r, r, g, b)
        if g > node.g_range[1]:
            return self.__search(node.g, r, g, b)
        if b > node.b_range[1]:
            return self.__search(node.b, r, g, b)
        return node

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
                self.res = ""
                node = self.__search(self.graph, avg[0], avg[1], avg[2])
                if len(node.images) == 0:
                    nearest_image_name = node.res
                else:
                    nearest_image_name = random.choice(node.images)

                for i in enumerate(range(upper, lower)):
                    for j in enumerate(range(left, right)):
                        nearest_image = read_image(self.dataset[nearest_image_name])
                        new_pixel = nearest_image.getpixel((j[0], i[0]))
                        img.putpixel((j[1], i[1]), value=new_pixel)

        return img