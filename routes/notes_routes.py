from flask import Blueprint, request, jsonify
import requests
from config import SARVAM_API_KEY, SARVAM_CHAT_URL

notes_bp = Blueprint("notes", __name__)

headers = {
    "Authorization": f"Bearer {SARVAM_API_KEY}",
    "Content-Type": "application/json"
}

@notes_bp.route("/generate-notes", methods=["POST"])
def generate_notes():

    data = request.json

    topic = data.get("topic")
    level = data.get("level", "Beginner")

    prompt = f"""
Create detailed study notes for the topic: {topic}
Level: {level}

Include:
1. Introduction
2. Key Concepts
3. Examples
4. Applications
5. Summary

Keep the explanation simple and clear.
"""

    payload = {
        "model": "sarvam-m",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        SARVAM_CHAT_URL,
        json=payload,
        headers=headers
    )

    result = response.json()

    notes = result["choices"][0]["message"]["content"]

    return jsonify({
        "notes": notes
    })