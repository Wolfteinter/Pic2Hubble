from api.app.common.utils import load_dataset
from api.app.common.utils import build_graph

dataset_hubble_v1_0, metadata_hubble_v1_0 = load_dataset(
    name_dataset="hubble", version="v1.0"
)

dataset_hubble_v2_0, metadata_hubble_v2_0 = load_dataset(
    name_dataset="hubble", version="v2.0", is_compressed=True
)

nodes, graph = build_graph(
    name_dataset="hubble", version="v2.0", metadata_graph=metadata_hubble_v2_0
)