import sqlite3

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            reply TEXT NOT NULL,
            intent TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()

# ---- Users ----

def add_user(username: str, password_hash: str) -> bool:
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_user(username: str) -> Optional[tuple[int, str, str, str]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, created_at FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    return row

# ---- Logs ----

def log_chat(username: str, message: str, reply: str, intent: str = "unknown"):
    conn = get_conn()
    conn.execute(
        "INSERT INTO chats (username, message, reply, intent) VALUES (?, ?, ?, ?)",
        (username, message, reply, intent),
    )
    conn.commit()
    conn.close()