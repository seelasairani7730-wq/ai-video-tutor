from flask import Blueprint, request, jsonify
import requests
import json
from config import SARVAM_API_KEY, SARVAM_CHAT_URL
from database import get_db

quiz_bp = Blueprint("quiz", __name__)

headers = {
    "Authorization": f"Bearer {SARVAM_API_KEY}",
    "Content-Type": "application/json"
}

# ==============================
# GENERATE QUIZ
# ==============================

@quiz_bp.route("/generate-quiz", methods=["POST"])
def generate_quiz():

    data = request.json

    topic = data.get("topic")
    level = data.get("level", "Beginner")

    prompt = f"""
Generate 5 multiple choice questions about {topic}.
Difficulty level: {level}

Return ONLY valid JSON in this format:

[
 {{
  "question":"Question text",
  "options":["Option1","Option2","Option3","Option4"],
  "answer":"Correct option"
 }}
]

Do not include explanation.
Do not include text outside JSON.
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

    try:

        response = requests.post(
            SARVAM_CHAT_URL,
            json=payload,
            headers=headers
        )

        result = response.json()

        ai_text = result["choices"][0]["message"]["content"]

        print("AI RESPONSE:", ai_text)   # Debug

        # Extract JSON part safely
        start = ai_text.find("[")
        end = ai_text.rfind("]") + 1

        if start == -1 or end == -1:
            return jsonify({
                "error": "AI did not return JSON",
                "raw": ai_text
            })

        quiz_json = ai_text[start:end]

        quiz_data = json.loads(quiz_json)

        return jsonify({
            "quiz": quiz_data
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": "Quiz generation failed",
            "message": str(e)
        })

# ==============================
# SAVE QUIZ SCORE
# ==============================

@quiz_bp.route("/submit-quiz-score", methods=["POST"])
def save_score():

    data = request.json

    score = data.get("score",0)
    total = data.get("total",0)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO quiz_scores(score,total)
    VALUES(?,?)
    """,(score,total))

    conn.commit()
    conn.close()

    if total == 0:
        percentage = 0
    else:
        percentage = (score / total) * 100

    return jsonify({
        "score":score,
        "total":total,
        "percentage":percentage
    })
    
@quiz_bp.route("/get-progress", methods=["GET"])
def get_progress():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), AVG(score*100.0/total) FROM quiz_scores")

    result = cursor.fetchone()

    total_quiz = result[0] if result[0] else 0
    avg_score = result[1] if result[1] else 0

    conn.close()

    return jsonify({
        "total_quiz": total_quiz,
        "avg_score": round(avg_score,2)
    })
    