from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from inference_sdk import InferenceHTTPClient
import cv2
import os
import uuid

app = Flask(__name__)

# Folder setup
UPLOAD_FOLDER = "static/uploads"
STYLE_FOLDER = "static/styles"
RESULT_FOLDER = "static/results"
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
        raise FileNotFoundError(f"Image not found at {image_path}")
    if style is None:
        raise FileNotFoundError(f"Style image not found at {style_path}")

    for pred in result.get("predictions", []):
        x, y = int(pred["x"]), int(pred["y"])
        w, h = int(pred["width"]), int(pred["height"])
        x1, y1 = x - w // 2, y - h // 2

        resized_style = cv2.resize(style, (w, h))
        overlay_image(image, resized_style, x1, y1)

    output_filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join(app.config["RESULT_FOLDER"], output_filename)
    cv2.imwrite(output_path, image)
    return output_filename

# Upload route
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files.get("image")
        style = request.form.get("style")
        response_type = request.form.get("response", "html")

        if file and style:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(image_path)

            style_path = os.path.join(app.config["STYLE_FOLDER"], secure_filename(style))
            result = detect_blinds(image_path)
            annotated_filename = draw_detections_with_style(image_path, result, style_path)

            image_id = os.path.splitext(annotated_filename)[0]
            share_url = f"{request.host_url}share/{image_id}"

            if response_type == "json":
                return jsonify({
                    "image_url": f"/static/results/{annotated_filename}",
                    "share_url": share_url
                })

            return render_template("result.html", original=filename, annotated=annotated_filename)

    return render_template("upload.html")

# Share route
@app.route("/share/<image_id>")
def share_image(image_id):
    safe_filename = secure_filename(image_id) + ".png"
    return send_from_directory(app.config["RESULT_FOLDER"], safe_filename)
