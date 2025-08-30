# database.py
import sqlite3
import os

def get_connection():
    os.makedirs('database', exist_ok=True)
    db_path = os.path.join('database', 'transactions.db')
    return sqlite3.connect(db_path)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # --- Tickers (master table, replaces 'assets') ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tickers (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       symbol TEXT UNIQUE,
                          group_name TEXT
                   );
                   """)

    # --- Transactions (linked to tickers) ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS transactions (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       ticker_id INTEGER,
                       type TEXT CHECK(type IN ('خرید', 'فروش')),
                       amount REAL,
                       price_per_unit REAL,
                       equilibrium_price REAL,
                       equilibrium_price_date TEXT,
                       gold_price REAL,
                       dollar_price REAL,
                       timestamp TEXT,
                       note TEXT,
                       FOREIGN KEY (ticker_id) REFERENCES tickers(id)
                   );
                   """)

    # --- Gains (linked to transactions) ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS gains (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       transaction_id INTEGER,
                       latest_asset_price REAL,
                       irr_gain REAL,
                       usd_gain REAL,
                       gold_gain REAL,
                       FOREIGN KEY (transaction_id) REFERENCES transactions(id)
                   );
                   """)

    # --- Market data for each ticker ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS ticker_data (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       ticker_id INTEGER,
                       date TEXT,
                       open REAL,
                       high REAL,
                       low REAL,
                       adjClose REAL,
                       value REAL,
                       volume INTEGER,
                       count INTEGER,
                       yesterday REAL,
                       close REAL,
                       jdate TEXT,
                       FOREIGN KEY (ticker_id) REFERENCES tickers(id)
                   );
                   """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized with tickers, transactions, gains, and ticker_data.")
