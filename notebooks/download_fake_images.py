import os
import requests
import time

SAVE_DIR = "datasets/fake"
NUM_IMAGES = 1000

os.makedirs(SAVE_DIR, exist_ok=True)

print("🚀 Downloading fake images into datasets/fake ...", flush=True)

for i in range(NUM_IMAGES):
    try:
        url = "https://thispersondoesnotexist.com/"
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            with open(os.path.join(SAVE_DIR, f"fake_{i}.jpg"), "wb") as f:
                f.write(r.content)

            if (i + 1) % 50 == 0:
                print(f"✅ Downloaded {i+1}/{NUM_IMAGES}", flush=True)

        time.sleep(0.6)  # avoid blocking

    except Exception as e:
        print("❌ Error:", e, flush=True)
        time.sleep(2)

print("🎉 Done! Fake images saved in datasets/fake")
