import streamlit as st

from src.test import test


def run():
    st.title("Pic 2 Hubble")
    st.write(
        "Upload an image and we'll convert it into a mosaic composed image"
        " using astronomical photos"
    )

    uploaded_file = st.file_uploader(
        "Choose an image file", type=["jpg", "jpeg", "png"], key="image"
    )

    if uploaded_file is not None:
        image_filename = uploaded_file.name

        st.image(uploaded_file, width=300)

        image_bytes = test(uploaded_file)

        filename = f"pic-2-hubble.png"
        st.download_button("Download", image_bytes, file_name=filename)


if __name__ == "__main__":
    run()