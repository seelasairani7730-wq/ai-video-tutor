from flask import Blueprint, request, jsonify
from database import get_db

reminder_bp = Blueprint("reminder", __name__)

# Set reminder
@reminder_bp.route("/set-reminder", methods=["POST"])
def set_reminder():

    data = request.json
    topic = data["topic"]
    time = data["time"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reminders(topic,time)
    VALUES(?,?)
    """,(topic,time))

    conn.commit()
    conn.close()

    return jsonify({
        "message":f"Reminder set for {topic} at {time}"
    })


# View reminders
@reminder_bp.route("/get-reminders", methods=["GET"])
def get_reminders():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reminders")

    reminders = cursor.fetchall()

    conn.close()

    result = []

    for r in reminders:
        result.append({
            "topic":r["topic"],
            "time":r["time"]
        })

    return jsonify(result)