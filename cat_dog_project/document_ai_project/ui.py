# import streamlit as st
# import tensorflow as tf
# import easyocr

# from tensorflow.keras.preprocessing import image

# from PIL import Image

# import numpy as np
# import pandas as pd
# import re

# # ==========================================
# # LOAD AI MODEL
# # ==========================================

# model = tf.keras.models.load_model(
#     "document_classifier_mobilenet.keras"
# )

# # ==========================================
# # LOAD OCR
# # ==========================================

# reader = easyocr.Reader(['en'])

# # ==========================================
# # DOCUMENT CLASSES
# # ==========================================

# class_names = [

#     "Aadhar",

#     "DL",

#     "PAN",

#     "Passport"
# ]

# # ==========================================
# # STREAMLIT UI
# # ==========================================

# st.title(
#     "Enterprise Document AI"
# )

# st.write(
#     """
#     Supported Documents:
    
#     ✅ Aadhaar  
#     ✅ PAN  
#     ✅ Passport  
#     ✅ Driving License  
#     """
# )

# # ==========================================
# # FILE UPLOADER
# # ==========================================

# uploaded_file = st.file_uploader(

#     "Upload Document",

#     type=["jpg", "jpeg", "png"]
# )

# # ==========================================
# # MAIN PIPELINE
# # ==========================================

# if uploaded_file is not None:

#     # ======================================
#     # OPEN IMAGE
#     # ======================================

#     img = Image.open(
#         uploaded_file
#     ).convert("RGB")

#     # ======================================
#     # SHOW IMAGE
#     # ======================================

#     st.image(

#         img,

#         caption="Uploaded Document",

#         use_container_width=True
#     )

#     # ======================================
#     # AI PREPROCESSING
#     # ======================================

#     resized_img = img.resize(
#         (224,224)
#     )

#     img_array = image.img_to_array(
#         resized_img
#     )

#     img_array = np.expand_dims(

#         img_array,

#         axis=0
#     )

#     img_array = img_array / 255.0

#     # ======================================
#     # DOCUMENT CLASSIFICATION
#     # ======================================

#     prediction = model.predict(
#         img_array
#     )

#     predicted_index = np.argmax(
#         prediction
#     )

#     predicted_class = class_names[
#         predicted_index
#     ]

#     confidence = np.max(
#         prediction
#     ) * 100

#     # ======================================
#     # SHOW PREDICTION
#     # ======================================

#     st.success(

#         f"Predicted Document: "
#         f"{predicted_class}"
#     )

#     st.info(

#         f"Confidence: "
#         f"{confidence:.2f}%"
#     )

#     # ======================================
#     # SHOW PROBABILITIES
#     # ======================================

#     st.subheader(
#         "Prediction Probabilities"
#     )

#     for i, class_name in enumerate(class_names):

#         st.write(

#             f"{class_name}: "
#             f"{prediction[0][i]*100:.2f}%"
#         )

#     # ======================================
#     # OCR
#     # ======================================

#     results = reader.readtext(
#         np.array(img)
#     )

#     # ======================================
#     # OCR TEXT
#     # ======================================

#     ocr_lines = []

#     for result in results:

#         text = result[1]

#         ocr_lines.append(text)

#     extracted_text = "\n".join(
#         ocr_lines
#     )

#     # ======================================
#     # SHOW OCR TEXT
#     # ======================================

#     st.subheader(
#         "Extracted OCR Text"
#     )

#     st.code(
#         extracted_text
#     )

#     # ======================================
#     # FIELD EXTRACTION
#     # ======================================

#     extracted_fields = {}

#     # ======================================
#     # PAN EXTRACTION
#     # ======================================

#     if predicted_class == "PAN":

#         cleaned_text = re.sub(

#             r'[^A-Z0-9]',

#             '',

#             extracted_text.upper()
#         )

#         st.subheader(
#             "Cleaned PAN Text"
#         )

#         st.code(
#             cleaned_text
#         )

#         pan_match = re.search(

#             r'[A-Z]{5}[0-9]{4}[A-Z]',

#             cleaned_text
#         )

#         if pan_match:

#             pan_number = (
#                 pan_match.group()
#             )

#             extracted_fields[
#                 "PAN Number"
#             ] = pan_number

#             st.success(

#                 f"PAN Found: "
#                 f"{pan_number}"
#             )

#         else:

#             st.error(
#                 "PAN Not Found"
#             )

#     # ======================================
#     # AADHAAR EXTRACTION
#     # ======================================

#     elif predicted_class == "Aadhar":

#         aadhaar_match = re.search(

#             r'\d{4}\s?\d{4}\s?\d{4}',

#             extracted_text
#         )

#         if aadhaar_match:

#             aadhaar_number = (
#                 aadhaar_match.group()
#             )

#             aadhaar_number = (
#                 aadhaar_number.replace(
#                     " ",
#                     ""
#                 )
#             )

#             extracted_fields[
#                 "Aadhaar Number"
#             ] = aadhaar_number

#             st.success(

#                 f"Aadhaar Found: "
#                 f"{aadhaar_number}"
#             )

#         else:

#             st.error(
#                 "Aadhaar Not Found"
#             )

#     # ======================================
#     # PASSPORT EXTRACTION
#     # ======================================

#     elif predicted_class == "Passport":

#         cleaned_text = re.sub(

#             r'[^A-Z0-9]',

#             '',

#             extracted_text.upper()
#         )

#         passport_match = re.search(

#             r'[A-Z][0-9]{7}',

#             cleaned_text
#         )

#         if passport_match:

#             passport_number = (
#                 passport_match.group()
#             )

#             extracted_fields[
#                 "Passport Number"
#             ] = passport_number

#             st.success(

#                 f"Passport Found: "
#                 f"{passport_number}"
#             )

#         else:

#             st.error(
#                 "Passport Not Found"
#             )

#     # ======================================
#     # DRIVING LICENSE EXTRACTION
#     # ======================================

#     elif predicted_class == "DL":

#         cleaned_text = re.sub(

#             r'[^A-Z0-9]',

#             '',

#             extracted_text.upper()
#         )

#         dl_match = re.search(

#             r'[A-Z]{2}[0-9]{13}',

#             cleaned_text
#         )

#         if dl_match:

#             dl_number = (
#                 dl_match.group()
#             )

#             extracted_fields[
#                 "DL Number"
#             ] = dl_number

#             st.success(

#                 f"DL Found: "
#                 f"{dl_number}"
#             )

#         else:

#             st.error(
#                 "DL Not Found"
#             )

#     # ======================================
#     # SHOW EXTRACTED FIELDS
#     # ======================================

#     if extracted_fields:

#         st.subheader(
#             "Extracted Fields"
#         )

#         df = pd.DataFrame(

#             extracted_fields.items(),

#             columns=[
#                 "Field",
#                 "Value"
#             ]
#         )

#         st.table(df)

#     else:

#         st.warning(
#             "No fields extracted"
#         )

#     # ======================================
#     # JSON OUTPUT
#     # ======================================

#     st.subheader(
#         "JSON Output"
#     )

#     output_json = {

#         "document_type": predicted_class,

#         "confidence":
#         f"{confidence:.2f}%",

#         "fields": extracted_fields
#     }

#     st.json(
#         output_json
#     )

import streamlit as st
import tensorflow as tf
import pytesseract

from tensorflow.keras.preprocessing import image

from PIL import Image

import numpy as np
import pandas as pd
import re

# ==========================================
# LOAD AI MODEL
# ==========================================

model = tf.keras.models.load_model(
    "document_classifier_mobilenet.keras"
)

# ==========================================
# CLASS NAMES
# ==========================================

class_names = [

    "Aadhar",

    "DL",

    "PAN",

    "Passport"
]

# ==========================================
# STREAMLIT UI
# ==========================================

st.title(
    "Enterprise Document AI"
)

st.write(
    """
    Supported Documents:
    
    ✅ Aadhaar  
    ✅ PAN  
    ✅ Passport  
    ✅ Driving License  
    """
)

# ==========================================
# FILE UPLOADER
# ==========================================

uploaded_file = st.file_uploader(

    "Upload Document",

    type=["jpg", "jpeg", "png"]
)

# ==========================================
# MAIN PIPELINE
# ==========================================

if uploaded_file is not None:

    # ======================================
    # OPEN IMAGE
    # ======================================

    img = Image.open(
        uploaded_file
    ).convert("RGB")

    # ======================================
    # SHOW IMAGE
    # ======================================

    st.image(

        img,

        caption="Uploaded Document",

        use_container_width=True
    )

    # ======================================
    # AI PREPROCESSING
    # ======================================

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

    # ======================================
    # DOCUMENT CLASSIFICATION
    # ======================================

    prediction = model.predict(
        img_array
    )

    predicted_index = np.argmax(
        prediction
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = np.max(
        prediction
    ) * 100

    # ======================================
    # SHOW PREDICTION
    # ======================================

    st.success(

        f"Predicted Document: "
        f"{predicted_class}"
    )

    st.info(

        f"Confidence: "
        f"{confidence:.2f}%"
    )

    # ======================================
    # SHOW PROBABILITIES
    # ======================================

    st.subheader(
        "Prediction Probabilities"
    )

    for i, class_name in enumerate(class_names):

        st.write(

            f"{class_name}: "
            f"{prediction[0][i]*100:.2f}%"
        )

    # ======================================
    # OCR USING TESSERACT
    # ======================================

    ocr_text = pytesseract.image_to_string(
        img
    )

    # ======================================
    # SHOW OCR TEXT
    # ======================================

    st.subheader(
        "Extracted OCR Text"
    )

    st.code(
        ocr_text
    )

    # ======================================
    # FIELD EXTRACTION
    # ======================================

    extracted_fields = {}

    # ======================================
    # PAN EXTRACTION
    # ======================================

    if predicted_class == "PAN":

        cleaned_text = re.sub(

            r'[^A-Z0-9]',

            '',

            ocr_text.upper()
        )

        st.subheader(
            "Cleaned PAN Text"
        )

        st.code(
            cleaned_text
        )

        pan_match = re.search(

            r'[A-Z]{5}[0-9]{4}[A-Z]',

            cleaned_text
        )

        if pan_match:

            pan_number = (
                pan_match.group()
            )

            extracted_fields[
                "PAN Number"
            ] = pan_number

            st.success(

                f"PAN Found: "
                f"{pan_number}"
            )

        else:

            st.error(
                "PAN Not Found"
            )

    # ======================================
    # AADHAAR EXTRACTION
    # ======================================

    elif predicted_class == "Aadhar":

        aadhaar_match = re.search(

            r'\d{4}\s?\d{4}\s?\d{4}',

            ocr_text
        )

        if aadhaar_match:

            aadhaar_number = (
                aadhaar_match.group()
            )

            aadhaar_number = (
                aadhaar_number.replace(
                    " ",
                    ""
                )
            )

            extracted_fields[
                "Aadhaar Number"
            ] = aadhaar_number

            st.success(

                f"Aadhaar Found: "
                f"{aadhaar_number}"
            )

        else:

            st.error(
                "Aadhaar Not Found"
            )

    # ======================================
    # PASSPORT EXTRACTION
    # ======================================

    elif predicted_class == "Passport":

        cleaned_text = re.sub(

            r'[^A-Z0-9]',

            '',

            ocr_text.upper()
        )

        passport_match = re.search(

            r'[A-Z][0-9]{7}',

            cleaned_text
        )

        if passport_match:

            passport_number = (
                passport_match.group()
            )

            extracted_fields[
                "Passport Number"
            ] = passport_number

            st.success(

                f"Passport Found: "
                f"{passport_number}"
            )

        else:

            st.error(
                "Passport Not Found"
            )

    # ======================================
    # DRIVING LICENSE EXTRACTION
    # ======================================

    elif predicted_class == "DL":

        cleaned_text = re.sub(

            r'[^A-Z0-9]',

            '',

            ocr_text.upper()
        )

        dl_match = re.search(

            r'[A-Z]{2}[0-9]{13}',

            cleaned_text
        )

        if dl_match:

            dl_number = (
                dl_match.group()
            )

            extracted_fields[
                "DL Number"
            ] = dl_number

            st.success(

                f"DL Found: "
                f"{dl_number}"
            )

        else:

            st.error(
                "DL Not Found"
            )

    # ======================================
    # SHOW EXTRACTED FIELDS
    # ======================================

    if extracted_fields:

        st.subheader(
            "Extracted Fields"
        )

        df = pd.DataFrame(

            extracted_fields.items(),

            columns=[
                "Field",
                "Value"
            ]
        )

        st.table(df)

    else:

        st.warning(
            "No fields extracted"
        )

    # ======================================
    # JSON OUTPUT
    # ======================================

    st.subheader(
        "JSON Output"
    )

    output_json = {

        "document_type": predicted_class,

        "confidence":
        f"{confidence:.2f}%",

        "fields": extracted_fields
    }

    st.json(
        output_json
    )