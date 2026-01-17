import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import io
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

# ----------------------------
# App Init
# ----------------------------
app = FastAPI(
    title="AI Media Detector",
    description="API to estimate whether an image is AI-generated or real",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Load Model (ONCE at startup)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "saved", "ai_media_detector.h5")

print("📦 Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
model.trainable = False  # 🔒 inference only
print("✅ Model loaded successfully")

# ----------------------------
# Image Preprocessing
# ----------------------------
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    image = image.resize((224, 224))
    image = np.array(image, dtype=np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# ----------------------------
# Prediction Logic (FINAL & HONEST)
# ----------------------------
def predict_image(image_bytes: bytes) -> dict:
    img = preprocess_image(image_bytes)

    # Model predicts probability of REAL image
    raw_pred = float(model.predict(img, verbose=0)[0][0])

    # Clamp values to avoid fake 100%
    real_conf = max(min(raw_pred, 0.99), 0.01)
    ai_conf = max(min(1.0 - raw_pred, 0.99), 0.01)

    # Decision logic
    if real_conf >= 0.90:
        label = "Real Image"
        status = "confident"
    elif ai_conf >= 0.90:
        label = "AI Generated"
        status = "confident"
    else:
        label = "Suspicious"
        status = "uncertain"

    return {
        "prediction": label,
        "confidence_real": round(real_conf * 100, 2),
        "confidence_ai": round(ai_conf * 100, 2),
        "status": status,
        "note": (
            "Results are probabilistic. "
            "High-quality AI images (Gemini, DALL·E, Midjourney) "
            "may appear visually indistinguishable from real photos."
        )
    }

# ----------------------------
# API Route
# ----------------------------
@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported")

    image_bytes = await file.read()
    return predict_image(image_bytes)
