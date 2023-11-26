import io
import time

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile


def test(uploaded_file: UploadedFile) -> None:
    image = Image.open(uploaded_file)

    print(image.size)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    time.sleep(3)

    return buffer