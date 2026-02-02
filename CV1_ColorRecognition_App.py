import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from utils import load_color_lookup_table, recognize_color

st.set_page_config(page_title="Color Recognition", layout="wide")
st.title("🎨 Color Recognition from Image")

colors_df = load_color_lookup_table()

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is None:
    st.info("Please upload an image to continue.")
    st.stop()

image = Image.open(uploaded_file).convert("RGB")
img_np = np.array(image)
h, w, _ = img_np.shape

st.markdown(
    """
**📌 Instruction:**  
Double-click on the image below to learn the color of that pixel.
"""
)

canvas = st_canvas(
    background_image=image,
    drawing_mode="point",
    stroke_width=1,
    height=h,
    width=w,
    key="canvas"
)

if canvas.json_data is not None:
    objects = canvas.json_data.get("objects", [])
    if len(objects) > 0:
        obj = objects[-1]
        x, y = int(obj["left"]), int(obj["top"])

        if 0 <= x < w and 0 <= y < h:
            rgb = img_np[y, x]
            color_name, _ = recognize_color(rgb, colors_df)

            st.markdown(
                f"""
**📍 Selected Point**
- X: {x}
- Y: {y}
- Color Name: **{color_name}**
- RGB: ({rgb[0]}, {rgb[1]}, {rgb[2]})
"""
            )

st.markdown("---")
st.image(img_np, caption="Uploaded Image", use_column_width=True)
