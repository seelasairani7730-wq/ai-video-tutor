from flask import Blueprint, request, jsonify
import requests
import json
from config import SARVAM_API_KEY, SARVAM_CHAT_URL


studyplan_bp = Blueprint("studyplan", __name__)

headers = {
    "Authorization": f"Bearer {SARVAM_API_KEY}",
    "Content-Type": "application/json"
}

@studyplan_bp.route("/generate-studyplan", methods=["POST"])
def generate_studyplan():

    data = request.json

    topic = data.get("topic")
    days = data.get("days")

    prompt = f"""
Create a {days}-day study plan for learning {topic}.

Return the plan as clear text with each day separated.

Example:
Day 1: Introduction
Day 2: Basics
Day 3: Practice
"""

    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }

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

    study_plan = result["choices"][0]["message"]["content"]

    return jsonify({
        "study_plan": study_plan
    })