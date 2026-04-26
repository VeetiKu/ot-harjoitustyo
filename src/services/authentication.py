from entities import User
from database import get_connection

class Authentication:
    def __init__(self):
        self.users = []

    def login(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username FROM users WHERE username=? AND password=?",
            (username, password))

        user = cursor.fetchone()
        conn.close()
        
        if not user:
            raise ValueError("Invalid credentials")

        return {"id": user[0], "username": user[1]}

    def register(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password))
            
            conn.commit()
        except Exception:
            raise ValueError("Username already exists")
        finally:
            conn.close()
