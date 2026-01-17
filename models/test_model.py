import sys
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# ---------------- CONFIG ----------------
MODEL_PATH = "models/saved/ai_media_detector.h5"
IMG_SIZE = (224, 224)
# ----------------------------------------

if len(sys.argv) < 2:
    print("❌ Please provide an image path")
    print("Usage: python models/test_model.py <image_path>")
    sys.exit(1)

IMAGE_PATH = sys.argv[1]

if not os.path.exists(IMAGE_PATH):
    print("❌ Image not found:", IMAGE_PATH)
    sys.exit(1)

# Load model
print("📦 Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)

# Load and preprocess image
img = image.load_img(IMAGE_PATH, target_size=IMG_SIZE)
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
pred = model.predict(img_array)[0][0]

# Interpret result
if pred >= 0.5:
    label = "🟢 REAL IMAGE"
    confidence = pred * 100
else:
    label = "🔴 FAKE IMAGE"
    confidence = (1 - pred) * 100

# Output
print("\n🧠 Prediction Result")
print("--------------------")
print(f"Prediction : {label}")
print(f"Confidence : {confidence:.2f}%")
