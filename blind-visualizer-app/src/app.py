import logging
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from inference_sdk import InferenceHTTPClient
import cv2
import os
import uuid

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# Folder setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
STYLE_FOLDER = os.path.join(BASE_DIR, "static", "styles")
RESULT_FOLDER = os.path.join(BASE_DIR, "static", "results")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STYLE_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["STYLE_FOLDER"] = STYLE_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

# Roboflow setup
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="jIJ4XwURLIYKDTzTWeha"
)

# Detection function
def detect_blinds(image_path):
    logging.info(f"Running detection on image: {image_path}")
    return CLIENT.infer(image_path, model_id="window-labeling/1")

# Overlay function
def overlay_image(background, overlay, x, y):
    h, w = overlay.shape[:2]
    for i in range(h):
        for j in range(w):
            if x + j >= background.shape[1] or y + i >= background.shape[0]:
                continue
            if overlay.shape[2] == 4:  # RGBA
                alpha = overlay[i, j, 3] / 255.0
                for c in range(3):
                    background[y + i, x + j, c] = (
                        alpha * overlay[i, j, c] + (1 - alpha) * background[y + i, x + j, c]
                    )

# Drawing function with style overlay
def draw_detections_with_style(image_path, result, style_path):
    image = cv2.imread(image_path)
    style = cv2.imread(style_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        logging.error(f"Failed to load image: {image_path}")
        raise FileNotFoundError(f"Image not found at {image_path}")
    if style is None:
        logging.error(f"Failed to load style image: {style_path}")
        raise FileNotFoundError(f"Style image not found at {style_path}")

    logging.info(f"Applying style from: {style_path}")

    for pred in result.get("predictions", []):
        x, y = int(pred["x"]), int(pred["y"])
        w, h = int(pred["width"]), int(pred["height"])
        x1, y1 = x - w // 2, y - h // 2

        resized_style = cv2.resize(style, (w, h))
        overlay_image(image, resized_style, x1, y1)

    output_filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join(app.config["RESULT_FOLDER"], output_filename)
    cv2.imwrite(output_path, image)

    logging.info(f"Saved annotated image: {output_path}")
    return output_filename

# Upload route
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files.get("image")
        styles = request.form.getlist("styles")
        response_type = request.form.get("response", "html")

        if not file or not styles:
            logging.warning("Upload failed: missing image or styles")
            return "Missing image or styles", 400

        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(image_path)

        logging.info(f"Image uploaded: {filename}")
        logging.info(f"Styles selected: {styles}")

        result = detect_blinds(image_path)

        annotated_files = []
        for style_name in styles:
            style_path = os.path.join(app.config["STYLE_FOLDER"], secure_filename(style_name))
            annotated_filename = draw_detections_with_style(image_path, result, style_path)
            annotated_files.append(annotated_filename)

        if response_type == "json":
            return jsonify({
                "images": [f"/static/results/{f}" for f in annotated_files],
                "share_urls": [f"{request.host_url}share/{os.path.splitext(f)[0]}" for f in annotated_files]
            })

        return render_template("result.html", original=filename, annotated_files=annotated_files)

    return render_template("upload.html")

# Share route
@app.route("/share/<image_id>")
def share_image(image_id):
    safe_filename = secure_filename(image_id) + ".png"
    logging.info(f"Serving shared image: {safe_filename}")
    return send_from_directory(app.config["RESULT_FOLDER"], safe_filename)

# Entry point
if __name__ == "__main__":
    app.run(debug=True)
