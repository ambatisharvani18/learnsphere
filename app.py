"""
╔══════════════════════════════════════════════════════════════╗
║              LearnSphere (GyanGuru)                         ║
║     AI-Powered Machine Learning Learning System             ║
║                                                              ║
║  A Streamlit app that guides learners through a personalized ║
║  ML journey with adaptive content, quizzes, and feedback.    ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import os
import json
import time

# ─────────────────── PAGE CONFIG ───────────────────────
st.set_page_config(
    page_title="LearnSphere — AI ML Tutor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────── CUSTOM CSS ───────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap');

    /* ═══════ GLOBAL ═══════ */
    .stApp {
        background: #fffaf5;
        font-family: 'Nunito', sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ═══════ HERO SECTION ═══════ */
    .hero-container {
        text-align: center;
        padding: 50px 20px;
        animation: bounceIn 0.8s ease-out;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #87CEEB, #93C572);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
        animation: wiggle 2s ease-in-out infinite;
    }
    .hero-title {
        font-size: 3.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #2d1b69, #87CEEB, #93C572);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #636e72;
        max-width: 550px;
        margin: 0 auto 36px;
        line-height: 1.7;
    }
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 24px;
        flex-wrap: wrap;
        margin-top: 40px;
    }
    .hero-feature {
        background: white;
        border: 2px solid #E0F7FA;
        border-radius: 20px;
        padding: 24px 20px;
        width: 180px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(135,206,235,0.08);
    }
    .hero-feature:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 15px 35px rgba(135,206,235,0.15);
        border-color: #87CEEB;
    }
    .hero-feature-icon {
        font-size: 2.2rem;
        margin-bottom: 10px;
        animation: float 3s ease-in-out infinite;
    }
    .hero-feature-title {
        font-weight: 800;
        color: #2d3436;
        font-size: 0.9rem;
        margin-bottom: 4px;
    }
    .hero-feature-desc {
        font-size: 0.75rem;
        color: #b2bec3;
    }

    /* ═══════ CARDS ═══════ */
    .glass-card {
        background: white;
        border: 2px solid #E0F7FA;
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover {
        box-shadow: 0 12px 30px rgba(135,206,235,0.1);
        transform: translateY(-3px);
    }

    /* ═══════ LEVEL SELECTOR ═══════ */
    .level-container {
        text-align: center;
        padding: 30px 20px;
    }
    .level-title {
        font-size: 2rem;
        font-weight: 900;
        color: #2d3436;
        margin-bottom: 8px;
    }
    .level-subtitle {
        font-size: 1rem;
        color: #636e72;
        margin-bottom: 40px;
    }
    .level-card {
        background: white;
        border: 3px solid #dfe6e9;
        border-radius: 24px;
        padding: 36px 24px;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .level-card:hover {
        border-color: #87CEEB;
        transform: translateY(-8px) rotate(-1deg);
        box-shadow: 0 20px 40px rgba(135,206,235,0.12);
    }
    .level-icon {
        font-size: 3.5rem;
        margin-bottom: 14px;
        display: block;
        animation: float 3s ease-in-out infinite;
    }
    .level-name {
        font-size: 1.3rem;
        font-weight: 800;
        color: #2d3436;
        margin-bottom: 8px;
    }
    .level-desc {
        font-size: 0.85rem;
        color: #b2bec3;
        line-height: 1.5;
    }

    /* ═══════ ROADMAP ═══════ */
    .roadmap-header {
        text-align: center;
        margin-bottom: 36px;
    }
    .roadmap-title {
        font-size: 2rem;
        font-weight: 900;
        color: #2d3436;
    }
    .roadmap-badge {
        display: inline-block;
        background: linear-gradient(135deg, #87CEEB, #93C572);
        color: white;
        padding: 5px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .topic-card {
        background: white;
        border: 2px solid #E0F7FA;
        border-radius: 18px;
        padding: 18px 22px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 14px;
        cursor: pointer;
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .topic-card:hover {
        border-color: #87CEEB;
        box-shadow: 0 8px 20px rgba(135,206,235,0.1);
        transform: translateX(6px);
    }
    .topic-num {
        background: linear-gradient(135deg, #87CEEB, #93C572);
        color: white;
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .topic-content { flex: 1; }
    .topic-name {
        font-weight: 800;
        color: #2d3436;
        font-size: 1rem;
        margin-bottom: 2px;
    }
    .topic-desc {
        font-size: 0.78rem;
        color: #b2bec3;
    }
    .topic-icon {
        font-size: 1.5rem;
    }

    /* ═══════ LEARNING STYLE ═══════ */
    .style-card {
        background: white;
        border: 3px solid #dfe6e9;
        border-radius: 24px;
        padding: 28px 18px;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .style-card:hover {
        border-color: #87CEEB;
        transform: translateY(-6px) rotate(1deg);
        box-shadow: 0 15px 30px rgba(135,206,235,0.12);
    }
    .style-icon { font-size: 2.8rem; margin-bottom: 10px; }
    .style-name {
        font-weight: 800;
        color: #2d3436;
        font-size: 1rem;
        margin-bottom: 6px;
    }
    .style-desc {
        font-size: 0.78rem;
        color: #b2bec3;
        line-height: 1.4;
    }

    /* ═══════ PROGRESS BAR ═══════ */
    .progress-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        margin: 16px 0 28px;
        padding: 0 20px;
    }
    .progress-step {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .progress-dot {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 800;
        transition: all 0.4s ease;
    }
    .progress-dot.active {
        background: linear-gradient(135deg, #87CEEB, #93C572);
        color: white;
        box-shadow: 0 5px 15px rgba(135,206,235,0.3);
        animation: pulse 2s infinite;
    }
    .progress-dot.completed {
        background: #00b894;
        color: white;
    }
    .progress-dot.pending {
        background: #E0F7FA;
        color: #b2bec3;
        border: 2px solid #E0F7FA;
    }
    .progress-line {
        width: 36px;
        height: 3px;
        border-radius: 2px;
    }
    .progress-line.completed { background: #00b894; }
    .progress-line.pending { background: #E0F7FA; }

    /* ═══════ CONTENT DISPLAY ═══════ */
    .content-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 24px;
    }
    .content-header-icon {
        background: linear-gradient(135deg, #87CEEB, #93C572);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    .content-header-text h2 {
        margin: 0;
        color: #2d3436;
        font-size: 1.4rem;
        font-weight: 800;
    }
    .content-header-text p {
        margin: 0;
        color: #b2bec3;
        font-size: 0.85rem;
    }

    /* ═══════ QUIZ ═══════ */
    .quiz-question {
        background: white;
        border: 2px solid #E0F7FA;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .quiz-type-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    .badge-scenario { background: #E0F7FA; color: #87CEEB; }
    .badge-code { background: #dfe6e9; color: #6c5ce7; }
    .badge-mcq { background: #55efc4; color: #00b894; }

    /* ═══════ FEEDBACK ═══════ */
    .score-display {
        text-align: center;
        padding: 36px;
        animation: bounceIn 0.6s ease-out;
    }
    .score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        font-size: 2.5rem;
        font-weight: 900;
        color: white;
        animation: pulse 2s infinite;
    }
    .score-high {
        background: linear-gradient(135deg, #00b894, #55efc4);
        box-shadow: 0 8px 25px rgba(0,184,148,0.3);
    }
    .score-mid {
        background: linear-gradient(135deg, #fdcb6e, #ffeaa7);
        box-shadow: 0 8px 25px rgba(253,203,110,0.3);
    }
    .score-low {
        background: linear-gradient(135deg, #ff7675, #fab1a0);
        box-shadow: 0 8px 25px rgba(255,118,117,0.3);
    }

    /* ═══════ BUTTONS ═══════ */
    .stButton > button {
        background: linear-gradient(135deg, #87CEEB, #93C572) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 10px 28px !important;
        font-weight: 700 !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px rgba(135,206,235,0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(135,206,235,0.35) !important;
    }
    .stButton > button:active {
        transform: scale(0.97) !important;
    }

    /* ═══════ ANIMATIONS ═══════ */
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.9) translateY(20px); }
        60% { transform: scale(1.02) translateY(-3px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes wiggle {
        0%, 100% { transform: rotate(-2deg); }
        50% { transform: rotate(2deg); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    .animate-fade-in {
        animation: fadeIn 0.6s ease-out;
    }

    /* ═══════ SIDEBAR STYLES ═══════ */
    section[data-testid="stSidebar"] {
        background: #fff5f5 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        font-family: 'Nunito', sans-serif;
    }

    /* ═══════ MARKDOWN CONTENT ═══════ */
    .stMarkdown {
        font-family: 'Nunito', sans-serif;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2d3436;
        font-weight: 800;
    }
    .stMarkdown code {
        font-family: 'Fira Code', monospace;
    }

    /* ═══════ RADIO + SELECTBOX ═══════ */
    .stRadio > div { gap: 8px !important; }
    .stRadio label span { font-family: 'Nunito', sans-serif !important; }

    /* ═══════ GYANGURU SIDE PANEL ═══════ */
    .gg-side-panel {
        border-left: 2.5px solid rgba(108,52,131,0.15);
        padding-left: 8px;
        animation: gg-panel-slide 0.35s cubic-bezier(0.175,0.885,0.32,1.275);
    }
    @keyframes gg-panel-slide {
        from { opacity: 0; transform: translateX(30px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    .gg-panel-header {
        background: linear-gradient(135deg, #6C3483, #2980B9);
        padding: 14px 16px;
        border-radius: 14px 14px 0 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .gg-panel-header .title { color: white; font-weight: 800; font-size: 1.05rem; }
    .gg-panel-header .subtitle { color: rgba(255,255,255,0.7); font-size: 0.7rem; }
    .gg-panel-header .level-badge {
        background: rgba(255,255,255,0.2);
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.7rem;
        color: white;
        font-weight: 700;
    }

    /* ═══════ GAMIFICATION ═══════ */
    .xp-bar-container {
        background: #E0F7FA;
        border-radius: 50px;
        padding: 3px;
        margin: 8px 0;
    }
    .xp-bar {
        background: linear-gradient(90deg, #87CEEB, #93C572, #A0D6B4);
        height: 10px;
        border-radius: 50px;
        transition: width 0.8s ease;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: #E0F7FA;
        border: 2px solid #93C572;
        border-radius: 50px;
        padding: 4px 12px;
        font-size: 0.7rem;
        font-weight: 700;
        color: #e17055;
        margin: 3px;
        animation: float 4s ease-in-out infinite;
    }
    .stat-card {
        background: white;
        border: 2px solid #E0F7FA;
        border-radius: 16px;
        padding: 14px;
        text-align: center;
        margin-bottom: 8px;
    }
    .stat-number {
        font-size: 1.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #87CEEB, #93C572);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 0.65rem;
        color: #b2bec3;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    /* ═══════ FLASHCARDS ═══════ */
    .flashcard {
        perspective: 1000px;
        height: 200px;
        margin-bottom: 16px;
        cursor: pointer;
    }
    .flashcard-inner {
        position: relative;
        width: 100%;
        height: 100%;
        transition: transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
    }
    .flashcard.flipped .flashcard-inner {
        transform: rotateY(180deg);
    }
    .flashcard-front, .flashcard-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        text-align: center;
    }
    .flashcard-front {
        background: linear-gradient(135deg, #87CEEB, #93C572);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 8px 25px rgba(135,206,235,0.2);
    }
    .flashcard-back {
        background: white;
        border: 3px solid #87CEEB;
        color: #2d3436;
        transform: rotateY(180deg);
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* ═══════ CONFETTI ═══════ */
    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    .confetti-piece {
        position: fixed;
        width: 10px;
        height: 10px;
        top: -10px;
        z-index: 10000;
        animation: confetti-fall 3s ease-in forwards;
    }

    /* ═══════ MOTIVATIONAL TOAST ═══════ */
    .stToast {
        font-family: 'Nunito', sans-serif !important;
        font-weight: 700 !important;
    }



    /* ═══════ MINI PROJECTS ═══════ */
    .mini-project-card {
        background: white;
        border: 2px solid #E0F7FA;
        border-radius: 20px;
        padding: 22px 18px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        position: relative;
        overflow: hidden;
    }
    .mini-project-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #87CEEB, #93C572, #6C3483);
    }
    .mini-project-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 12px 30px rgba(135,206,235,0.15);
        border-color: #87CEEB;
    }
    .mini-project-icon { font-size: 2.2rem; margin-bottom: 10px; }
    .mini-project-title {
        font-weight: 800;
        color: #2d3436;
        font-size: 0.95rem;
        margin-bottom: 6px;
    }
    .mini-project-desc {
        font-size: 0.78rem;
        color: #636e72;
        line-height: 1.5;
        margin-bottom: 10px;
    }
    .mini-project-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(135,206,235,0.15), rgba(147,197,114,0.15));
        border: 1px solid rgba(135,206,235,0.3);
        border-radius: 50px;
        padding: 3px 10px;
        font-size: 0.65rem;
        font-weight: 700;
        color: #6C3483;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Concept Flow Visualization */
    .cf-header {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .cf-header::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 30% 50%, rgba(108,52,131,0.4) 0%, transparent 60%),
                    radial-gradient(ellipse at 70% 50%, rgba(41,128,185,0.4) 0%, transparent 60%);
    }
    .cf-title {
        font-size: 2rem;
        font-weight: 900;
        color: white;
        position: relative;
        margin-bottom: 8px;
    }
    .cf-subtitle {
        color: rgba(255,255,255,0.75);
        font-size: 0.95rem;
        position: relative;
    }
    .cf-content {
        background: white;
        border-radius: 16px;
        padding: 28px;
        border: 2px solid rgba(108,52,131,0.1);
        box-shadow: 0 4px 20px rgba(108,52,131,0.06);
        font-family: 'Fira Code', monospace;
        font-size: 0.88rem;
        line-height: 1.7;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────── SESSION STATE ───────────────────────
def init_session_state():
    defaults = {
        "page": "welcome",
        "level": None,
        "roadmap": None,
        "selected_topic": None,
        "selected_topic_title": None,
        "learning_style": None,
        "content": None,
        "quiz_data": None,
        "user_answers": {},
        "feedback": None,
        "revision": None,
        "projects": None,
        "topics_completed": [],
        "loading": False,
        # legacy
        "chat_messages": [],
        "show_doubt_chat": False,
        "xp": 0,
        "badges": [],
        "flashcards": None,
        "flipped_cards": set(),
        # GyanGuru chatbot
        "gg_open": False,
        "gg_messages": [],          # persistent session history
        "gg_level": None,           # user's selected level inside chatbot
        "gg_mode": "text",          # text | image | audio | video | flow
        "gg_thinking": False,
        # Concept Flow
        "cf_topic": None,
        "cf_content": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def navigate(page):
    st.session_state.page = page


def award_xp(points, reason=""):
    """Award XP points and check for new badges."""
    st.session_state.xp += points
    check_badges()


def check_badges():
    """Check and award badges based on progress."""
    badges = st.session_state.badges
    xp = st.session_state.xp
    topics = len(st.session_state.topics_completed)

    badge_defs = [
        ("🌟 First Steps", topics >= 1),
        ("📚 Bookworm", topics >= 3),
        ("🏆 Scholar", topics >= 5),
        ("💎 Expert", topics >= 8),
        ("⚡ Quick Learner", xp >= 100),
        ("🔥 On Fire", xp >= 300),
        ("👑 ML Master", xp >= 500),
    ]
    for name, condition in badge_defs:
        if condition and name not in badges:
            badges.append(name)


def get_user_level():
    """Get the gamification level based on XP."""
    xp = st.session_state.xp
    if xp >= 500: return "🏆 Master", 500, 500
    elif xp >= 300: return "💎 Expert", 300, 500
    elif xp >= 150: return "🌟 Pro", 150, 300
    elif xp >= 50: return "📘 Learner", 50, 150
    else: return "🌱 Newbie", 0, 50


def show_confetti():
    """Show confetti celebration animation."""
    import random
    colors = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#ef4444', '#3b82f6']
    confetti_html = ""
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.random() * 2
        color = random.choice(colors)
        size = random.randint(6, 12)
        confetti_html += f'<div class="confetti-piece" style="left:{left}%;background:{color};width:{size}px;height:{size}px;animation-delay:{delay}s;border-radius:{random.choice(["50%","0"])};"></div>'
    st.markdown(confetti_html, unsafe_allow_html=True)


# ─────────────────── PROGRESS BAR ───────────────────────
def render_progress():
    steps = [
        ("1", "Level"),
        ("2", "Roadmap"),
        ("3", "Style"),
        ("4", "Learn"),
        ("5", "Quiz"),
        ("6", "Review"),
    ]
    page_order = ["level_select", "roadmap", "style_select", "content", "quiz", "feedback"]
    current_idx = page_order.index(st.session_state.page) if st.session_state.page in page_order else -1

    html = '<div class="progress-container">'
    for i, (num, label) in enumerate(steps):
        if i < current_idx:
            dot_class = "completed"
        elif i == current_idx:
            dot_class = "active"
        else:
            dot_class = "pending"

        html += f"""
        <div style="text-align:center;">
            <div class="progress-dot {dot_class}">{'✓' if i < current_idx else num}</div>
            <div class="progress-label">{label}</div>
        </div>
        """
        if i < len(steps) - 1:
            line_class = "completed" if i < current_idx else "pending"
            html += f'<div class="progress-line {line_class}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#                      PAGES
# ═══════════════════════════════════════════════════════

# ─────────────────── WELCOME ───────────────────────
def page_welcome():
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">✨ AI-POWERED LEARNING</div>
        <div class="hero-title">LearnSphere</div>
        <div class="hero-subtitle">
            Your personal AI tutor for Machine Learning.
            Learn at your own pace with adaptive content, hands-on code,
            audio lessons, visual diagrams, and smart assessments.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀  Get Started", use_container_width=True):
            navigate("level_select")
            st.rerun()

    st.markdown("""
    <div class="hero-features">
        <div class="hero-feature">
            <div class="hero-feature-icon">📖</div>
            <div class="hero-feature-title">Reading</div>
            <div class="hero-feature-desc">In-depth articles & explanations</div>
        </div>
        <div class="hero-feature">
            <div class="hero-feature-icon">🎧</div>
            <div class="hero-feature-title">Auditory</div>
            <div class="hero-feature-desc">Podcast-style audio lessons</div>
        </div>
        <div class="hero-feature">
            <div class="hero-feature-icon">💻</div>
            <div class="hero-feature-title">Kinesthetic</div>
            <div class="hero-feature-desc">Hands-on code & problems</div>
        </div>
        <div class="hero-feature">
            <div class="hero-feature-icon">🎨</div>
            <div class="hero-feature-title">Visual</div>
            <div class="hero-feature-desc">AI-generated diagrams & visuals</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────── LEVEL SELECT ───────────────────────
def page_level_select():
    render_progress()

    st.markdown("""
    <div class="level-container">
        <div class="level-title">What's your ML experience?</div>
        <div class="level-subtitle">We'll customize your learning roadmap based on your level</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    levels = [
        ("🌱", "Beginner", "New to ML. I want to start from the very basics.", col1),
        ("🌿", "Intermediate", "I know the fundamentals and want to go deeper.", col2),
        ("🌳", "Advanced", "I'm experienced and want to master cutting-edge topics.", col3),
    ]

    for icon, name, desc, col in levels:
        with col:
            st.markdown(f"""
            <div class="level-card">
                <div class="level-icon">{icon}</div>
                <div class="level-name">{name}</div>
                <div class="level-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {name}", key=f"level_{name}", use_container_width=True):
                st.session_state.level = name
                navigate("roadmap")
                st.rerun()

    st.divider()
    if st.button("← Back to Welcome"):
        navigate("welcome")
        st.rerun()


# ─────────────────── ROADMAP ───────────────────────
def page_roadmap():
    render_progress()

    # Generate roadmap if not cached
    if st.session_state.roadmap is None:
        with st.spinner("🗺️ Generating your personalized ML roadmap..."):
            from utils.genai_utils import generate_roadmap
            st.session_state.roadmap = generate_roadmap(st.session_state.level)

    level = st.session_state.level
    roadmap = st.session_state.roadmap

    st.markdown(f"""
    <div class="roadmap-header">
        <div class="roadmap-badge">📍 {level.upper()} TRACK</div>
        <div class="roadmap-title">Your ML Learning Roadmap</div>
    </div>
    """, unsafe_allow_html=True)

    # Show completed topics
    if st.session_state.topics_completed:
        st.success(f"✅ Completed: {', '.join(st.session_state.topics_completed)}")

    # Display topics
    for topic in roadmap:
        tid = topic.get("id", 0)
        title = topic.get("title", "Topic")
        desc = topic.get("description", "")
        icon = topic.get("icon", "📘")
        is_done = title in st.session_state.topics_completed

        col1, col2 = st.columns([6, 1])
        with col1:
            status_emoji = "✅" if is_done else icon
            st.markdown(f"""
            <div class="topic-card">
                <div class="topic-num">{tid}</div>
                <div class="topic-content">
                    <div class="topic-name">{status_emoji} {title}</div>
                    <div class="topic-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            btn_label = "Review" if is_done else "Start"
            if st.button(btn_label, key=f"topic_{tid}", use_container_width=True):
                st.session_state.selected_topic = tid
                st.session_state.selected_topic_title = title
                navigate("style_select")
                st.rerun()

    st.divider()

    col_back, col_proj = st.columns([1, 1])
    with col_back:
        if st.button("← Change Level"):
            st.session_state.roadmap = None
            navigate("level_select")
            st.rerun()
    with col_proj:
        # Project suggestions button (visible after completing at least 3 topics)
        if len(st.session_state.topics_completed) >= 3:
            if st.button("🚀  Get Project Suggestions", use_container_width=True):
                navigate("projects")
                st.rerun()

    # ─────────────────── MINI PROJECTS SECTION ───────────────────────
    st.markdown("""<br>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="roadmap-header">
        <div class="roadmap-badge">🛠️ HANDS-ON PRACTICE</div>
        <div class="roadmap-title">Mini Projects</div>
        <div style="color:#636e72;font-size:0.9rem;margin-top:4px;">Apply what you learn with these bite-sized projects</div>
    </div>
    """, unsafe_allow_html=True)

    mini_projects = {
        "Beginner": [
            {
                "icon": "📊", "title": "Data Explorer",
                "desc": "Load a CSV dataset, compute basic statistics, and visualize distributions.",
                "tags": "Pandas · Matplotlib",
                "explanation": "This project teaches you the foundation of any ML workflow — understanding your data. You'll load real-world datasets, compute summary statistics (mean, median, mode, standard deviation), handle missing values, and create visualizations like histograms, box plots, and scatter matrices to uncover patterns before building any model.",
                "tools": ["Python 3.8+", "Pandas", "Matplotlib", "Seaborn", "Jupyter Notebook"],
                "concepts": ["Data loading & cleaning", "Descriptive statistics", "Data visualization", "Handling missing values", "Exploratory Data Analysis (EDA)"],
            },
            {
                "icon": "🏠", "title": "House Price Predictor",
                "desc": "Build a linear regression model to predict house prices from features.",
                "tags": "Scikit-learn · NumPy",
                "explanation": "Your first predictive model! You'll use the classic Boston/Ames Housing dataset to understand how features like square footage, number of rooms, and location affect price. You'll learn to split data into train/test sets, fit a linear regression, evaluate it with R² and RMSE, and visualize predicted vs actual values.",
                "tools": ["Python 3.8+", "Scikit-learn", "NumPy", "Pandas", "Matplotlib"],
                "concepts": ["Linear Regression", "Train-Test Split", "Feature selection", "Mean Squared Error (MSE)", "R² Score", "Model evaluation"],
            },
            {
                "icon": "🌸", "title": "Iris Classifier",
                "desc": "Train a KNN classifier on the Iris dataset with decision boundary visualization.",
                "tags": "KNN · Seaborn",
                "explanation": "A classic ML project! You'll classify iris flowers into 3 species based on petal and sepal measurements. You'll experiment with different K values, understand how the distance metric affects predictions, and create beautiful 2D decision boundary plots to see exactly how your classifier divides the feature space.",
                "tools": ["Python 3.8+", "Scikit-learn", "Seaborn", "Matplotlib", "NumPy"],
                "concepts": ["K-Nearest Neighbors (KNN)", "Classification", "Decision boundaries", "Cross-validation", "Hyperparameter tuning (K value)", "Confusion matrix"],
            },
            {
                "icon": "📧", "title": "Spam Detector",
                "desc": "Create a Naive Bayes text classifier to detect spam emails.",
                "tags": "NLP · Naive Bayes",
                "explanation": "Enter the world of Natural Language Processing! You'll preprocess email text (tokenization, removing stop words, TF-IDF vectorization), train a Naive Bayes classifier, and build a working spam filter. You'll learn how probabilistic models handle text data and evaluate your model with precision, recall, and F1-score.",
                "tools": ["Python 3.8+", "Scikit-learn", "NLTK or spaCy", "Pandas", "Matplotlib"],
                "concepts": ["Text preprocessing", "TF-IDF Vectorization", "Naive Bayes Theorem", "Precision & Recall", "F1-Score", "Bag of Words"],
            },
        ],
        "Intermediate": [
            {
                "icon": "🖼️", "title": "Image Classifier",
                "desc": "Build a CNN to classify CIFAR-10 images with augmentation and dropout.",
                "tags": "TensorFlow · CNN",
                "explanation": "Dive into deep learning by building a Convolutional Neural Network from scratch! You'll work with the CIFAR-10 dataset (60,000 images across 10 classes), implement convolutional and pooling layers, apply data augmentation (rotation, flipping, zoom) to prevent overfitting, and use dropout regularization to build a robust classifier.",
                "tools": ["Python 3.8+", "TensorFlow / Keras", "NumPy", "Matplotlib", "GPU (recommended)"],
                "concepts": ["Convolutional Neural Networks (CNN)", "Convolution & Pooling layers", "Data Augmentation", "Dropout Regularization", "Batch Normalization", "Learning rate scheduling"],
            },
            {
                "icon": "💬", "title": "Sentiment Analyzer",
                "desc": "Fine-tune a pre-trained model for movie review sentiment classification.",
                "tags": "Transformers · NLP",
                "explanation": "Learn transfer learning for NLP! You'll take a pre-trained transformer model (like BERT or DistilBERT), fine-tune it on the IMDB movie reviews dataset, and build a sentiment classifier that understands context, sarcasm, and nuance far better than traditional approaches. You'll learn tokenization, attention mechanisms, and evaluation.",
                "tools": ["Python 3.8+", "Hugging Face Transformers", "PyTorch or TensorFlow", "Datasets library", "GPU (recommended)"],
                "concepts": ["Transfer Learning", "Transformer Architecture", "Attention Mechanism", "Fine-tuning", "Tokenization (WordPiece/BPE)", "Pre-trained Language Models"],
            },
            {
                "icon": "📈", "title": "Stock Price Forecaster",
                "desc": "Use an LSTM network to predict stock prices from time-series data.",
                "tags": "LSTM · Keras",
                "explanation": "Apply deep learning to finance! You'll fetch real stock price data, create sliding window sequences, normalize features, and train an LSTM (Long Short-Term Memory) network that captures temporal patterns. You'll learn about vanishing gradients, why LSTMs solve them, and how to evaluate time-series predictions properly.",
                "tools": ["Python 3.8+", "Keras / TensorFlow", "yfinance", "Pandas", "Matplotlib", "Scikit-learn"],
                "concepts": ["Recurrent Neural Networks (RNN)", "LSTM cells & gates", "Time-series forecasting", "Sequence-to-sequence learning", "Feature normalization", "Sliding window approach"],
            },
            {
                "icon": "🎵", "title": "Music Genre Classifier",
                "desc": "Extract audio features and train an SVM to classify songs by genre.",
                "tags": "Librosa · SVM",
                "explanation": "Combine signal processing with ML! You'll load audio files, extract features like MFCCs (Mel-frequency cepstral coefficients), spectral centroid, and chroma features using Librosa. Then train a Support Vector Machine with different kernels (linear, RBF) to classify songs into genres like rock, jazz, classical, and hip-hop.",
                "tools": ["Python 3.8+", "Librosa", "Scikit-learn", "NumPy", "Matplotlib", "SoundFile"],
                "concepts": ["Audio signal processing", "MFCCs & spectral features", "Support Vector Machines (SVM)", "Kernel trick (RBF, linear)", "Feature extraction", "Multi-class classification"],
            },
        ],
        "Advanced": [
            {
                "icon": "🤖", "title": "Chatbot with RAG",
                "desc": "Build a retrieval-augmented generation chatbot for your own documents.",
                "tags": "LangChain · FAISS",
                "explanation": "Build a production-grade AI chatbot! You'll chunk and embed documents using sentence transformers, store embeddings in a FAISS vector database, and implement retrieval-augmented generation where the LLM answers questions grounded in your actual documents — reducing hallucinations. You'll learn embedding models, similarity search, prompt engineering, and chain orchestration.",
                "tools": ["Python 3.8+", "LangChain", "FAISS", "OpenAI / Gemini API", "Sentence-Transformers", "Streamlit (for UI)"],
                "concepts": ["Retrieval-Augmented Generation (RAG)", "Vector embeddings", "Similarity search (cosine/L2)", "Prompt engineering", "Document chunking strategies", "LLM orchestration"],
            },
            {
                "icon": "🎨", "title": "Style Transfer App",
                "desc": "Apply artistic styles to photos using neural style transfer with VGG.",
                "tags": "PyTorch · VGG19",
                "explanation": "Create art with AI! You'll implement Gatys et al.'s neural style transfer algorithm — extracting content features from one image and style features (Gram matrices) from another, then optimizing a generated image to match both. You'll understand how different CNN layers capture different levels of abstraction, from edges to textures to objects.",
                "tools": ["Python 3.8+", "PyTorch", "torchvision (VGG19)", "PIL/Pillow", "Matplotlib", "GPU (required)"],
                "concepts": ["Neural Style Transfer", "Content & Style loss functions", "Gram matrices", "Feature extraction from CNN layers", "Optimization-based image generation", "VGG architecture"],
            },
            {
                "icon": "🔍", "title": "Object Detection API",
                "desc": "Train YOLOv8 on custom data and deploy as a real-time REST API.",
                "tags": "YOLO · FastAPI",
                "explanation": "End-to-end MLOps! You'll annotate a custom dataset, train a YOLOv8 model for real-time object detection, evaluate it with mAP (mean Average Precision), and deploy it as a REST API using FastAPI. You'll handle image uploads, run inference, return bounding box predictions as JSON, and learn about model serving best practices.",
                "tools": ["Python 3.8+", "Ultralytics YOLOv8", "FastAPI", "Uvicorn", "LabelImg (annotation)", "Docker (optional)"],
                "concepts": ["Object Detection (YOLO architecture)", "Anchor boxes & NMS", "mAP evaluation metric", "Model deployment & serving", "REST API design", "Real-time inference optimization"],
            },
            {
                "icon": "🧬", "title": "GAN Image Generator",
                "desc": "Build a DCGAN to generate realistic images with latent space exploration.",
                "tags": "GAN · PyTorch",
                "explanation": "Master generative AI! You'll implement a Deep Convolutional GAN with a Generator and Discriminator competing in a minimax game. Train on face datasets to generate realistic portraits, experiment with latent space interpolation (morphing between faces), and understand mode collapse, training instability, and techniques to stabilize GAN training.",
                "tools": ["Python 3.8+", "PyTorch", "torchvision", "Matplotlib", "NumPy", "GPU (required)"],
                "concepts": ["Generative Adversarial Networks", "Generator & Discriminator", "Minimax loss function", "Transposed convolutions", "Latent space interpolation", "Mode collapse & training tricks"],
            },
        ],
    }

    projects = mini_projects.get(level, mini_projects["Beginner"])

    # Render project cards in a 2-column grid
    for row_start in range(0, len(projects), 2):
        cols = st.columns(2)
        for col_idx, proj_idx in enumerate(range(row_start, min(row_start + 2, len(projects)))):
            p = projects[proj_idx]
            with cols[col_idx]:
                st.markdown(f"""
                <div class="mini-project-card">
                    <div class="mini-project-icon">{p['icon']}</div>
                    <div class="mini-project-title">{p['title']}</div>
                    <div class="mini-project-desc">{p['desc']}</div>
                    <div class="mini-project-tag">{p['tags']}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander(f"📖 Details — {p['title']}"):
                    st.markdown(f"**💡 What You'll Build:**\n\n{p['explanation']}")
                    st.markdown("---")
                    st.markdown("**🔧 Tools Required:**")
                    for tool in p["tools"]:
                        st.markdown(f"- `{tool}`")
                    st.markdown("---")
                    st.markdown("**🧠 Concepts You'll Learn:**")
                    for concept in p["concepts"]:
                        st.markdown(f"- {concept}")


# ─────────────────── STYLE SELECT ───────────────────────
def page_style_select():
    render_progress()

    topic_title = st.session_state.selected_topic_title

    st.markdown(f"""
    <div class="level-container">
        <div class="roadmap-badge">📚 {topic_title}</div>
        <div class="level-title">How would you like to learn?</div>
        <div class="level-subtitle">Choose the learning style that works best for you</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    styles = [
        ("📖", "Reading", "In-depth articles, explanations, and written guides", col1),
        ("🎧", "Auditory", "Listen to podcast-style audio lessons", col2),
        ("💻", "Kinesthetic", "Hands-on coding examples and practice problems", col3),
        ("🎨", "Visual", "AI-generated diagrams, infographics, and visuals", col4),
    ]

    for icon, name, desc, col in styles:
        with col:
            st.markdown(f"""
            <div class="style-card">
                <div class="style-icon">{icon}</div>
                <div class="style-name">{name}</div>
                <div class="style-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Choose {name}", key=f"style_{name}", use_container_width=True):
                st.session_state.learning_style = name
                st.session_state.content = None  # Reset content
                navigate("content")
                st.rerun()

    st.divider()
    if st.button("← Back to Roadmap"):
        navigate("roadmap")
        st.rerun()


# ─────────────────── CONTENT DELIVERY ───────────────────────
def page_content():
    render_progress()

    topic = st.session_state.selected_topic_title
    level = st.session_state.level
    style = st.session_state.learning_style

    style_icons = {"Reading": "📖", "Auditory": "🎧", "Kinesthetic": "💻", "Visual": "🎨"}

    st.markdown(f"""
    <div class="content-header">
        <div class="content-header-icon">{style_icons.get(style, "📘")}</div>
        <div class="content-header-text">
            <h2>{topic}</h2>
            <p>{style} Mode · {level} Level</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Generate content based on style
    if st.session_state.content is None:
        if style == "Reading":
            with st.spinner("📖 Generating your reading material..."):
                from utils.genai_utils import generate_reading_content
                st.session_state.content = generate_reading_content(topic, level)

        elif style == "Auditory":
            with st.spinner("🎧 Creating your audio lesson... This may take a moment."):
                from utils.genai_utils import generate_audio_script
                from utils.audio_utils import generate_audio
                script = generate_audio_script(topic, level)
                audio_path = generate_audio(script, topic)
                st.session_state.content = {"script": script, "audio_path": audio_path}

        elif style == "Kinesthetic":
            with st.spinner("💻 Generating code examples and problems..."):
                from utils.genai_utils import generate_code_content
                st.session_state.content = generate_code_content(topic, level)

        elif style == "Visual":
            with st.spinner("🎨 Finding videos & generating visual explanations..."):
                from utils.genai_utils import generate_visual_content
                from utils.video_utils import search_youtube_videos
                diagrams = generate_visual_content(topic, level)
                videos = search_youtube_videos(topic, max_results=3)
                st.session_state.content = {"diagrams": diagrams, "videos": videos}

    # Display content
    content = st.session_state.content

    if style == "Reading":
        st.markdown(content)

    elif style == "Auditory":
        st.markdown("### 🎧 Audio Lesson")
        if os.path.exists(content["audio_path"]):
            st.audio(content["audio_path"], format="audio/mp3")
        st.markdown("---")
        with st.expander("📜 View Lesson Script"):
            st.markdown(content["script"])

    elif style == "Kinesthetic":
        st.markdown(content)

    elif style == "Visual":
        # YouTube Videos
        videos = content.get("videos", []) if isinstance(content, dict) else []
        if videos:
            st.markdown("### 🎬 Video Tutorials")
            # Filter real videos vs search links
            real_videos = [v for v in videos if not v.get("is_search_link")]
            search_links = [v for v in videos if v.get("is_search_link")]

            if real_videos:
                vid_cols = st.columns(min(len(real_videos), 3))
                for i, video in enumerate(real_videos):
                    with vid_cols[i % 3]:
                        st.video(video["url"])
                        st.caption(f"**{video['title']}**")

            if search_links:
                for link in search_links:
                    st.markdown(f"🔗 [Search YouTube for more videos]({link['url']})")

            st.markdown("---")
        else:
            st.info("No videos found for this topic. Showing visual diagrams below.")

        # Text-based diagrams
        diagrams = content.get("diagrams", "") if isinstance(content, dict) else content
        if diagrams:
            st.markdown("### 📊 Visual Diagrams & Concept Maps")
            st.markdown(diagrams)

    st.divider()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Style Selection"):
            st.session_state.content = None
            navigate("style_select")
            st.rerun()
    with col2:
        if st.button("🔄 Try Another Style"):
            st.session_state.content = None
            navigate("style_select")
            st.rerun()
    with col3:
        if st.button("📝 Take Quiz →", type="primary"):
            st.session_state.quiz_data = None
            st.session_state.user_answers = {}
            navigate("quiz")
            st.rerun()


# ─────────────────── QUIZ ───────────────────────
def page_quiz():
    render_progress()

    topic = st.session_state.selected_topic_title
    level = st.session_state.level

    st.markdown(f"""
    <div class="content-header">
        <div class="content-header-icon">📝</div>
        <div class="content-header-text">
            <h2>Quiz: {topic}</h2>
            <p>3 questions · Scenario, Code Analysis, and MCQ</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Generate quiz
    if st.session_state.quiz_data is None:
        with st.spinner("📝 Preparing your quiz..."):
            from utils.genai_utils import generate_quiz
            st.session_state.quiz_data = generate_quiz(topic, level)

    quiz = st.session_state.quiz_data

    if not quiz:
        st.error("Failed to generate quiz. Please try again.")
        if st.button("🔄 Retry"):
            st.session_state.quiz_data = None
            st.rerun()
        return

    type_badges = {
        "scenario": ("🌍 Real-Life Scenario", "badge-scenario"),
        "code_analysis": ("💻 Code Analysis", "badge-code"),
        "mcq": ("✅ Multiple Choice", "badge-mcq"),
    }

    with st.form("quiz_form"):
        for i, q in enumerate(quiz):
            q_type = q.get("type", "mcq")
            badge_text, badge_class = type_badges.get(q_type, ("❓ Question", "badge-mcq"))

            st.markdown(f"""
            <div class="quiz-question">
                <span class="quiz-type-badge {badge_class}">{badge_text}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**Question {i+1}:** {q['question']}")

            if q_type == "mcq" and q.get("options"):
                answer = st.radio(
                    "Select your answer:",
                    options=q["options"],
                    key=f"quiz_q{i}",
                    index=None,
                )
                st.session_state.user_answers[i] = answer or ""
            elif q_type == "code_analysis" and q.get("options"):
                answer = st.radio(
                    "Select your answer:",
                    options=q["options"],
                    key=f"quiz_q{i}",
                    index=None,
                )
                st.session_state.user_answers[i] = answer or ""
            else:
                answer = st.text_area(
                    "Write your answer:",
                    key=f"quiz_q{i}",
                    height=100,
                )
                st.session_state.user_answers[i] = answer or ""

            st.markdown("---")

        submitted = st.form_submit_button("✅  Submit Answers", use_container_width=True)
        if submitted:
            answers_list = [st.session_state.user_answers.get(i, "") for i in range(len(quiz))]
            if any(a == "" for a in answers_list):
                st.warning("Please answer all questions before submitting.")
            else:
                st.session_state.feedback = None
                navigate("feedback")
                st.rerun()

    st.divider()
    if st.button("← Back to Content"):
        navigate("content")
        st.rerun()


# ─────────────────── FEEDBACK ───────────────────────
def page_feedback():
    render_progress()

    topic = st.session_state.selected_topic_title
    level = st.session_state.level
    quiz = st.session_state.quiz_data
    answers = [st.session_state.user_answers.get(i, "") for i in range(len(quiz))]

    if st.session_state.feedback is None:
        with st.spinner("🔍 Evaluating your answers..."):
            from utils.genai_utils import evaluate_answers
            st.session_state.feedback = evaluate_answers(topic, level, quiz, answers)

    fb = st.session_state.feedback

    # Score display
    score = fb.get("score", 0)
    total = fb.get("total", 3)
    pct = fb.get("percentage", 0)

    if pct >= 70:
        score_class = "score-high"
        emoji = "🎉"
    elif pct >= 40:
        score_class = "score-mid"
        emoji = "💪"
    else:
        score_class = "score-low"
        emoji = "📚"

    st.markdown(f"""
    <div class="score-display">
        <div class="score-circle {score_class}">{score}/{total}</div>
        <h2>{emoji} {pct}%</h2>
    </div>
    """, unsafe_allow_html=True)

    # Overall feedback
    st.markdown(f"### 📋 Feedback")
    st.info(fb.get("overall_feedback", ""))

    # Per-question feedback
    per_q = fb.get("per_question", [])
    for pq in per_q:
        q_num = pq.get("question_num", "?")
        is_correct = pq.get("is_correct", False)
        q_feedback = pq.get("feedback", "")
        if is_correct:
            st.success(f"**Question {q_num}**: ✅ Correct! {q_feedback}")
        else:
            st.error(f"**Question {q_num}**: ❌ {q_feedback}")

    # Strong & Weak areas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💪 Strong Areas")
        for area in fb.get("strong_areas", []):
            st.markdown(f"- ✅ {area}")
    with col2:
        st.markdown("### 📌 Areas to Improve")
        for area in fb.get("weak_areas", []):
            st.markdown(f"- 🔸 {area}")

    st.divider()

    # Award XP
    if topic not in st.session_state.topics_completed:
        st.session_state.topics_completed.append(topic)
        xp_earned = int(pct * 0.5) + 10  # 10-60 XP based on score
        award_xp(xp_earned)
        st.toast(f"🎉 +{xp_earned} XP earned!")
        if pct >= 70:
            show_confetti()

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("📖 Revision"):
            st.session_state.revision = None
            navigate("revision")
            st.rerun()
    with col2:
        if st.button("🃏 Flashcards"):
            st.session_state.flashcards = None
            navigate("flashcards")
            st.rerun()
    with col3:
        if st.button("🗺️ Roadmap"):
            navigate("roadmap")
            st.rerun()
    with col4:
        if len(st.session_state.topics_completed) >= 3:
            if st.button("🚀 Projects"):
                st.session_state.projects = None
                navigate("projects")
                st.rerun()


# ─────────────────── REVISION ───────────────────────
def page_revision():
    topic = st.session_state.selected_topic_title
    level = st.session_state.level
    fb = st.session_state.feedback or {}
    weak = fb.get("weak_areas", [])

    st.markdown(f"""
    <div class="content-header">
        <div class="content-header-icon">🔄</div>
        <div class="content-header-text">
            <h2>Revision: {topic}</h2>
            <p>Targeted material for your weak areas</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.revision is None:
        with st.spinner("🔄 Generating targeted revision material..."):
            from utils.genai_utils import generate_revision
            st.session_state.revision = generate_revision(topic, level, weak)

    st.markdown(st.session_state.revision)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗺️ Back to Roadmap"):
            navigate("roadmap")
            st.rerun()
    with col2:
        if st.button("📝 Retake Quiz"):
            st.session_state.quiz_data = None
            st.session_state.user_answers = {}
            st.session_state.feedback = None
            navigate("quiz")
            st.rerun()


# ─────────────────── PROJECTS ───────────────────────
def page_projects():
    topics = st.session_state.topics_completed
    level = st.session_state.level

    st.markdown(f"""
    <div class="content-header">
        <div class="content-header-icon">🚀</div>
        <div class="content-header-text">
            <h2>Capstone Project Suggestions</h2>
            <p>Based on {len(topics)} topics you've completed</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.projects is None:
        with st.spinner("🚀 Generating project ideas tailored to your learning..."):
            from utils.genai_utils import generate_project_suggestions
            st.session_state.projects = generate_project_suggestions(topics, level)

    st.markdown(st.session_state.projects)

    st.divider()
    if st.button("🗺️ Back to Roadmap"):
        navigate("roadmap")
        st.rerun()


# ─────────────────── FLASHCARDS ───────────────────────
def page_flashcards():
    topic = st.session_state.selected_topic_title
    level = st.session_state.level

    st.markdown(f"""
    <div class="content-header">
        <div class="content-header-icon">🃏</div>
        <div class="content-header-text">
            <h2>Flashcards: {topic}</h2>
            <p>Click each card to flip and reveal the answer</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.flashcards is None:
        with st.spinner("🃏 Creating flashcards..."):
            from utils.genai_utils import generate_flashcards
            st.session_state.flashcards = generate_flashcards(topic, level)

    cards = st.session_state.flashcards

    # Display flashcards in a grid
    cols = st.columns(min(len(cards), 3))
    for i, card in enumerate(cards):
        with cols[i % 3]:
            emoji = card.get("emoji", "📘")
            front = card.get("front", "Question")
            back = card.get("back", "Answer")
            card_key = f"card_{i}"

            # Toggle flip state
            is_flipped = st.session_state.get(card_key, False)
            flip_class = "flipped" if is_flipped else ""

            st.markdown(f"""
            <div class="flashcard {flip_class}">
                <div class="flashcard-inner">
                    <div class="flashcard-front">
                        <div style="font-size:2rem;margin-bottom:12px;">{emoji}</div>
                        {front}
                    </div>
                    <div class="flashcard-back">
                        {back}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 Flip" if not is_flipped else "↩️ Back", key=f"flip_{i}", use_container_width=True):
                st.session_state[card_key] = not is_flipped
                st.rerun()

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗺️ Back to Roadmap"):
            navigate("roadmap")
            st.rerun()
    with col2:
        if st.button("🔄 New Flashcards"):
            st.session_state.flashcards = None
            for i in range(10):
                if f"card_{i}" in st.session_state:
                    del st.session_state[f"card_{i}"]
            st.rerun()
    # Award XP for reviewing flashcards
    if "flashcards_xp_awarded" not in st.session_state:
        award_xp(15)
        st.session_state.flashcards_xp_awarded = True
        st.toast("🃏 +15 XP for reviewing flashcards!")


# ════════════════════════════════════════════════════════
#                 CONCEPT FLOW VISUALIZATION PAGE
# ════════════════════════════════════════════════════════

def page_concept_flow():
    """Full-page concept flow visualization."""
    topic = st.session_state.cf_topic
    level = st.session_state.level or "Beginner"

    st.markdown(f"""
    <div class="cf-header">
        <div class="cf-title">🔀 Concept Flow Visualization</div>
        <div class="cf-subtitle">
            {'Visualizing: <strong>' + topic + '</strong>' if topic else 'Enter a topic below to visualize its concept flow'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Topic input
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        new_topic = st.text_input(
            "Enter an ML topic:",
            value=topic or "",
            placeholder="e.g. Gradient Descent, Random Forest, Neural Networks...",
            key="cf_topic_input",
            label_visibility="collapsed"
        )
    with col2:
        lvl_opts = ["Beginner", "Intermediate", "Advanced"]
        cf_level = st.selectbox("Level", lvl_opts,
                                index=lvl_opts.index(level) if level in lvl_opts else 0,
                                key="cf_level_select",
                                label_visibility="collapsed")
    with col3:
        gen_btn = st.button("🔀 Visualize", use_container_width=True, type="primary")

    # Quick topic suggestions
    st.markdown("**Quick topics:**")
    quick_topics = ["Linear Regression", "Neural Networks", "Decision Trees",
                    "Gradient Descent", "Random Forest", "K-Means Clustering",
                    "Backpropagation", "Attention Mechanism", "SVM"]
    q_cols = st.columns(len(quick_topics))
    for i, qt in enumerate(quick_topics):
        with q_cols[i]:
            if st.button(qt, key=f"qt_{i}", use_container_width=True):
                st.session_state.cf_topic = qt
                st.session_state.cf_content = None
                st.rerun()

    st.divider()

    if gen_btn and new_topic.strip():
        st.session_state.cf_topic = new_topic.strip()
        st.session_state.cf_content = None
        st.rerun()

    if st.session_state.cf_topic:
        if st.session_state.cf_content is None:
            with st.spinner(f"🔀 Generating concept flow for '{st.session_state.cf_topic}'..."):
                from utils.genai_utils import generate_concept_flow
                st.session_state.cf_content = generate_concept_flow(
                    st.session_state.cf_topic, cf_level
                )

        # Display the concept flow
        st.markdown(f"""
        <div class="cf-content">
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.cf_content)
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.cf_content = None
                st.rerun()
        with col_b:
            if st.button("🗸 Generate Diagram", use_container_width=True):
                with st.spinner("🗸 Creating visual diagram..."):
                    import os
                    from utils.image_utils import generate_visual
                    img_path, desc = generate_visual(st.session_state.cf_topic)
                    if img_path and os.path.exists(img_path):
                        st.image(img_path, caption=f"🗸 {st.session_state.cf_topic} — Concept Diagram", use_container_width=True)
                        if desc:
                            st.caption(desc)
                    else:
                        st.warning(desc or "Image generation failed.")
        with col_c:
            if st.button("🗣️ Listen to Explanation", use_container_width=True):
                with st.spinner("🗣️ Generating audio..."):
                    from utils.genai_utils import generate_audio_script
                    from utils.audio_utils import generate_audio
                    script = generate_audio_script(st.session_state.cf_topic, cf_level)
                    audio_path = generate_audio(script, st.session_state.cf_topic)
                    if os.path.exists(audio_path):
                        st.audio(audio_path, format="audio/mp3")
                        st.caption("🎧 Audio explanation generated!")
    else:
        st.info("💡 Enter any ML topic above to see its complete concept flow visualization — how ideas connect, prerequisites, pipeline steps, and key parameters.")

    st.divider()
    if st.button("← Back to Roadmap"):
        navigate("roadmap")
        st.rerun()


# ════════════════════════════════════════════════════════
#                 GYANGURU FLOATING CHATBOT
# ════════════════════════════════════════════════════════

def render_gyanguru_panel():
    """
    Render the GyanGuru chatbot as an inline side-panel (copilot style).
    Called inside a st.column context — no floating CSS needed.
    """
    eff_level = st.session_state.gg_level or st.session_state.level or None
    level_emoji = {"Beginner": "🌱", "Intermediate": "🌿", "Advanced": "🌳"}.get(eff_level, "🧠")
    level_label = eff_level or "Auto-detect"
    context_topic = st.session_state.selected_topic_title

    # ── Panel header (uses side-panel CSS) ──
    st.markdown(f"""
    <div class="gg-panel-header">
        <div>
            <div class="title">🧠 GyanGuru</div>
            <div class="subtitle">Your Personal AI Tutor</div>
        </div>
        <div class="level-badge">{level_emoji} {level_label}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Welcome message on first open ──
    if not st.session_state.gg_messages:
        greeting = """👋 **Namaste! I'm GyanGuru!**

Ask me anything — academics, science, math, coding, ML, general knowledge & more!"""
        st.session_state.gg_messages.append({"role": "assistant", "content": greeting, "media": None})

    # ── Messages ──
    msg_container = st.container(height=350)
    with msg_container:
        for msg in st.session_state.gg_messages:
            role = msg["role"]
            content = msg.get("content", "")
            if role == "user":
                st.markdown(f"**👤 You:** {content}")
            else:
                st.markdown(f"**🧠 GyanGuru:**")
                st.markdown(content)
            st.markdown("---")

    # ── Mode selector (compact) ──
    mode_cols = st.columns(5)
    modes = [
        ("text", "💬"), ("flow", "🔀"), ("image", "🖼️"), ("audio", "🔊"), ("video", "🎥"),
    ]
    for i, (mode_key, mode_icon) in enumerate(modes):
        with mode_cols[i]:
            is_active = st.session_state.gg_mode == mode_key
            if st.button(mode_icon, key=f"gg_mode_{mode_key}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary",
                         help=mode_key.capitalize()):
                st.session_state.gg_mode = mode_key
                st.rerun()

    # ── Suggestion chips ──
    if st.session_state.gg_messages:
        last_bot = next((m for m in reversed(st.session_state.gg_messages)
                         if m["role"] == "assistant" and m.get("suggestions")), None)
        if last_bot and last_bot.get("suggestions"):
            for i, sug in enumerate(last_bot["suggestions"][:2]):
                label = f"💡 {sug[:35]}.." if len(sug) > 35 else f"💡 {sug}"
                if st.button(label, key=f"gg_sug_{i}_{len(st.session_state.gg_messages)}",
                             use_container_width=True):
                    st.session_state["gg_prefill"] = sug
                    st.rerun()

    # ── Input ──
    prefill = st.session_state.pop("gg_prefill", "") if "gg_prefill" in st.session_state else ""
    question = st.text_input(
        "Ask anything:",
        value=prefill,
        key="gg_input",
        placeholder="Type your question...",
        label_visibility="collapsed"
    )
    c1, c2 = st.columns([4, 1])
    with c1:
        send_btn = st.button("🚀 Ask", key="gg_send", use_container_width=True, type="primary")
    with c2:
        if st.button("🗑️", key="gg_clear", use_container_width=True, help="Clear chat"):
            st.session_state.gg_messages = []
            st.rerun()

    # ── Process question ──
    if send_btn and question.strip():
        q = question.strip()
        st.session_state.gg_messages.append({"role": "user", "content": q, "media": None})
        current_level = eff_level
        mode = st.session_state.gg_mode

        with st.spinner("🧠 Thinking..."):
            if mode == "text":
                from utils.genai_utils import answer_ml_chatbot
                result = answer_ml_chatbot(
                    q, level=current_level, context_topic=context_topic,
                    chat_history=st.session_state.gg_messages[:-1]
                )
                st.session_state.gg_messages.append({
                    "role": "assistant", "content": result["text"],
                    "suggestions": result.get("suggestions", []), "media": None
                })

            elif mode == "flow":
                from utils.genai_utils import generate_concept_flow_for_chat
                lvl = current_level or "Beginner"
                topic_name, flow_content = generate_concept_flow_for_chat(q, lvl)
                st.session_state.gg_messages.append({
                    "role": "assistant",
                    "content": f"🔀 **Concept Flow: {topic_name}**\n\n" + flow_content,
                    "media": None
                })
                st.session_state.cf_topic = topic_name
                st.session_state.cf_content = flow_content

            elif mode == "image":
                from utils.genai_utils import answer_ml_chatbot
                from utils.image_utils import generate_visual
                result = answer_ml_chatbot(q, level=current_level, context_topic=context_topic)
                img_path, img_desc = generate_visual(q)
                media_data = {"type": "image", "path": img_path, "desc": img_desc} if img_path else None
                st.session_state.gg_messages.append({
                    "role": "assistant", "content": result["text"],
                    "suggestions": result.get("suggestions", []), "media": media_data
                })

            elif mode == "audio":
                from utils.genai_utils import answer_ml_chatbot, generate_audio_script
                from utils.audio_utils import generate_audio
                result = answer_ml_chatbot(q, level=current_level, context_topic=context_topic)
                script = generate_audio_script(q, current_level or "Beginner")
                audio_path = generate_audio(script, q)
                media_data = {"type": "audio", "path": audio_path}
                st.session_state.gg_messages.append({
                    "role": "assistant", "content": result["text"],
                    "suggestions": result.get("suggestions", []), "media": media_data
                })

            elif mode == "video":
                from utils.genai_utils import answer_ml_chatbot
                from utils.video_utils import search_youtube_videos
                result = answer_ml_chatbot(q, level=current_level, context_topic=context_topic)
                videos = search_youtube_videos(q, max_results=3)
                media_data = {"type": "video", "videos": videos}
                st.session_state.gg_messages.append({
                    "role": "assistant", "content": result["text"],
                    "suggestions": result.get("suggestions", []), "media": media_data
                })

        st.rerun()

    # ── Render media for latest bot message ──
    latest_bot_with_media = next(
        (m for m in reversed(st.session_state.gg_messages)
         if m["role"] == "assistant" and m.get("media")), None
    )
    if latest_bot_with_media:
        media = latest_bot_with_media["media"]
        mtype = media.get("type")
        if mtype == "image" and media.get("path") and os.path.exists(media["path"]):
            st.image(media["path"], caption=media.get("desc", ""), use_container_width=True)
        elif mtype == "audio" and media.get("path") and os.path.exists(media["path"]):
            st.audio(media["path"], format="audio/mp3")
        elif mtype == "video" and media.get("videos"):
            for v in media["videos"][:2]:
                if v.get("video_id"):
                    st.video(v["url"])
                    st.caption(f"🎥 {v['title']}")
                else:
                    st.markdown(f"🔗 [{v['title']}]({v['url']})")


# ════════════════════════════════════════════════════════
#                    MAIN ROUTER
# ════════════════════════════════════════════════════════

def main():
    inject_css()
    init_session_state()

    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🧠 LearnSphere")
        st.caption("AI-Powered Learning Tutor")

        # XP & Level
        level_name, level_min, level_max = get_user_level()
        xp = st.session_state.xp
        progress_pct = min(100, int(((xp - level_min) / max(1, level_max - level_min)) * 100))

        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{xp}</div>
            <div class="stat-label">Total XP</div>
            <div style="margin-top:6px;font-size:0.85rem;font-weight:600;">{level_name}</div>
            <div class="xp-bar-container">
                <div class="xp-bar" style="width:{progress_pct}%"></div>
            </div>
            <div style="font-size:0.65rem;color:#94a3b8;">{xp}/{level_max} XP to next level</div>
        </div>
        """, unsafe_allow_html=True)

        # Stats row
        s1, s2 = st.columns(2)
        with s1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.topics_completed)}</div>
                <div class="stat-label">Topics</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.badges)}</div>
                <div class="stat-label">Badges</div>
            </div>
            """, unsafe_allow_html=True)

        # Badges
        if st.session_state.badges:
            badges_html = " ".join(f'<span class="badge">{b}</span>' for b in st.session_state.badges)
            st.markdown(f"<div style='margin:8px 0;'>{badges_html}</div>", unsafe_allow_html=True)

        st.divider()

        if st.session_state.level:
            st.markdown(f"**Track:** {st.session_state.level}")
        if st.session_state.selected_topic_title:
            st.markdown(f"**Topic:** {st.session_state.selected_topic_title}")

        if st.session_state.topics_completed:
            st.divider()
            st.markdown("**✅ Completed:**")
            for t in st.session_state.topics_completed:
                st.markdown(f"- {t}")

        st.divider()

        # Concept Flow shortcut in sidebar
        if st.button("🔀 Concept Flow Visualizer", use_container_width=True):
            navigate("concept_flow")
            st.rerun()

        if st.button("🏠 Start Over", use_container_width=True):
            gg_history = st.session_state.gg_messages[:]
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.gg_messages = gg_history
            st.rerun()

    # ─────────────── PAGE ROUTING WITH GYANGURU PANEL ───────────────
    page = st.session_state.page
    pages = {
        "welcome": page_welcome,
        "level_select": page_level_select,
        "roadmap": page_roadmap,
        "style_select": page_style_select,
        "content": page_content,
        "quiz": page_quiz,
        "feedback": page_feedback,
        "revision": page_revision,
        "flashcards": page_flashcards,
        "projects": page_projects,
        "concept_flow": page_concept_flow,
    }
    page_fn = pages.get(page, page_welcome)

    # Only show GyanGuru panel after level is selected
    show_gg = bool(st.session_state.level)

    if show_gg:
        # ── Toggle button row (always visible after level select) ──
        toggle_col1, toggle_col2 = st.columns([6, 1])
        with toggle_col2:
            btn_label = "✕ Close" if st.session_state.gg_open else "🧠 GyanGuru"
            btn_type = "secondary" if st.session_state.gg_open else "primary"
            if st.button(btn_label, key="gg_toggle", use_container_width=True, type=btn_type):
                st.session_state.gg_open = not st.session_state.gg_open
                st.rerun()

    if show_gg and st.session_state.gg_open:
        # ── Split layout: page content + GyanGuru side panel ──
        content_col, gyan_col = st.columns([3, 2])
        with content_col:
            page_fn()
        with gyan_col:
            st.markdown('<div class="gg-side-panel">', unsafe_allow_html=True)
            render_gyanguru_panel()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # ── Full-width page content ──
        page_fn()


if __name__ == "__main__":
    main()
