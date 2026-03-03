import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect("finance.db", check_same_thread=False)

def create_tables():
    conn = connect()
    c = conn.cursor()

    # Users table (fixed family members)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Transactions
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            user TEXT,
            type TEXT,
            category TEXT,
            amount REAL
        )
    """)

    conn.commit()
    conn.close()

def add_transaction(user, t_type, category, amount):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO transactions VALUES (NULL,?,?,?,?,?)",
              (datetime.now(), user, t_type, category, amount))
    conn.commit()
    conn.close()

def get_transactions():
    conn = connect()
    c = conn.cursor()
    data = c.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return data