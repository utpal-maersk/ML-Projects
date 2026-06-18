import streamlit as st
from PIL import Image
import pytesseract

st.title(
    "AI Invoice OCR System"
)

uploaded_file = st.file_uploader(
    "Upload Invoice Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    )

    st.image(
        image,
        caption="Uploaded Invoice",
        use_container_width=True
    )

    # Perform OCR on the uploaded image
    text = pytesseract.image_to_string(image)

    st.subheader("Extracted Text:")
    st.write(text)  

    extracted_text = pytesseract.image_to_string(
    image
    )
    st.subheader(
    "Extracted Text"
    )

    st.text_area(
        "OCR Output",
        extracted_text,
        height=300
    )
    