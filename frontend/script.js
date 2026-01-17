async function detectImage() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image");
    return;
  }

  // Preview image
  const preview = document.getElementById("preview");
  preview.innerHTML = `<img src="${URL.createObjectURL(file)}" />`;

  const formData = new FormData();
  formData.append("file", file);

  const resultDiv = document.getElementById("result");
  resultDiv.classList.add("hidden");

  try {
    const response = await fetch("http://127.0.0.1:8000/detect/image", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    document.getElementById("prediction").innerText =
      "Prediction: " + data.prediction;

    document.getElementById("confidence").innerText =
      `Real: ${data.confidence_real}% | AI: ${data.confidence_ai}%`;

    document.getElementById("status").innerText =
      "Status: " + data.status;

    resultDiv.classList.remove("hidden");

  } catch (err) {
    alert("Error connecting to server");
    console.error(err);
  }
}
