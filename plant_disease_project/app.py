import streamlit as st
from PIL import Image

from modules.predictor import predict_disease

st.title("TEST APP")

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    img = Image.open(uploaded_file).convert("RGB")

    st.image(img)

    st.write("Image loaded successfully")

    try:

        predicted_class, confidence, prediction = (
            predict_disease(img)
        )

        st.success("Prediction completed")

        st.write(predicted_class)
        st.write(confidence)
        st.write(prediction)

    except Exception as e:

        st.error(str(e))