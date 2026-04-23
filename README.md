AI-Powered Learning Platform

An AI-based educational web application that helps students learn smarter through personalized content generation, interactive quizzes, AI tutoring, and progress tracking.

📌 Features
🤖 AI Tutor

Ask any question and get instant explanations powered by AI.

🎥 AI Video Lessons

Automatically generates video lessons with slides and voice narration.

📝 Quiz Generator
Generate quizzes based on topic & level
Auto evaluation
Shows correct answers
Tracks performance
📚 Notes Generator

Generates structured notes for any topic instantly.

📅 Study Plan Generator

Creates personalized day-wise study plans.

💬 Live Doubt Solver

Ask doubts while watching videos and get instant answers.

📄 PDF Explainer

Upload PDF and ask questions from it.

📊 Progress Tracker

Tracks:

Total quizzes attempted
Average score
Learning performance
🛠️ Tech Stack

Frontend:

HTML
CSS
Bootstrap
JavaScript

Backend:

Python
Flask

Database:

SQLite

AI Integration:

Sarvam AI API

Libraries Used:

MoviePy (video creation)
gTTS (text-to-speech)
Pillow (image generation)
⚙️ Installation
git clone https://github.com/seelasairani7730-wq/ai-video-tutor.git
cd ai-learning-platform
pip install -r requirements.txt
▶️ Run the Project
python app.py

Open in browser:

http://127.0.0.1:5000
📂 Project Structure
project/
│
├── app.py
├── database.py
├── config.py
│
├── routes/
│   ├── ai_routes.py
│   ├── quiz_routes.py
│   ├── notes_routes.py
│   ├── studyplan_routes.py
│   ├── progress_routes.py
│   ├── pdf_routes.py
│   └── reminder_routes.py
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── quiz.html
│   ├── video.html
│   ├── notes.html
│   ├── studyplan.html
│   ├── pdf.html
│   └── progress.html
│
├── static/
│   ├── css/
│   ├── js/
│
├── videos/
├── slides/
├── audio/
├── pdfs/
🧠 How It Works
User inputs topic / question
Frontend sends request to Flask backend
Backend calls AI API
AI generates content (quiz, notes, video, etc.)
Response is displayed to user
Quiz scores are stored in database
Progress is calculated and shown
📊 Database Tables
quiz_scores
id
user_id
score
total
progress
id
topic
completed
reminders
id
topic
time
🚧 Challenges Faced
Handling unstructured AI responses
Parsing JSON from AI output
Matching quiz answers correctly
Video generation performance
Frontend-backend synchronization
🔮 Future Improvements
User authentication system
AI adaptive quizzes
Real-time analytics dashboard
Cloud deployment
Voice-based learning
⭐ Conclusion

This project demonstrates how AI can transform traditional learning into an interactive, personalized experience by combining multiple intelligent features into a single platform.
