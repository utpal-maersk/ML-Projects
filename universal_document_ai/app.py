import streamlit as st
import easyocr
from PIL import Image, ImageDraw
import pandas as pd
import re
from pdf2image import convert_from_bytes
import numpy as np
import ssl
import certifi
import cv2


# ==========================================
# SSL FIX
# ==========================================

ssl._create_default_https_context = (
    lambda: ssl.create_default_context(
        cafile=certifi.where()
    )
)

# ==========================================
# EASYOCR READER
# ==========================================

reader = easyocr.Reader(['en'])

# ==========================================
# DOCUMENT RULES
# ==========================================

DOCUMENT_RULES = {

    "PAN Card": {

        "keywords": [

            "income tax",

            "permanent account",

            "govt",

            "government",

            "india",

            "pan",

            "father",

            "signature"
        ]
    },

    "Aadhaar Card": {

        "keywords": [

            "aadhaar",

            "government of india",

            "unique identification authority",

            "dob",

            "male",

            "female",

            "year of birth",

            "uidai"
        ]
    },

    "Passport": {

        "keywords": [

            "passport",

            "republic of india",

            "nationality",

            "place of birth",

            "date of issue",

            "date of expiry"
        ]
    },

    "Driving License": {

        "keywords": [

            "driving",

            "license",

            "transport",

            "motor",

            "vehicle",

            "valid till"
        ]
    }
}

# ==========================================
# DOCUMENT CLASSIFIER
# ==========================================

def classify_document(text):

    text_lower = text.lower()

    scores = {}

    # ======================================
    # SCORE EACH DOCUMENT
    # ======================================

    for document_name, config in DOCUMENT_RULES.items():

        score = 0

        for keyword in config["keywords"]:

            if keyword.lower() in text_lower:

                score += 1

        scores[document_name] = score

    # ======================================
    # BEST MATCH
    # ======================================

    best_document = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_document]

    # ======================================
    # MINIMUM SCORE
    # ======================================

    if best_score >= 2:

        return best_document

    return "Unknown Document"

# ==========================================
# FAILURE EXPLANATION ENGINE
# ==========================================

def explain_document_failure(text):

    text_lower = text.lower()

    # LOW OCR TEXT
    if len(text.strip()) < 20:

        return (
            "⚠️ Very little text detected. "
            "Image may be blurry or unclear."
        )

    # OCR NOISE
    if len(text.split()) < 5:

        return (
            "⚠️ OCR extracted very limited text. "
            "Try better image quality."
        )

    # PAN FAILURE
    if (
        "income" in text_lower
        or "tax" in text_lower
        or "pan" in text_lower
    ):

        return (
            "⚠️ PAN keywords detected "
            "but PAN number pattern missing."
        )

    # AADHAAR FAILURE
    if (
        "aadhaar" in text_lower
        or "uidai" in text_lower
    ):

        return (
            "⚠️ Aadhaar keywords detected "
            "but Aadhaar number missing."
        )

    # PASSPORT FAILURE
    if "passport" in text_lower:

        return (
            "⚠️ Passport detected "
            "but passport number missing."
        )

    # DL FAILURE
    if (
        "driving" in text_lower
        or "license" in text_lower
    ):

        return (
            "⚠️ Driving License keywords detected "
            "but DL number missing."
        )

    return (
        "⚠️ Unable to confidently identify document."
    )

# ==========================================
# FIELD EXTRACTION ENGINE
# ==========================================

def extract_fields(document_type, text):

    extracted_data = {}

    # ======================================
    # PAN CARD
    # ======================================

    if document_type == "PAN Card":

        pan_match = re.search(
            r'[A-Z]{5}[0-9]{4}[A-Z]',
            text.upper()
        )

        if pan_match:

            extracted_data["PAN Number"] = (
                pan_match.group()
            )

        else:

            extracted_data["PAN Number"] = (
                "Not Found"
            )

    # ======================================
    # AADHAAR CARD
    # ======================================

    elif document_type == "Aadhaar Card":

        aadhaar_match = re.search(
            r'\d{4}\s\d{4}\s\d{4}',
            text
        )

        if aadhaar_match:

            extracted_data["Aadhaar Number"] = (
                aadhaar_match.group()
            )

        else:

            extracted_data["Aadhaar Number"] = (
                "Not Found"
            )

    # ======================================
    # PASSPORT
    # ======================================

    elif document_type == "Passport":

        passport_match = re.search(
            r'[A-Z][0-9]{7}',
            text.upper()
        )

        if passport_match:

            extracted_data["Passport Number"] = (
                passport_match.group()
            )

        else:

            extracted_data["Passport Number"] = (
                "Not Found"
            )

    # ======================================
    # DRIVING LICENSE
    # ======================================

    elif document_type == "Driving License":

        dl_match = re.search(
            r'[A-Z]{2}[0-9]{2}[0-9]{11}',
            text.upper()
        )

        if dl_match:

            extracted_data["DL Number"] = (
                dl_match.group()
            )

        else:

            extracted_data["DL Number"] = (
                "Not Found"
            )

    return extracted_data

# ==========================================
# VALIDATION ENGINE
# ==========================================

def validate_field(value):

    if value == "Not Found":

        return "❌ Invalid"

    return "✅ Valid"

# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(

    page_title="Universal Enterprise Document AI",

    layout="wide"
)

st.title(
    "Universal Enterprise Document AI"
)

st.write(
    """
    Upload:
    - PAN Card
    - Aadhaar Card
    - Passport
    - Driving License
    - PDF Documents
    """
)

# ==========================================
# FILE UPLOADER
# ==========================================

uploaded_file = st.file_uploader(

    "Upload Document",

    type=["jpg", "jpeg", "png", "pdf"]
)

# ==========================================
# MAIN PROCESSING
# ==========================================

if uploaded_file is not None:

    # ======================================
    # PDF SUPPORT
    # ======================================

    if uploaded_file.type == "application/pdf":

        pages = convert_from_bytes(
            uploaded_file.read()
        )

        img = pages[0]

    else:

        img = Image.open(uploaded_file)

    # ======================================
    # SHOW ORIGINAL IMAGE
    # ======================================

    st.image(

        img,

        caption="Uploaded Document",

        use_container_width=True
    )

    # ======================================
    # IMAGE TO NUMPY
    # ======================================

    img_np = np.array(img)

    # ======================================
    # IMAGE PREPROCESSING
    # ======================================

    gray = cv2.cvtColor(
        img_np,
        cv2.COLOR_RGB2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    processed = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # ======================================
    # OCR EXTRACTION
    # ======================================

    results = reader.readtext(
        processed
    )

    # ======================================
    # DRAW BOUNDING BOXES
    # ======================================

    draw = ImageDraw.Draw(img)

    extracted_text = ""

    for result in results:

        bbox = result[0]

        text = result[1]

        confidence = result[2]

        extracted_text += text + "\n"

        # BOX COORDINATES
        top_left = tuple(
            map(int, bbox[0])
        )

        bottom_right = tuple(
            map(int, bbox[2])
        )

        # GREEN RECTANGLE
        draw.rectangle(

            [top_left, bottom_right],

            outline="green",

            width=3
        )

        # CONFIDENCE SCORE
        draw.text(

            top_left,

            f"{confidence:.2f}",

            fill="red"
        )

    # ======================================
    # SHOW OCR IMAGE
    # ======================================

    st.image(

        img,

        caption="OCR Bounding Boxes",

        use_container_width=True
    )

    # ======================================
    # SHOW OCR TEXT
    # ======================================

    st.subheader(
        "Extracted OCR Text"
    )

    st.code(
        extracted_text
    )

    # ======================================
    # DOCUMENT CLASSIFICATION
    # ======================================

    document_type = classify_document(
        extracted_text
    )

    st.subheader(
        "Detected Document Type"
    )

    # ======================================
    # SUCCESS / FAILURE
    # ======================================

    if document_type == "Unknown Document":

        st.error(
            document_type
        )

        failure_reason = explain_document_failure(
            extracted_text
        )

        st.warning(
            failure_reason
        )

    else:

        st.success(
            document_type
        )

    # ======================================
    # FIELD EXTRACTION
    # ======================================

    extracted_fields = extract_fields(

        document_type,

        extracted_text
    )

    # ======================================
    # CREATE TABLE
    # ======================================

    table_data = []

    for field, value in extracted_fields.items():

        validation = validate_field(
            value
        )

        table_data.append({

            "Field": field,

            "Value": value,

            "Validation": validation
        })

    # ======================================
    # SHOW TABLE
    # ======================================

    if table_data:

        df = pd.DataFrame(table_data)

        st.subheader(
            "Extracted Document Fields"
        )

        st.table(df)

    # ======================================
    # JSON OUTPUT
    # ======================================

    st.subheader(
        "JSON Output"
    )

    json_output = {

        "document_type": document_type,

        "fields": extracted_fields
    }

    st.json(json_output)