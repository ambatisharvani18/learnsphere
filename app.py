"""
╔══════════════════════════════════════════════════════════════╗
║              LearnSphere (GyanGuru)                         ║
║     AI-Powered Machine Learning Learning System             ║
║                                                              ║
║  A Flask web app that guides learners through a personalized ║
║  ML journey with adaptive content, quizzes, and feedback.    ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
from functools import wraps
from flask import (
    Flask, render_template, request, jsonify, session, redirect,
    url_for, send_from_directory
)
from flask_cors import CORS
from dotenv import load_dotenv

import models
from utils.genai_utils import (
    generate_roadmap, generate_reading_content, generate_audio_script,
    generate_code_content, generate_visual_content, generate_quiz,
    evaluate_answers, generate_revision, generate_flashcards,
    generate_concept_flow, answer_ml_chatbot, generate_concept_flow_for_chat,
    generate_project_suggestions
)
from utils.audio_utils import generate_audio
from utils.video_utils import search_youtube_videos
from utils.image_utils import generate_visual

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "learnsphere-secret-key-change-in-prod")
CORS(app)

# ═══════════════════════════════════════════════════════
#                    AUTH ROUTES
# ═══════════════════════════════════════════════════════

@app.route("/")
def index():
    session.clear()
    import uuid
    guest_username = "guest_" + str(uuid.uuid4())[:8]
    models.create_user(guest_username, "guest", f"{guest_username}@learnsphere.local", "Guest Learner")
    user = models.authenticate_user(guest_username, "guest")
    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["display_name"] = "Learner"
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login():
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET"])
def register():
    return redirect(url_for("dashboard"))


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    user = models.authenticate_user(username, password)
    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["display_name"] = user["display_name"]
        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "display_name": user["display_name"]
            }
        })
    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip()
    display_name = username  # Use username as display name
    
    if not username or not password or not email:
        return jsonify({"error": "All fields are required"}), 400
        
    if len(password) < 4:
        return jsonify({"error": "Password must be at least 4 characters"}), 400
        
    user_id = models.create_user(username, password, email, display_name)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["display_name"] = display_name
        return jsonify({
            "success": True,
            "user": {
                "id": user_id,
                "username": username,
                "display_name": display_name
            }
        })
    return jsonify({"error": "Username already exists"}), 409


@app.route("/api/social-login", methods=["POST"])
def api_social_login():
    data = request.get_json()
    email = data.get("email", "")
    display_name = data.get("display_name", "")
    provider = data.get("provider", "")
    if not email or not provider:
        return jsonify({"error": "Email and provider are required"}), 400
    user = models.social_login(email, display_name, provider)
    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["display_name"] = user["display_name"]
        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "display_name": user["display_name"]
            }
        })
    return jsonify({"error": "Login failed"}), 500


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ═══════════════════════════════════════════════════════
#                    PAGE ROUTES
# ═══════════════════════════════════════════════════════

def login_required(f):
    """Decorator to bypass login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            import uuid
            guest_username = "guest_" + str(uuid.uuid4())[:8]
            models.create_user(guest_username, "guest", f"{guest_username}@learnsphere.local", "Guest Learner")
            user = models.authenticate_user(guest_username, "guest")
            if user:
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["display_name"] = "Learner"
        return f(*args, **kwargs)
    return decorated


@app.route("/dashboard")
@login_required
def dashboard():
    progress = models.get_progress(session["user_id"])
    history = models.get_history(session["user_id"], limit=10)
    return render_template(
        "dashboard.html",
        user={"display_name": session.get("display_name", "Learner")},
        progress=progress,
        history=history
    )


@app.route("/learn")
@login_required
def learn():
    progress = models.get_progress(session["user_id"])
    return render_template(
        "learn.html",
        user={"display_name": session.get("display_name", "Learner")},
        progress=progress
    )


# ═══════════════════════════════════════════════════════
#                    API ROUTES
# ═══════════════════════════════════════════════════════

@app.route("/api/progress", methods=["GET"])
@login_required
def api_get_progress():
    progress = models.get_progress(session["user_id"])
    return jsonify(progress or {})


@app.route("/api/progress", methods=["POST"])
@login_required
def api_save_progress():
    data = request.get_json()
    models.save_progress(session["user_id"], **data)
    return jsonify({"success": True})


@app.route("/api/history", methods=["GET"])
@login_required
def api_get_history():
    history = models.get_history(session["user_id"])
    return jsonify(history)


@app.route("/api/roadmap", methods=["POST"])
@login_required
def api_generate_roadmap():
    data = request.get_json()
    level = data.get("level", "Beginner")
    roadmap = generate_roadmap(level)
    # Save to progress
    models.save_progress(
        session["user_id"],
        level=level,
        current_roadmap=roadmap
    )
    return jsonify({"roadmap": roadmap})


@app.route("/api/content", methods=["POST"])
@login_required
def api_generate_content():
    data = request.get_json()
    topic = data.get("topic", "")
    level = data.get("level", "Beginner")
    style = data.get("style", "Reading")

    models.save_progress(
        session["user_id"],
        current_topic=topic,
        learning_style=style
    )

    if style == "Reading":
        content = generate_reading_content(topic, level)
        return jsonify({"content": content, "type": "text"})

    elif style == "Auditory":
        script = generate_audio_script(topic, level)
        audio_path = generate_audio(script, topic)
        return jsonify({
            "content": script,
            "audio_path": "/" + audio_path.replace("\\", "/"),
            "type": "audio"
        })

    elif style == "Kinesthetic":
        content = generate_code_content(topic, level)
        return jsonify({"content": content, "type": "text"})

    elif style == "Visual":
        diagrams = generate_visual_content(topic, level)
        videos = search_youtube_videos(topic, max_results=3)
        return jsonify({
            "content": diagrams,
            "videos": videos,
            "type": "visual"
        })

    return jsonify({"content": "Style not supported", "type": "text"})


@app.route("/api/quiz", methods=["POST"])
@login_required
def api_generate_quiz():
    data = request.get_json()
    topic = data.get("topic", "")
    level = data.get("level", "Beginner")
    quiz = generate_quiz(topic, level)
    return jsonify({"quiz": quiz})


@app.route("/api/evaluate", methods=["POST"])
@login_required
def api_evaluate():
    data = request.get_json()
    topic = data.get("topic", "")
    level = data.get("level", "Beginner")
    quiz_data = data.get("quiz_data", [])
    answers = data.get("answers", [])
    feedback = evaluate_answers(topic, level, quiz_data, answers)

    # Save history and award XP
    score = feedback.get("score", 0)
    total = feedback.get("total", 3)
    pct = feedback.get("percentage", 0)
    models.add_history(
        session["user_id"],
        topic,
        quiz_score=score,
        quiz_total=total
    )

    xp_earned = int(pct * 0.5) + 10
    new_xp = models.add_xp(session["user_id"], xp_earned)

    # Update topics completed
    progress = models.get_progress(session["user_id"])
    completed = progress.get("topics_completed", [])
    if topic not in completed:
        completed.append(topic)
        models.save_progress(session["user_id"], topics_completed=completed)

    feedback["xp_earned"] = xp_earned
    feedback["total_xp"] = new_xp
    return jsonify(feedback)


@app.route("/api/revision", methods=["POST"])
@login_required
def api_revision():
    data = request.get_json()
    topic = data.get("topic", "")
    level = data.get("level", "Beginner")
    weak_areas = data.get("weak_areas", [])
    revision = generate_revision(topic, level, weak_areas)
    return jsonify({"content": revision})


@app.route("/api/flashcards", methods=["POST"])
@login_required
def api_flashcards():
    data = request.get_json()
    topic = data.get("topic", "")
    level = data.get("level", "Beginner")
    cards = generate_flashcards(topic, level)
    models.add_xp(session["user_id"], 15)
    return jsonify({"cards": cards})


@app.route("/api/concept-flow", methods=["POST"])
@login_required
def api_concept_flow():
    data = request.get_json()
    topic = data.get("topic", "")
    level = data.get("level", "Beginner")
    content = generate_concept_flow(topic, level)
    return jsonify({"content": content})


@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    data = request.get_json()
    question = data.get("question", "")
    level = data.get("level")
    context_topic = data.get("context_topic")
    chat_history = data.get("chat_history", [])
    mode = data.get("mode", "text")

    if mode == "text":
        result = answer_ml_chatbot(
            question,
            level=level,
            context_topic=context_topic,
            chat_history=chat_history
        )
        return jsonify({
            "text": result["text"],
            "suggestions": result.get("suggestions", [])
        })

    elif mode == "flow":
        lvl = level or "Beginner"
        topic_name, flow_content = generate_concept_flow_for_chat(question, lvl)
        return jsonify({
            "text": f"🔀 **Concept Flow: {topic_name}**\n\n{flow_content}",
            "suggestions": []
        })

    elif mode == "image":
        result = answer_ml_chatbot(
            question,
            level=level,
            context_topic=context_topic
        )
        img_path, img_desc = generate_visual(question)
        path = "/" + img_path.replace("\\", "/") if img_path else None
        return jsonify({
            "text": result["text"],
            "suggestions": result.get("suggestions", []),
            "media": {
                "type": "image",
                "path": path,
                "desc": img_desc
            }
        })

    elif mode == "audio":
        result = answer_ml_chatbot(
            question,
            level=level,
            context_topic=context_topic
        )
        script = generate_audio_script(question, level or "Beginner")
        audio_path = generate_audio(script, question)
        return jsonify({
            "text": result["text"],
            "suggestions": result.get("suggestions", []),
            "media": {
                "type": "audio",
                "path": "/" + audio_path.replace("\\", "/")
            }
        })

    elif mode == "video":
        result = answer_ml_chatbot(
            question,
            level=level,
            context_topic=context_topic
        )
        videos = search_youtube_videos(question, max_results=3)
        return jsonify({
            "text": result["text"],
            "suggestions": result.get("suggestions", []),
            "media": {
                "type": "video",
                "videos": videos
            }
        })

    return jsonify({"text": "Mode not supported", "suggestions": []})


@app.route("/api/projects", methods=["POST"])
@login_required
def api_projects():
    data = request.get_json()
    topics = data.get("topics", [])
    level = data.get("level", "Beginner")
    projects = generate_project_suggestions(topics, level)
    return jsonify({"content": projects})


# Serve generated audio files
@app.route("/generated_audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory("generated_audio", filename)


# Serve generated images
@app.route("/generated_images/<path:filename>")
def serve_images(filename):
    return send_from_directory("generated_images", filename)


if __name__ == "__main__":
    print("🧠 LearnSphere is starting...")
    print("   Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
