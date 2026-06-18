import streamlit as st

import tensorflow as tf

from tensorflow.keras.preprocessing import image

import numpy as np

from PIL import Image

model = tf.keras.models.load_model(
    "cat_dog_model.h5"
)

st.title(
    "Cat vs Dog Classifier"
)

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
        img = Image.open(
        uploaded_file
    )
        st.image(
            img,
            caption="Uploaded Image",
            use_container_width=True
        )
        img = img.resize((128,128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array,axis=0)
        img_array = img_array / 255.0
        prediction = model.predict(img_array)
        if prediction[0][0] > 0.5:
               st.success("Dog 🐶")
        else:
              st.success("Cat 🐱")
