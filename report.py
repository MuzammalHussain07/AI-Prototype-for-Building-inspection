from docx import Document
from io import BytesIO

def generate_word_report(detected_results):
    doc = Document()
    doc.add_heading("Building Inspection Report", level=1)
    doc.add_paragraph("This AI-generated report summarizes detected defects from uploaded images.")

    for idx, detections in enumerate(detected_results, start=1):
        doc.add_heading(f"Image {idx}", level=2)
        for det in detections:
            doc.add_paragraph(
                f"- Defect: {det['defect_type']}\n"
                f"  Confidence: {det['confidence']}\n"
                f"  Width: {det['width_mm']} mm\n"
                f"  Severity: {det['severity']}"
            )

    bio = BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()
