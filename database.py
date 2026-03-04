import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect("finance.db", check_same_thread=False)

def create_tables():
    conn = connect()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            user TEXT,
            person TEXT,
            type TEXT,
            category TEXT,
            amount REAL
        )
    """)

    conn.commit()
    conn.close()


def add_transaction(user, person, t_type, category, amount):
    conn = connect()
    c = conn.cursor()

    c.execute(
        "INSERT INTO transactions VALUES (NULL,?,?,?,?,?,?)",
        (datetime.now(), user, person, t_type, category, amount)
    )

    conn.commit()
    conn.close()


def get_transactions():
    conn = connect()
    c = conn.cursor()
    data = c.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return data


def delete_transaction(transaction_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()