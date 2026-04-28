from database import get_connection

class Authentication:
    """Class that handles user authentication and registration"""

    def __init__(self):
        pass

    def login(self, username, password):
        """Logs in a user with the given username and password.
        Raises ValueError if the credentials are invalid."""

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
        """Registers a new user with the given username and password.
        Raises ValueError if the username is too short or already exists."""

        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")

        if len(password) < 3:
            raise ValueError("Password must be at least 3 characters")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password))

            conn.commit()
        except Exception as exc:
            raise ValueError("Username already exists") from exc
        finally:
            conn.close()
