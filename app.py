# app.py
import streamlit as st
from infer import detect_cracks
from report import create_report
import os
try:
    import cv2
except ModuleNotFoundError:
    os.system("pip install opencv-python-headless==4.10.0.84")
    import cv2
st.set_page_config(page_title="Crack Detection Prototype", page_icon="🧱", layout="centered")

st.title("🧱 Building Crack Detection Prototype (YOLOv8)")
st.write("Upload an image — the app will automatically detect cracks and generate a report.")

uploaded = st.file_uploader("Upload image (JPG/PNG)", type=["jpg", "png", "jpeg"])

if uploaded:
    temp_path = f"temp_{uploaded.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded.read())

    st.image(temp_path, caption="Uploaded Image", use_container_width=True)

    if st.button("🔍 Run Crack Detection"):
        with st.spinner("Detecting cracks..."):
            detections, result_img = detect_cracks(temp_path, model_path="yolov8n-seg.pt")

        st.image(result_img, caption="Detection Result", use_container_width=True)

        st.write("### Detected Cracks:")
        st.table(detections)

        report_path = "Inspection_Report.docx"
        create_report(report_path, result_img, detections)

        with open(report_path, "rb") as f:
            st.download_button("📄 Download Report", f, file_name=report_path)

        st.success("✅ Report generated successfully!")

    # Clean up on refresh
    if os.path.exists(temp_path):
        os.remove(temp_path)
