import sqlite3

DB_NAME = "expenses.db"


def get_connection():
    """Returns a connection to the database."""
    return sqlite3.connect(DB_NAME)


def initialize_database():
    """Initializes the database by creating the necessary tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    with open("schema.sql", "r", encoding="utf-8") as file:
        cursor.executescript(file.read())

    conn.commit()
    conn.close()

def drop_tables():
    """Drops the tables in the database. This is used for testing purposes."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS expenses")
    cursor.execute("DROP TABLE IF EXISTS users")

    conn.commit()
    conn.close()

def reset_database():
    """Resets the database by dropping the tables and reinitializing them.
    This is used for testing purposes."""
    drop_tables()
    initialize_database()

def create_test_user():
    """Creates a test user in the database. This is used for testing purposes."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password, budget) VALUES (?, ?, ?)",
    ("testuser", "123", 1000))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {"id": user_id, "username": "testuser"}
