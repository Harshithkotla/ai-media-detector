import os
import sys
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

MODEL_PATH = "models/saved/ai_media_detector.h5"
IMG_SIZE = (224, 224)

REAL_DIR = "datasets/real"
FAKE_DIR = "datasets/fake"

model = load_model(MODEL_PATH)

def predict_image(path):
    img = load_img(path, target_size=IMG_SIZE)
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img, verbose=0)[0][0]
    return pred

def evaluate(folder, label, max_images=20):
    correct = 0
    files = os.listdir(folder)[:max_images]

    for f in files:
        p = predict_image(os.path.join(folder, f))
        is_fake = p < 0.5

        if (is_fake and label == "fake") or (not is_fake and label == "real"):
            correct += 1

    return correct, len(files)

real_correct, real_total = evaluate(REAL_DIR, "real")
fake_correct, fake_total = evaluate(FAKE_DIR, "fake")

print("\n📊 Evaluation Results")
print(f"REAL  : {real_correct}/{real_total} correct")
print(f"FAKE  : {fake_correct}/{fake_total} correct")
print(f"TOTAL : {real_correct + fake_correct}/{real_total + fake_total}")
