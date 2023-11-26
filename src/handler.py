import logging as logger

from src.graph import build_graph
from src.utils import load_dataset


logger.basicConfig(level=logger.INFO)


logger.info("Loading dataset...")
dataset_hubble_v2_0, metadata_hubble_v2_0 = load_dataset(
    name_dataset="hubble", version="v2.0", is_compressed=True
)

logger.info("Creating graph...")
nodes, graph = build_graph(
    name_dataset="hubble", version="v2.0", metadata_graph=metadata_hubble_v2_0
)


def greet():
    pass