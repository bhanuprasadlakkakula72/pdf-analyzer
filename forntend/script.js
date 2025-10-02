// Handle file upload
document.getElementById("uploadBtn").addEventListener("click", async () => {
    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a PDF file first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        // Send file to Flask backend
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        const outputDiv = document.getElementById("output");

        if (result.error) {
            outputDiv.innerHTML = `<span style="color:red;">❌ ${result.error}</span>`;
        } else {
            outputDiv.innerHTML = `<strong>📄 Summary:</strong><br>${result.summary}`;
        }
    } catch (err) {
        console.error("Error:", err);
        alert("Something went wrong while uploading the file.");
    }
});
