import streamlit as st

from src.handler import pic_2_hubble
from src.utils import build_result_filename

IMAGE_KEY = "image"


def reset():
    if st.session_state.get(IMAGE_KEY):
        del st.session_state[IMAGE_KEY]


def run():
    st.title("Pic 2 Hubble")
    st.write(
        "Upload an image and we'll convert it into a mosaic composed image"
        " using astronomical photos."
    )
    st.markdown("[GitHub repo](https://github.com/Wolfteinter/Pic2Hubble)")

    st.warning(
        body="Non-profit project. Submitted and generated images are not being stored.",
        icon="⚠️",
    )

    uploaded_file = st.file_uploader(
        "Choose an image file", type=["jpg", "jpeg", "png"], key=IMAGE_KEY
    )

    if uploaded_file is not None:
        image_filename = uploaded_file.name

        st.image(uploaded_file, width=400)

        with st.spinner("Generating image"):
            image_bytes = pic_2_hubble(uploaded_file)

        filename = build_result_filename(image_filename)

        st.success("Image generated successfully!")

        st.image(image_bytes, width=400)

        st.download_button("Download", image_bytes, file_name=filename, on_click=reset)

        st.info(body="App created by Onder F. Campos and David Betancourt")


if __name__ == "__main__":
    run()
