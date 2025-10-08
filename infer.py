# infer.py
from ultralytics import YOLO
import cv2
import numpy as np

def pixel_width_from_mask(mask):
    mask_bin = (mask > 127).astype(np.uint8)
    dist = cv2.distanceTransform(mask_bin, cv2.DIST_L2, 5)
    return float(dist.max() * 2.0)  # max width in pixels

def detect_cracks(image_path, model_path="yolov8n-seg.pt", pixel_to_mm=None):
    model = YOLO(model_path)
    results = model.predict(source=image_path, imgsz=1280, conf=0.25)
    res = results[0]

    img = cv2.imread(image_path)
    annotated = img.copy()
    detections = []

    for mask, box, cls, conf in zip(res.masks.data, res.boxes.xyxy, res.boxes.cls, res.boxes.conf):
        mask_np = (mask.cpu().numpy() * 255).astype(np.uint8)
        mask_np = cv2.resize(mask_np, (img.shape[1], img.shape[0]))
        px_width = pixel_width_from_mask(mask_np)

        if pixel_to_mm:
            mm_width = px_width * pixel_to_mm
            if mm_width < 1:
                category = "Fine"
            elif mm_width < 3:
                category = "Medium"
            elif mm_width < 5:
                category = "Wide"
            else:
                category = "Very wide"
        else:
            category = "No Scale"

        x1, y1, x2, y2 = map(int, box.cpu().numpy())
        color = (0, 0, 255)
        annotated[mask_np > 127] = [0, 0, 255]
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated, f"{category} ({conf:.2f})", (x1, y1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        detections.append({
            "category": category,
            "confidence": float(conf),
            "px_width": round(px_width, 2),
            "mm_width": round(px_width * pixel_to_mm, 2) if pixel_to_mm else None
        })

    out_path = image_path.replace(".jpg", "_result.jpg")
    cv2.imwrite(out_path, annotated)
    return detections, out_path
