from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
def create_report(
    file_name,
    prediction,
    confidence,
    description,
    treatment
):

    pdf_file = "plant_report.pdf"

    doc = SimpleDocTemplate(
        pdf_file
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Plant Disease Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1,12)
    )

    elements.append(
        Paragraph(
            f"File: {file_name}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Prediction: {prediction}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Confidence: {confidence:.2f}%",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Description: {description}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            "Treatment:",
            styles["Heading2"]
        )
    )

    for item in treatment:

        elements.append(
            Paragraph(
                f". {item}",
                styles["BodyText"]
            )
        )

    doc.build(
        elements
    )

    return pdf_file