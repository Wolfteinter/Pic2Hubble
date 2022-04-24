import base64
import io
import os
from math import sqrt
from typing import List, Union

import pandas as pd
from PIL import Image

from api.app.common.constants import BASE_DATASETS_PATH


def compute_euclidian_distance(a: List[Union[int, float]], b: List[Union[int, float]]):
    acc = 0.0

    for a_i, b_i in zip(a, b):
        acc += (a_i - b_i)**2

    return sqrt(acc)


def image_to_base64(img: Image):
    rawBytes = io.BytesIO()
    img.save(rawBytes, "png")
    rawBytes.seek(0)

    return base64.b64encode(rawBytes.read())


def load_dataset(name_dataset: str, version: str) -> tuple:
    base_path = os.path.join(BASE_DATASETS_PATH.format(name_dataset, version))
    base_img_path = base_path + "/thumbnails/"
    metadata_path = base_path + "/metadata.csv"

    files = os.listdir(base_img_path)
    images = dict()

    for file in files:
        img_path = base_img_path + file
        images[file] = Image.open(img_path)
    
    metadata = pd.read_csv(metadata_path)

    return (images, metadata)