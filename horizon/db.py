"""SQLite storage for enquiries, viewing requests and newsletter sign-ups.

The public site is server-rendered from :mod:`horizon.data`; this module only
persists what visitors send us. The database file lives inside the package's
``data`` directory, which is git-ignored.
"""
import os
import sqlite3
from contextlib import closing

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "horizon.db")


def connect():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(connect()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL DEFAULT 'contact',
                property_slug TEXT DEFAULT '',
                name TEXT DEFAULT '',
                email TEXT DEFAULT '',
                phone TEXT DEFAULT '',
                message TEXT DEFAULT '',
                preferred_date TEXT DEFAULT '',
                preferred_time TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def add_enquiry(kind, name, email, phone="", message="", property_slug="",
                preferred_date="", preferred_time=""):
    with closing(connect()) as conn:
        cur = conn.execute(
            """
            INSERT INTO enquiries
                (kind, property_slug, name, email, phone, message,
                 preferred_date, preferred_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (kind, property_slug, name, email, phone, message,
             preferred_date, preferred_time),
        )
        conn.commit()
        return cur.lastrowid


def add_subscriber(email):
    """Store a newsletter address. Returns False when it was already known."""
    with closing(connect()) as conn:
        try:
            conn.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def enquiry_count():
    with closing(connect()) as conn:
        return conn.execute("SELECT COUNT(*) FROM enquiries").fetchone()[0]
