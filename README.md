# 🧠 AI Media Detector  
**An Honest Approach to AI-Generated Image Detection**

---

## 📌 Overview
AI Media Detector is a web-based application that analyzes images and estimates whether they are **Real**, **AI-Generated**, or **Suspicious**.

Unlike many projects that claim unrealistic accuracy, this system is intentionally designed to be **honest about uncertainty**, especially when dealing with modern, high-quality AI-generated images from tools such as **Gemini**, **DALL·E 3**, and **Midjourney v6**.

The goal of this project is **risk estimation**, not false certainty.

---

## ✨ Key Features
- 📷 Image upload with live preview  
- 🧠 Deep Learning–based image analysis  
- 📊 Displays **both Real and AI confidence scores**  
- ⚖️ Three output classes:
  - **Real Image**
  - **AI Generated**
  - **Suspicious (Uncertain)**
- ❌ Avoids misleading 99–100% confidence claims  
- 🌐 REST API using FastAPI  
- 🎨 Simple, clean frontend (HTML, CSS, JavaScript)

---

## 🚀 Why This Project Is Different
Most AI image detectors force a confident answer even when the model is unsure.  
This project follows **responsible AI principles**:

> *If the model is not confident, the system does not lie.*

Modern AI-generated images can be visually indistinguishable from real photographs.  
Instead of misclassifying such images, this system labels them as **Suspicious**.

---

## 🧠 How the System Works
1. User uploads an image  
2. Image is preprocessed and passed to a trained CNN model  
3. The model outputs the probability of the image being **Real**  
4. AI probability is calculated as `1 − Real Probability`  
5. Final decision logic:
   - **Real Image** → Real confidence ≥ 90%
   - **AI Generated** → AI confidence ≥ 90%
   - **Suspicious** → Any value in between  

This approach ensures transparent and explainable predictions.

---

## ⚠️ Important Limitation (Very Important)
**AI image detection cannot be fully solved using visual data alone.**

Modern diffusion-based generators (Gemini, DALL·E, Midjourney) produce images that:
- Have realistic textures and lighting  
- Match natural frequency distributions  
- Lack traditional AI artifacts  

As a result:
- Some AI-generated images may be classified as **Real**
- This is a known **research limitation**, not a software bug

This behavior aligns with current academic research and real-world AI detection systems.

---

## 🧪 Example API Response
```json
{
  "prediction": "Suspicious",
  "confidence_real": 55.3,
  "confidence_ai": 44.7,
  "status": "uncertain",
  "note": "High-quality AI images may be indistinguishable from real photos."
}
