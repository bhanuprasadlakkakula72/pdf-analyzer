const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("pdfFile");
const resultDiv = document.getElementById("result");

uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    resultDiv.innerText = "Uploading & summarizing...";
    
    const formData = new FormData();
    formData.append("pdf", fileInput.files[0]);

    try {
        const response = await fetch("https://pdf-analyzer-d4py.onrender.com/upload", {
            method: "POST",
            body: formData
        });
        const data = await response.json();

        if (data.summary) {
            resultDiv.innerText = data.summary;
        } else {
            resultDiv.innerText = "No summary (error)";
        }
    } catch (err) {
        console.error(err);
        resultDiv.innerText = "Failed: " + err.message;
    }
});
