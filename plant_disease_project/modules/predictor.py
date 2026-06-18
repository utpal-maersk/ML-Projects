import tensorflow as tf
import numpy as np

from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model(
    "plant_disease_model.keras"
)

class_names = [

    "Early_Blight",

    "Healthy",

    "Late_Blight"
]


def predict_disease(img):

    resized_img = img.resize(
        (224,224)
    )

    img_array = image.img_to_array(
        resized_img
    )

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = img_array / 255.0

    prediction = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = np.argmax(
        prediction
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = float(
        np.max(prediction) * 100
    )

    return (
        predicted_class,
        confidence,
        prediction
    )