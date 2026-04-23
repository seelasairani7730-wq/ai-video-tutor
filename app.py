
from flask import Flask, render_template, send_from_directory
import os

# ==============================
# INITIALIZE FLASK
# ==============================

app = Flask(__name__)

# ==============================
# INITIALIZE DATABASE
# ==============================

from database import init_db
init_db()

# ==============================
# IMPORT BLUEPRINT ROUTES
# ==============================

from routes.ai_routes import ai_bp
from routes.quiz_routes import quiz_bp
from routes.pdf_routes import pdf_bp
from routes.reminder_routes import reminder_bp
from routes.progress_routes import progress_bp
from routes.notes_routes import notes_bp
from routes.studyplan_routes import studyplan_bp


# ==============================
# REGISTER BLUEPRINTS
# ==============================

app.register_blueprint(ai_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(pdf_bp)
app.register_blueprint(reminder_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(studyplan_bp)

# ==============================
# CREATE REQUIRED FOLDERS
# ==============================

os.makedirs("slides", exist_ok=True)
os.makedirs("audio", exist_ok=True)
os.makedirs("videos", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)

# ==============================
# PAGE ROUTES
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/chat")
def chat_page():
    return render_template("chat.html")


@app.route("/tutor")
def tutor_page():
    return render_template("tutor.html")


@app.route("/video")
def video_page():
    return render_template("video.html")


@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")


@app.route("/notes")
def notes_page():
    return render_template("notes.html")


@app.route("/studyplan")
def studyplan_page():
    return render_template("studyplan.html")


@app.route("/pdf")
def pdf_page():
    return render_template("pdf.html")

@app.route("/progress")
def progress():
    return render_template("progress.html")


# ==============================
# SERVE GENERATED VIDEOS
# ==============================

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('videos', filename)


# ==============================
# RUN FLASK SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)

