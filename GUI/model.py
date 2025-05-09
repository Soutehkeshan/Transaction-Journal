import sqlite3

DB_NAME = "transactions.db"

class TransactionModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER,
                type TEXT,
                amount REAL,
                price_per_unit REAL,
                total REAL,
                gold_price REAL,
                btc_price REAL,
                timestamp TEXT,
                note TEXT,
                FOREIGN KEY(asset_id) REFERENCES assets(id)
            )
        ''')
        self.conn.commit()

    def add_transaction(self, symbol, tx_type, amount, price, gold_price, btc_price, timestamp, note):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO assets (symbol) VALUES (?)", (symbol,))
        cursor.execute("SELECT id FROM assets WHERE symbol = ?", (symbol,))
        asset_id = cursor.fetchone()[0]

        total = amount * price
        cursor.execute('''
            INSERT INTO transactions (asset_id, type, amount, price_per_unit, total, gold_price, btc_price, timestamp, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (asset_id, tx_type, amount, price, total, gold_price, btc_price, timestamp, note))

        self.conn.commit()

    def get_all_symbols(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT symbol FROM assets")
        return [row[0] for row in cursor.fetchall()]
    
    def get_asset_info(self, symbol):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM assets WHERE symbol = ?", (symbol,))
        return cursor.fetchone()

