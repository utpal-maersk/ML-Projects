import tensorflow as tf

from tensorflow.keras.preprocessing.image import (
    ImageDataGenerator
)

from tensorflow.keras.applications import (
    MobileNetV2
)

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (

    GlobalAveragePooling2D,

    Dense,

    Dropout
)

# ==========================================
# SETTINGS
# ==========================================

IMG_SIZE = 224

BATCH_SIZE = 16

# ==========================================
# IMAGE GENERATOR
# ==========================================

train_datagen = ImageDataGenerator(

    rescale=1./255,

    validation_split=0.2,

    rotation_range=20,

    zoom_range=0.2,

    width_shift_range=0.2,

    height_shift_range=0.2,

    brightness_range=[0.8,1.2]
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
# LOAD MOBILENETV2
# ==========================================

base_model = MobileNetV2(

    weights='imagenet',

    include_top=False,

    input_shape=(224,224,3)
)

# ==========================================
# FREEZE BASE MODEL
# ==========================================

base_model.trainable = False

# ==========================================
# BUILD MODEL
# ==========================================

model = Sequential([

    base_model,

    GlobalAveragePooling2D(),

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
# MODEL SUMMARY
# ==========================================

model.summary()

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
    "document_classifier_mobilenet.keras"
)

print(
    "✅ MobileNetV2 Model Trained"
)