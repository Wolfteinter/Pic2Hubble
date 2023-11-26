import io

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile


def test(uploaded_file: UploadedFile) -> None:
    print(type(uploaded_file))

    image = Image.open(uploaded_file)

    print(image.size)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer