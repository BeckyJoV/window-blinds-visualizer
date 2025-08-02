from ultralytics import YOLO
from PIL import Image
import io
import numpy as np

# Load your custom-trained model (replace with actual path)
model = YOLO("model/window_detector.pt")  # Use "yolov8n.pt" for testing or "best.pt" if fine-tuned

def detect_windows(image_bytes):
    # Convert bytes to PIL image
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    except Exception as e:
        raise ValueError(f"Invalid image bytes: {e}")

    image_np = np.array(image)

    # Run inference
    results = model(image_np)
    detections = []

    # Extract bounding boxes from first result
    if results and results[0].boxes is not None:
        for box in results[0].boxes:
            xyxy = box.xyxy[0].tolist()
            x1, y1, x2, y2 = map(int, xyxy)

            detections.append({
                "x": x1,
                "y": y1,
                "w": x2 - x1,
                "h": y2 - y1,
                "confidence": float(box.conf[0]) if box.conf is not None else None,
                "class": int(box.cls[0]) if box.cls is not None else None
            })

    return detections
