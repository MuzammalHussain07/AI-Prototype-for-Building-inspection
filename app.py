import os
import streamlit as st
from infer import detect_cracks
from report import generate_word_report
from PIL import Image
import tempfile

# Ensure dependencies
os.system("pip install --quiet ultralytics==8.2.50 opencv-python-headless==4.9.0.80 torch==2.3.0 python-docx pillow numpy")

st.set_page_config(page_title="AI Building Inspection Tool", layout="wide")
st.title("🏗️ AI Prototype for Building Inspection")
st.write("Automatically detect cracks, spalling, and dampness in building inspection images.")

uploaded_files = st.file_uploader("Upload one or more images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    results = []
    temp_dir = tempfile.mkdtemp()

    for file in uploaded_files:
        image_path = os.path.join(temp_dir, file.name)
        image = Image.open(file)
        image.save(image_path)

        with st.spinner(f"Analyzing {file.name}..."):
            output_image, detected_data = detect_cracks(image_path)
            results.append(detected_data)

        st.image(output_image, caption=f"Processed: {file.name}", use_container_width=True)

    st.success("✅ Analysis complete!")
    st.download_button(
        label="📄 Download Word Report",
        data=generate_word_report(results),
        file_name="Inspection_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
