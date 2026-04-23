from flask import Blueprint, request, jsonify
import requests
import json
import os
import textwrap
from langdetect import detect
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS

from config import SARVAM_API_KEY, SARVAM_CHAT_URL

ai_bp = Blueprint("ai", __name__)

# ==============================
# AI CHAT
# ==============================

@ai_bp.route("/ai-chat", methods=["POST"])
def ai_chat():
    data = request.get_json()
    question = data.get("question")
    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model":"sarvam-m",
        "messages":[{"role":"user","content":question}]
    }
    response = requests.post(SARVAM_CHAT_URL, json=payload, headers=headers)
    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})

#==========================
#create slide - FIXED
#==========================

def get_font(text, size):
    """Pick correct font file based on text language"""
    try:
        lang = detect(text)
    except:
        lang = 'en'
    
    font_dir = os.path.join(os.getcwd(), "fonts")
    
    # Language to font mapping
    if lang == 'te':
        font_file = "NotoSansTelugu-Regular.ttf"
    elif lang == 'hi':
        font_file = "NotoSansDevanagari-Regular.ttf"  # Download if needed
    else:
        font_file = "NotoSans-Regular.ttf"  # Your 2MB file for English
    
    font_path = os.path.join(font_dir, font_file)
    
    # Fallback to 2MB file if specific font missing
    if not os.path.exists(font_path):
        font_path = os.path.join(font_dir, "NotoSans-Regular.ttf")
    
    print(f" Font: {font_file} for lang={lang}")
    return ImageFont.truetype(font_path, size)

def create_slide(title, content, index):
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), (15, 32, 39))
    draw = ImageDraw.Draw(img)

    # Use language-specific fonts
    title_font = get_font(title, 60)
    content_font = get_font(content, 40)

    def wrap_text(text, font, max_width):
        words = text.split()
        lines, current = [], ""
        for word in words:
            test_line = current + " " + word if current else word
            w = font.getlength(test_line)
            if w <= max_width:
                current = test_line
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    y = 100
    for line in wrap_text(title, title_font, width - 200):
        draw.text((100, y), line, font=title_font, fill=(255, 255, 255))
        y += 70

    y += 40
    for line in wrap_text(content, content_font, width - 200):
        draw.text((100, y), line, font=content_font, fill=(236, 240, 241))
        y += 50

    path = f"slides/slide_{index}.png"
    img.save(path)
    return path

# ==============================
# GENERATE AI VIDEO - FIXED
# ==============================

@ai_bp.route("/generate-ai-video", methods=["POST"])
def generate_ai_video():
    data = request.json
    topic = data["topic"]
    level = data["level"]

    prompt = f"""
Create 5 teaching slides about the topic: {topic}
Difficulty level: {level}

IMPORTANT:
Generate the slide titles and explanations in the SAME language as the topic provided by the user.

Return ONLY JSON in this format:
{{
 "slides":[
  {{"title":"Title","content":"Explanation"}}
 ]
}}
"""

    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sarvam-m",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(SARVAM_CHAT_URL, json=payload, headers=headers)

    try:
        ai_text = response.json()["choices"][0]["message"]["content"]
        start = ai_text.find("{")
        end = ai_text.rfind("}") + 1
        slides_json = ai_text[start:end]
        slides_data = json.loads(slides_json)
    except Exception as e:
        return jsonify({"error": "Slide generation failed", "raw": response.text, "exc": str(e)})

    slides = slides_data["slides"]
    clips = []

    for i, slide in enumerate(slides):
        title = slide["title"]
        content = slide["content"]
        image_path = create_slide(title, content, i)

        text = title + ". " + content
        audio_path = f"audio/audio_{i}.mp3"

        # FIX 1: Auto-detect language for TTS
        try:
            lang_code = detect(text)
            if lang_code not in ['hi', 'te', 'ta', 'kn', 'ml', 'bn', 'gu', 'mr']: # gTTS supported Indic
                lang_code = 'en'
        except:
            lang_code = 'en'

        print(f"[TTS DEBUG] Detected lang: {lang_code} for text: {text[:50]}")
        tts = gTTS(text=text, lang=lang_code) # FIXED: Not hardcoded to 'en'
        tts.save(audio_path)

        image_clip = ImageClip(image_path)
        audio_clip = AudioFileClip(audio_path)
        clip = image_clip.set_audio(audio_clip)
        clip = clip.set_duration(audio_clip.duration)
        clips.append(clip)

    final_video = concatenate_videoclips(clips)
    video_path = "videos/lesson.mp4"
    final_video.write_videofile(video_path, fps=24)

    return jsonify({
        "message": "Video generated successfully",
        "video_path": video_path
    })