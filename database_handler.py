import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            score REAL,
            severity TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_scan(url, score, severity):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans (url, score, severity, timestamp)
        VALUES (?, ?, ?, ?)
    """, (url, score, severity, datetime.now()))

    conn.commit()
    conn.close()