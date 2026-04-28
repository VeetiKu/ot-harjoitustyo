CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    budget REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT,
    recurring INTEGER DEFAULT 0,
    last_applied TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);