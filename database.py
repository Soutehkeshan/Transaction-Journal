# database.py
import sqlite3
import os

def get_connection():
    # Ensure that the 'database' folder exists
    os.makedirs('database', exist_ok=True)
    
    # Create the path to the database inside the 'database' folder
    db_path = os.path.join('database', 'transactions.db')
    
    # Return the connection to the database
    return sqlite3.connect(db_path)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS assets (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   symbol TEXT UNIQUE
                   );""")


    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS transactions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   asset_id INTEGER,
                   type TEXT CHECK(type IN ('خرید', 'فروش')),
                   amount REAL,
                   price_per_unit REAL,
                   equilibrium_price REAL,
                   equilibrium_price_date TEXT,
                   gold_price REAL,
                   dollar_price REAL,
                   timestamp TEXT,
                   note TEXT,
                   FOREIGN KEY (asset_id) REFERENCES assets(id)
                   )""")

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS gains (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   transaction_id INTEGER,
                   latest_asset_price REAL,
                   irr_gain REAL,
                   usd_gain REAL,
                   gold_gain REAL,
                   FOREIGN KEY (transaction_id) REFERENCES transactions(id)
                   )""")

    conn.commit()
    conn.close()

init_db()
print("Database initialized.")