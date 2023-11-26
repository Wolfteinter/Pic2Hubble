import os
import math
import zipfile
from typing import List, Tuple, Union

import pandas as pd

from src.constants import BASE_DATASETS_PATH


def load_dataset(
    name_dataset: str, version: str, is_compressed=False
) -> Tuple[dict, pd.DataFrame]:
    """Load dataset (images paths and metadata) given its name, version and flag to 
    uncompress when necessary."""
    base_path = os.path.join(BASE_DATASETS_PATH.format(name_dataset, version))
    base_img_path = base_path + "/thumbnails/"
    metadata_path = base_path + "/metadata.csv"

    if is_compressed:
        with zipfile.ZipFile(base_path + "/thumbnails.zip", "r") as zip_ref:
            zip_ref.extractall(base_path)

    files = os.listdir(base_img_path)
    images = dict()

    for file in files:
        img_path = base_img_path + file
        images[file] = img_path
    
    metadata = pd.read_csv(metadata_path)

    return (images, metadata)


def compute_euclidian_distance(a: List[Union[int, float]], b: List[Union[int, float]]):
    acc = 0.0

    for a_i, b_i in zip(a, b):
        acc += (a_i - b_i)**2

    return math.sqrt(acc)


def compute_nearest_images(
    metadata: pd.DataFrame, avg_per_channel: tuple, k: int = 3
) -> list:
    distances = list() # list of tuples(distance, index)

    distances_serie = metadata.apply(
        lambda row: (
            compute_euclidian_distance(
                a=list(avg_per_channel),
                b=[row["r_avg"], row["g_avg"], row["b_avg"]]
            ),
            row.name
        ),
        axis=1
    )

    distances = list(distances_serie)

    distances.sort()

    nearest_images = list()
    for i in range(k):
        index = distances[i][1]
        nearest_images.append(metadata.iloc[index]["file"])

    return nearest_images
