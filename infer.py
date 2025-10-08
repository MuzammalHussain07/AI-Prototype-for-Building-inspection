import cv2
from ultralytics import YOLO
from PIL import Image
import numpy as np

# Load pretrained YOLOv8 model
model = YOLO("keremberke/yolov8n-crack-segmentation")

def detect_cracks(image_path):
    results = model(image_path)
    annotated = results[0].plot()  # Bounding boxes + masks drawn

    # Convert to PIL Image
    image_pil = Image.fromarray(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))

    detected_data = []
    for box in results[0].boxes:
        conf = float(box.conf)
        cls = int(box.cls)
        label = model.names[cls]
        width_mm = estimate_crack_width(conf)  # simulated width estimation
        severity = classify_crack(width_mm)
        detected_data.append({
            "defect_type": label,
            "confidence": round(conf, 2),
            "width_mm": width_mm,
            "severity": severity,
        })

    return image_pil, detected_data


def estimate_crack_width(confidence):
    # Mock width estimator based on confidence (for prototype)
    if confidence > 0.85:
        return 5.5
    elif confidence > 0.7:
        return 3.0
    elif confidence > 0.5:
        return 1.5
    else:
        return 0.8


def classify_crack(width):
    if width < 1:
        return "Fine (<1mm)"
    elif width < 3:
        return "Medium (<3mm)"
    elif width < 5:
        return "Wide (<5mm)"
    else:
        return "Very Wide (>5mm)"
