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
        symbol TEXT UNIQUE,         -- e.g. 'BTC', 'ETH', 'XAU'
        data_source TEXT,           -- e.g. 'binance', 'metals_api', 'alpha_vantage'
        source_symbol TEXT          -- e.g. 'GC=F', 'BTC-USD'
    );""")


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id INTEGER,
        type TEXT CHECK(type IN ('buy', 'sell')),
        amount REAL,
        price_per_unit REAL,
        total REAL,
        gold_price REAL,
        btc_price REAL,
        timestamp TEXT,
        note TEXT,
        gold_gain REAL,
        btc_gain REAL,
        gain REAL,
        FOREIGN KEY (asset_id) REFERENCES assets(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        asset_id INTEGER,
        price_usd REAL,
        FOREIGN KEY (asset_id) REFERENCES assets(id)
    )""")

    conn.commit()
    conn.close()

init_db()
print("Database initialized.")