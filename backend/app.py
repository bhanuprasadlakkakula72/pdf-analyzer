from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import PyPDF2, io, os, requests

app = Flask(__name__)
CORS(app)

# -------------------------
# Serve the frontend files
# -------------------------
@app.route("/")
def index():
    return send_from_directory("../forntend", "index.html")  # make sure path is correct

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../forntend", path)

# -------------------------
# Hugging Face summarization
# -------------------------
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")  # Set this in Render environment variables
HF_INFERENCE_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

def hf_summarize(text):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}", "Content-Type":"application/json"}
    resp = requests.post(HF_INFERENCE_URL, headers=headers, json={"inputs": text})
    resp.raise_for_status()
    out = resp.json()
    return out[0]["summary_text"]

# -------------------------
# PDF Upload & Summarization
# -------------------------
@app.route("/upload", methods=["POST"])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error":"No file uploaded"}), 400
    f = request.files['pdf']
    raw = f.read()
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(raw))
    except Exception as e:
        return jsonify({"error":"Could not read PDF", "details": str(e)}), 400

    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    if not text.strip():
        return jsonify({"error":"No extractable text found in PDF."}), 400

    # Limit first 10000 characters to avoid Hugging Face model limits
    summary = hf_summarize(text[:10000])
    return jsonify({"summary": summary})

# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
