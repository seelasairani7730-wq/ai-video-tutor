from flask import Blueprint, request, jsonify
import os
import PyPDF2
import requests
from config import SARVAM_API_KEY, SARVAM_CHAT_URL

pdf_bp = Blueprint("pdf", __name__)

UPLOAD_FOLDER = "uploads/pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

headers = {
    "Authorization": f"Bearer {SARVAM_API_KEY}",
    "Content-Type": "application/json"
}

pdf_text = ""


# Upload PDF
@pdf_bp.route("/upload-pdf", methods=["POST"])
def upload_pdf():

    global pdf_text

    file = request.files["file"]

    path = os.path.join(UPLOAD_FOLDER,file.filename)
    file.save(path)

    reader = PyPDF2.PdfReader(path)

    pdf_text=""

    for page in reader.pages:
        pdf_text += page.extract_text()

    return jsonify({
        "message":"PDF uploaded successfully",
        "filename":file.filename
    })


# Ask question from PDF
@pdf_bp.route("/ask-pdf", methods=["POST"])
def ask_pdf():

    question = request.json["question"]

    prompt = f"""
Answer the question based on this PDF.

PDF Content:
{pdf_text}

Question:
{question}
"""

    payload = {
        "model":"sarvam-m",
        "messages":[
            {"role":"user","content":prompt}
        ]
    }

    response = requests.post(SARVAM_CHAT_URL,json=payload,headers=headers)

    answer = response.json()["choices"][0]["message"]["content"]

    return jsonify({"answer":answer})