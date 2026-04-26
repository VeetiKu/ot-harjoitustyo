import sqlite3

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    with open("schema.sql", "r") as file:
        cursor.executescript(file.read())

    conn.commit()
    conn.close()