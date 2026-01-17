async function detectImage() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image first");
    return;
  }

  // Preview image
  const preview = document.getElementById("preview");
  preview.innerHTML = `<img src="${URL.createObjectURL(file)}" />`;

  const formData = new FormData();
  formData.append("file", file);

  const resultDiv = document.getElementById("result");
  const predictionEl = document.getElementById("prediction");
  const confidenceEl = document.getElementById("confidence");
  const statusEl = document.getElementById("status");

  // 🔄 Reset UI + show loading state
  resultDiv.classList.remove("hidden");
  predictionEl.innerText = "Analyzing image… please wait ⏳";
  confidenceEl.innerText = "";
  statusEl.innerText = "";

  try {
    const response = await fetch(
      "https://ai-media-detector.onrender.com/detect/image",
      {
        method: "POST",
        body: formData
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "Server error");
    }

    const data = await response.json();

    // ✅ Update UI with results
    predictionEl.innerText = "Prediction: " + data.prediction;
    confidenceEl.innerText =
      `Real: ${data.confidence_real}% | AI: ${data.confidence_ai}%`;
    statusEl.innerText = "Status: " + data.status;

  } catch (err) {
    // ⚠️ Cold start / network error handling
    resultDiv.classList.remove("hidden");
    predictionEl.innerText = "Server is waking up ⏳";
    confidenceEl.innerText = "Please try again in 20–30 seconds";
    statusEl.innerText = "Free backend cold start";
    console.error("Fetch error:", err);
  }
}
