import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "transactions.db")
print(f"DB_PATH: {DB_PATH}")

def get_db_connection():
    return sqlite3.connect(DB_PATH)
