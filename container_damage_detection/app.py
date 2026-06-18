import tensorflow as tf

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense
)

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

train_data = train_datagen.flow_from_directory(
    "dataset/train",
    target_size=(128,128),
    batch_size=32,
    class_mode="binary"
)
test_data = test_datagen.flow_from_directory(
    "dataset/test",
    target_size=(128,128),
    batch_size=32,
    class_mode="binary"
)

model = Sequential()
model.add(
    Conv2D(
        32,
        (3,3),
        activation="relu",
        input_shape=(128,128,3)
    )
)
model.add(
    MaxPooling2D(
        pool_size=(2,2)
    )
)
model.add(
    Conv2D(
        64,
        (3,3),
        activation="relu"
    )
)
model.add(
    MaxPooling2D(
        pool_size=(2,2)
    )
)
model.add(
    Flatten()
)

model.add(
    Dense(
        128,
        activation="relu"
    )
)
model.add(
    Dense(
        1,
        activation="sigmoid"
    )
)

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    train_data,
    epochs=5,
    validation_data=test_data
)

model.save(
    "container_damage_model.h5"
)