import streamlit as st

import tensorflow as tf

from tensorflow.keras.preprocessing import image

import numpy as np

from PIL import Image
import cv2

model = tf.keras.models.load_model(
    "container_damage_model.h5"
)
st.title(
    "Container Damage Detection System"
)

uploaded_file = st.file_uploader(
    "Upload Container Image",
    type=["jpg", "jpeg", "png"]
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
        img_array = image.img_to_array(
        img
    )  
        img_array = np.expand_dims(
        img_array,
        axis=0
    )
        img_array = img_array / 255.0

        prediction = model.predict(
        img_array
    )
        if prediction[0][0] > 0.5:
             st.success(
        "Safe Container ✅"
    )

        else:
             st.error(
        "Damaged Container Detected ⚠️"
    )

    # Convert PIL image to OpenCV format
        img_cv = np.array(img)

    # Convert RGB to BGR
        img_cv = cv2.cvtColor(
        img_cv,
        cv2.COLOR_RGB2BGR
    )

    # Convert to grayscale
        gray = cv2.cvtColor(
        img_cv,
        cv2.COLOR_BGR2GRAY
    )

    # Blur image
        blur = cv2.GaussianBlur(
        gray,
        (5,5),
        0
    )

    # Threshold image
        _, thresh = cv2.threshold(
        blur,
        120,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Find contours
        contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw boxes around possible damage
        for contour in contours:
             area = cv2.contourArea(contour)

        if area > 500:

            x, y, w, h = cv2.boundingRect(
                contour
            )

            cv2.rectangle(
                img_cv,
                (x,y),
                (x+w,y+h),
                (0,0,255),
                3
            )

            cv2.putText(

                img_cv,

                "Possible Damage",

                (x, y-10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                (0,0,255),

                2
            )

    # Convert back to RGB
            result_img = cv2.cvtColor(
        img_cv,
        cv2.COLOR_BGR2RGB
    )

    # Show result image
        st.image(
        result_img,
        caption="Detected Damage Area",
        use_container_width=True
    )
               
              
        confidence = prediction[0][0]
        st.write(
        f"Prediction Score: {confidence:.2f}"
        )