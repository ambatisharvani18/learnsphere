"""
LearnSphere — Database Models (SQLite)
Handles user accounts, progress tracking, and learning history.
"""

import sqlite3
import json
import os
import bcrypt  # type: ignore

DB_PATH = os.path.join(os.path.dirname(__file__), "learnsphere.db")


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            email TEXT,
            display_name TEXT,
            auth_provider TEXT DEFAULT 'local',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            level TEXT,
            xp INTEGER DEFAULT 0,
            badges TEXT DEFAULT '[]',
            topics_completed TEXT DEFAULT '[]',
            current_topic TEXT,
            current_roadmap TEXT,
            learning_style TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            learning_style TEXT,
            quiz_score INTEGER,
            quiz_total INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


# ─────────────── USER MANAGEMENT ───────────────

def create_user(username, password, email="", display_name="", auth_provider="local"):
    """Create a new user. Returns user_id or None if username exists."""
    conn = get_db()
    try:
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() if password else None
        cursor = conn.execute(
            "INSERT INTO users (username, password_hash, email, display_name, auth_provider) VALUES (?, ?, ?, ?, ?)",
            (username, pw_hash, email, display_name or username, auth_provider)
        )
        user_id = cursor.lastrowid
        # Initialize progress
        conn.execute(
            "INSERT INTO user_progress (user_id) VALUES (?)",
            (user_id,)
        )
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def authenticate_user(username, password):
    """Authenticate user. Returns user dict or None."""
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row and row["password_hash"]:
        if bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
            return dict(row)
    return None


def get_user_by_id(user_id):
    """Get user by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def social_login(email: str, display_name: str, provider: str):
    """Handle social login (Google/Facebook). Creates user if not exists."""
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE email = ? AND auth_provider = ?", (email, provider)).fetchone()
    if row:
        conn.close()
        return dict(row)
    # Create new user
    username = email.split("@")[0] + f"_{provider}"
    cursor = conn.execute(
        "INSERT INTO users (username, email, display_name, auth_provider) VALUES (?, ?, ?, ?)",
        (username, email, display_name, provider)
    )
    user_id = cursor.lastrowid
    conn.execute("INSERT INTO user_progress (user_id) VALUES (?)", (user_id,))
    conn.commit()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user)


# ─────────────── PROGRESS MANAGEMENT ───────────────

def get_progress(user_id):
    """Get user progress."""
    conn = get_db()
    row = conn.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        data: dict = dict(row)
        data["badges"] = json.loads(data["badges"] or "[]")
        data["topics_completed"] = json.loads(data["topics_completed"] or "[]")
        data["current_roadmap"] = json.loads(data["current_roadmap"]) if data["current_roadmap"] else None
        return data
    return None


def save_progress(user_id: int, **kwargs):
    """Update user progress fields."""
    conn = get_db()
    fields: list = []
    values: list = []
    for key, val in kwargs.items():
        if key in ("level", "xp", "badges", "topics_completed", "current_topic", "current_roadmap", "learning_style"):
            fields.append(f"{key} = ?")
            if key in ("badges", "topics_completed"):
                values.append(json.dumps(val))
            elif key == "current_roadmap":
                values.append(json.dumps(val) if val else None)
            else:
                values.append(val)
    if fields:
        values.append(user_id)
        conn.execute(f"UPDATE user_progress SET {', '.join(fields)} WHERE user_id = ?", values)
        conn.commit()
    conn.close()


def add_xp(user_id, points):
    """Add XP to user."""
    conn = get_db()
    conn.execute("UPDATE user_progress SET xp = xp + ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    row = conn.execute("SELECT xp FROM user_progress WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return row["xp"] if row else 0


# ─────────────── HISTORY MANAGEMENT ───────────────

def add_history(user_id, topic, learning_style=None, quiz_score=None, quiz_total=None):
    """Add a learning history entry."""
    conn = get_db()
    conn.execute(
        "INSERT INTO learning_history (user_id, topic, learning_style, quiz_score, quiz_total) VALUES (?, ?, ?, ?, ?)",
        (user_id, topic, learning_style, quiz_score, quiz_total)
    )
    conn.commit()
    conn.close()


def get_history(user_id, limit=20):
    """Get learning history for a user."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM learning_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Initialize DB on import
init_db()
