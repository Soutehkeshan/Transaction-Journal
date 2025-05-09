# database.py
import sqlite3

def get_connection():
    return sqlite3.connect("transactions.db")

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