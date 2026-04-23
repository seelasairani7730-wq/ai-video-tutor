# MODEL LAYER: User analytics + Progress tracking + Retention system
# Tables: progress (engagement), quiz_scores (performance), reminders (DAU)

import sqlite3

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # progress
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        completed INTEGER
    )
    """)

    # quiz scores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_scores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        total INTEGER
    )
    """)

    # reminders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()