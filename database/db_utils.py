import sqlite3
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "transactions.db")
print(f"DB_PATH: {DB_PATH}")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def get_asset_id_by_symbol(symbol: str) -> Optional[int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM assets WHERE symbol = ?", (symbol.upper(),))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_symbol_by_asset_id(id: int) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM assets WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
