from flask import Blueprint, jsonify
from database import get_db

progress_bp = Blueprint("progress", __name__)

@progress_bp.route("/get-progress", methods=["GET"])
def get_progress():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT score, total FROM quiz_scores")

    results = cursor.fetchall()

    conn.close()

    total_quizzes = len(results)

    if total_quizzes == 0:
        return jsonify({
            "total_quizzes":0,
            "average_score":0
        })

    total_percentage = 0

    for r in results:
        score = r[0]
        total = r[1]
        percentage = (score/total)*100
        total_percentage += percentage

    average_score = total_percentage / total_quizzes

    return jsonify({
        "total_quizzes": total_quizzes,
        "average_score": round(average_score,2)
    })