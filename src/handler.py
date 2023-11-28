import io
import logging as logger
import time

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.algos.graph_pic_to_x import AlgoGraphPict2X
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

algo = AlgoGraphPict2X(dataset_hubble_v2_0, metadata_hubble_v2_0, nodes, graph)


def pic_2_hubble(uploaded_file: UploadedFile):
    img = Image.open(uploaded_file)

    logger.info(
        f"New image {img.format}, width: {img.width}, height: {img.height}"
    )

    logger.info("Generating composed image...")
    start_time = time.time()
    img_res = algo.build(img)
    end_time = time.time()
    logger.info(f"Time taken: {end_time - start_time} seconds")

    buffer = io.BytesIO()
    img_res.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer