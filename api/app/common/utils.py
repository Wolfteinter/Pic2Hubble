import base64
import io
import os
import zipfile
from math import sqrt
from typing import List, Union

import pandas as pd
from PIL import Image

from api.app.common.constants import BASE_DATASETS_PATH, GRAPH_SIZE, GRAPH_RANGE_DIM
from api.app.common.node import Node

nodes = dict()
csv_nodes = dict()


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


def load_dataset(name_dataset: str, version: str, is_compressed=False) -> tuple:
    base_path = os.path.join(BASE_DATASETS_PATH.format(name_dataset, version))
    base_img_path = base_path + "/thumbnails/"
    metadata_path = base_path + "/metadata.csv"

    if is_compressed:
        uncompress_thumbnails(
            src=base_path + "/thumbnails.zip", dest=base_path
        )


    files = os.listdir(base_img_path)
    images = dict()

    for file in files:
        img_path = base_img_path + file
        images[file] = Image.open(img_path)
    
    metadata = pd.read_csv(metadata_path)

    return (images, metadata)


def uncompress_thumbnails(src: str, dest: str):
    with zipfile.ZipFile(src, "r") as zip_ref:
        zip_ref.extractall(dest)


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


def generate_graph_CSV(r_pk, g_pk, b_pk, metadata_graph: pd.DataFrame):
    pk = int(
        r_pk * pow(GRAPH_SIZE, 2) 
        + g_pk*pow(GRAPH_SIZE, 1) 
        + b_pk*pow(GRAPH_SIZE, 0)
    )

    if nodes.get(pk, -1) == -1:
        node = Node(r_pk, g_pk, b_pk, GRAPH_RANGE_DIM, GRAPH_SIZE)
        if pk == 3374:
            rgb_mean = (
                (node.r_range[0] + node.r_range[0])/2 , 
                (node.g_range[0] + node.g_range[0])/2 , 
                (node.b_range[0] + node.b_range[0])/2
            )
            node.images = compute_nearest_images(metadata_graph, rgb_mean, k=3)
        else :
            node.images = csv_nodes[pk].images

        if r_pk == GRAPH_SIZE-1 and g_pk == GRAPH_SIZE-1 and b_pk == GRAPH_SIZE-1:
            return node
        if r_pk < GRAPH_SIZE - 1:
            node.r = generate_graph_CSV(r_pk + 1, g_pk, b_pk, metadata_graph)
        if g_pk < GRAPH_SIZE - 1:
            node.g = generate_graph_CSV(r_pk, g_pk + 1, b_pk, metadata_graph)
        if b_pk < GRAPH_SIZE - 1:
            node.b = generate_graph_CSV(r_pk, g_pk, b_pk + 1, metadata_graph)

        nodes[pk] = node
        return node

    return nodes.get(pk)


def build_graph(name_dataset: str, version: str, metadata_graph: pd.DataFrame) -> tuple:
    base_path = os.path.join(BASE_DATASETS_PATH.format(name_dataset, version), "graph.csv")
    graph_metadata = pd.read_csv(base_path)
    for row in graph_metadata.iterrows():
        node = Node()
        node.pk = int(row[1]['pk'])
        node.r_range = (row[1]['r_range_l'], row[1]['r_range_r'])
        node.g_range = (row[1]['g_range_l'], row[1]['g_range_r'])
        node.b_range = (row[1]['b_range_l'], row[1]['b_range_r'])
        images = str(row[1]['images'])
        node.images = images.split(";") if images != 'nan' else []
        csv_nodes[node.pk] = node

    graph = generate_graph_CSV(0, 0, 0, metadata_graph)

    return (nodes, graph)