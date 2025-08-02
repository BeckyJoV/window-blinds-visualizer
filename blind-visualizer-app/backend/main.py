from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import uuid
import os
from detect import detect_windows  # ✅ YOLOv8 detection function

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🔼 Upload endpoint
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    extension = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": filename, "url": f"/uploads/{filename}"}

# 🔍 Detection endpoint
@app.get("/detect/{filename}")
def detect(filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return JSONResponse(status_code=404, content={"error": "File not found"})

    with open(filepath, "rb") as f:
        image_bytes = f.read()

    boxes = detect_windows(image_bytes)
    return {"windows": boxes}
