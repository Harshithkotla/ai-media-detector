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

  // Reset UI
  resultDiv.classList.remove("hidden");
  predictionEl.innerText = "Analyzing image...";
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
      throw new Error("Server error");
    }

    const data = await response.json();

    predictionEl.innerText = "Prediction: " + data.prediction;
    confidenceEl.innerText =
      `Real: ${data.confidence_real}% | AI: ${data.confidence_ai}%`;
    statusEl.innerText = "Status: " + data.status;

  } catch (err) {
    predictionEl.innerText = "Prediction failed";
    confidenceEl.innerText = "";
    statusEl.innerText = "Unable to connect to server";
    console.error(err);
  }
}
