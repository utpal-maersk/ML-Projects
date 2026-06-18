import tensorflow as tf

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (

    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout
)

from tensorflow.keras.preprocessing.image import (
    ImageDataGenerator
)

# ==========================================
# IMAGE SETTINGS
# ==========================================

IMG_SIZE = 128

BATCH_SIZE = 16

# ==========================================
# DATA GENERATOR
# ==========================================

train_datagen = ImageDataGenerator(

    rescale=1./255,

    validation_split=0.2,

    rotation_range=10,

    zoom_range=0.1,

    width_shift_range=0.1,

    height_shift_range=0.1
)

# ==========================================
# TRAIN DATA
# ==========================================

train_data = train_datagen.flow_from_directory(

    "dataset",

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="training"
)

# ==========================================
# VALIDATION DATA
# ==========================================

val_data = train_datagen.flow_from_directory(

    "dataset",

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="validation"
)

# ==========================================
# CLASS NAMES
# ==========================================

print(
    train_data.class_indices
)

# ==========================================
# CNN MODEL
# ==========================================

model = Sequential([

    Conv2D(
        32,
        (3,3),
        activation='relu',
        input_shape=(128,128,3)
    ),

    MaxPooling2D(2,2),

    Conv2D(
        64,
        (3,3),
        activation='relu'
    ),

    MaxPooling2D(2,2),

    Conv2D(
        128,
        (3,3),
        activation='relu'
    ),

    MaxPooling2D(2,2),

    Flatten(),

    Dense(
        128,
        activation='relu'
    ),

    Dropout(0.5),

    Dense(
        4,
        activation='softmax'
    )
])

# ==========================================
# COMPILE MODEL
# ==========================================

model.compile(

    optimizer='adam',

    loss='categorical_crossentropy',

    metrics=['accuracy']
)

# ==========================================
# TRAIN MODEL
# ==========================================

model.fit(

    train_data,

    validation_data=val_data,

    epochs=10
)

# ==========================================
# SAVE MODEL
# ==========================================

model.save(
    "document_classifier.h5"
)

print(
    "✅ Document Classifier Trained"
)