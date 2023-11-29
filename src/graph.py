import os

import pandas as pd

from src.constants import BASE_DATASETS_PATH, GRAPH_RANGE_DIM, GRAPH_SIZE
from src.utils import compute_nearest_images

nodes = dict()
csv_nodes = dict()


class Node:
    def __init__(self, r_pk=0, g_pk=0, b_pk=0, range_dim=0, size=0):
        # Images related
        self.images = []
        # Identification
        self.pk = r_pk * pow(size, 2) + g_pk * pow(size, 1) + b_pk * pow(size, 0)
        # Ranges
        self.r_range = (r_pk * range_dim, (r_pk * range_dim) + range_dim)
        self.g_range = (g_pk * range_dim, (g_pk * range_dim) + range_dim)
        self.b_range = (b_pk * range_dim, (b_pk * range_dim) + range_dim)
        # Childrens
        self.r = None
        self.g = None
        self.b = None

    def __repr__(self):
        return (
            str(self.pk)
            + " , "
            + str(self.r_range)
            + " , "
            + str(self.g_range)
            + " , "
            + str(self.b_range)
        )


def generate_graph_csv(r_pk: int, g_pk: int, b_pk: int, metadata_graph: pd.DataFrame):
    pk = int(
        r_pk * pow(GRAPH_SIZE, 2)
        + g_pk * pow(GRAPH_SIZE, 1)
        + b_pk * pow(GRAPH_SIZE, 0)
    )

    if nodes.get(pk, -1) == -1:
        node = Node(r_pk, g_pk, b_pk, GRAPH_RANGE_DIM, GRAPH_SIZE)
        if pk == 3374:
            rgb_mean = (
                (node.r_range[0] + node.r_range[0]) / 2,
                (node.g_range[0] + node.g_range[0]) / 2,
                (node.b_range[0] + node.b_range[0]) / 2,
            )
            node.images = compute_nearest_images(metadata_graph, rgb_mean, k=3)
        else:
            node.images = csv_nodes[pk].images

        if r_pk == GRAPH_SIZE - 1 and g_pk == GRAPH_SIZE - 1 and b_pk == GRAPH_SIZE - 1:
            return node
        if r_pk < GRAPH_SIZE - 1:
            node.r = generate_graph_csv(r_pk + 1, g_pk, b_pk, metadata_graph)
        if g_pk < GRAPH_SIZE - 1:
            node.g = generate_graph_csv(r_pk, g_pk + 1, b_pk, metadata_graph)
        if b_pk < GRAPH_SIZE - 1:
            node.b = generate_graph_csv(r_pk, g_pk, b_pk + 1, metadata_graph)

        nodes[pk] = node
        return node

    return nodes.get(pk)


def build_graph(name_dataset: str, version: str, metadata_graph: pd.DataFrame) -> tuple:
    base_path = os.path.join(
        BASE_DATASETS_PATH.format(name_dataset, version), "graph.csv"
    )
    graph_metadata = pd.read_csv(base_path)

    for row in graph_metadata.iterrows():
        node = Node()
        node.pk = int(row[1]["pk"])
        node.r_range = (row[1]["r_range_l"], row[1]["r_range_r"])
        node.g_range = (row[1]["g_range_l"], row[1]["g_range_r"])
        node.b_range = (row[1]["b_range_l"], row[1]["b_range_r"])
        images = str(row[1]["images"])
        node.images = images.split(";") if images != "nan" else []
        csv_nodes[node.pk] = node

    graph = generate_graph_csv(0, 0, 0, metadata_graph)

    return (nodes, graph)
