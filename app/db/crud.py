import uuid
from sqlite3 import IntegrityError
from .base import get_connection
from app.core.security import get_password_hash

def get_user_by_email(email: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row

def get_user_by_username(username: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row

def create_user(username: str, email: str, password: str):
    conn = get_connection()
    hashed = get_password_hash(password)
    user_id = str(uuid.uuid4())
    try:
        conn.execute(
            "INSERT INTO users (id, username, email, hashed_password) VALUES (?,?,?,?)",
            (user_id, username, email, hashed)
        )
        conn.commit()
        return user_id
    except IntegrityError:
        return None
    finally:
        conn.close()
