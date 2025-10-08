import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import tempfile

# Load pretrained YOLOv8 model
# You can replace this with your own fine-tuned model later
model = YOLO("https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt")

def detect_cracks(image_bytes):
    # Save temp file for YOLO
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    # Run YOLO inference
    results = model(tmp_path)

    # Get image with bounding boxes
    annotated = results[0].plot()
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    # Detection summary (class name + confidence)
    detections = []
    for box in results[0].boxes:
        cls = model.names[int(box.cls)]
        conf = float(box.conf)
        detections.append(f"{cls} ({conf*100:.1f}% confidence)")

    # Convert image to display
    result_image = Image.fromarray(annotated_rgb)
    return result_image, detections
