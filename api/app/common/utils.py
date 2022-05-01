import base64
import io
import os
import zipfile
from math import sqrt
from typing import List, Union

import pandas as pd
from PIL import Image

from api.app.common.constants import BASE_DATASETS_PATH
from api.app.common.node import Node

csv_nodes = {}
nodes = {}
size = 15
range_dim = 17

metadata_graph = pd.read_csv(os.path.join(BASE_DATASETS_PATH.format('hubble', 'v2.0'), "metadata.csv"))

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


def compute_nearest_images(metadata: pd.DataFrame, avg_per_channel: tuple, k: int = 3):
    distances = list() # list of tuples(distance, index)
    assert len(avg_per_channel) == 3

    for row in metadata.iterrows():
        distance = compute_euclidian_distance(
            a=list(avg_per_channel), 
            b=[row[1]["r_avg"], row[1]["g_avg"], row[1]["b_avg"]]
        )

        distances.append((distance, row[0]))
    
    distances.sort()

    nearest_images = list()
    for i in range(k):
        index = distances[i][1]
        nearest_images.append(metadata.iloc[index]["file"])

    return nearest_images

def generate_graph_CSV(r_pk, g_pk, b_pk):
    pk = int(r_pk * pow(size, 2) +  g_pk*pow(size, 1) +  b_pk*pow(size, 0))
    if nodes.get(pk, -1) == -1:
        node = Node(r_pk, g_pk, b_pk, range_dim, size)
        if pk == 3374:
            rgb_mean = (
                (node.r_range[0] + node.r_range[0])/2 , 
                (node.g_range[0] + node.g_range[0])/2 , 
                (node.b_range[0] + node.b_range[0])/2
            )
            node.images = compute_nearest_images(metadata_graph, rgb_mean, k=3)
        else :
            node.images = csv_nodes[pk].images

        if r_pk == size - 1 and g_pk == size - 1 and b_pk == size - 1:
            return node
        if r_pk < size - 1:
            node.r = generate_graph_CSV(r_pk + 1, g_pk, b_pk)
        if g_pk < size - 1:
            node.g = generate_graph_CSV(r_pk, g_pk + 1, b_pk)
        if b_pk < size - 1:
            node.b = generate_graph_CSV(r_pk, g_pk, b_pk + 1)

        nodes[pk] = node
        return node
    return nodes.get(pk)

def build_graph(name_dataset: str, version: str) -> tuple:
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
    graph = generate_graph_CSV(0,0,0)
    return (nodes, graph)