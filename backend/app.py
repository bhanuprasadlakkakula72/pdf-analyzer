from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import PyPDF2, io, os, requests

app = Flask(__name__, static_folder="../forntend", static_url_path="/")
CORS(app)

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")  # Add your Hugging Face token in Render's environment
HF_INFERENCE_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

def hf_summarize(text):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}", "Content-Type":"application/json"}
    resp = requests.post(HF_INFERENCE_URL, headers=headers, json={"inputs": text})
    resp.raise_for_status()
    out = resp.json()
    return out[0]["summary_text"]

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error":"No file uploaded"}), 400
    f = request.files['pdf']
    raw = f.read()
    reader = PyPDF2.PdfReader(io.BytesIO(raw))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    if not text.strip():
        return jsonify({"error":"No extractable text found in PDF."}), 400
    summary = hf_summarize(text[:10000])  # Limit to first 10k chars
    return jsonify({"summary": summary})

# Serve frontend
@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
