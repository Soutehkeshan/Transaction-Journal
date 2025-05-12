from database.db_utils import get_db_connection

class Asset:
    def __init__(self, symbol, data_source=None, source_symbol=None, id=None):
        self.id = id
        self.symbol = symbol
        self.data_source = data_source
        self.source_symbol = source_symbol

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
                INSERT INTO assets (symbol, data_source, source_symbol)
                VALUES (?, ?, ?)
            """, (self.symbol, self.data_source, self.source_symbol))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE assets
                SET symbol = ?, data_source = ?, source_symbol = ?
                WHERE id = ?
            """, (self.symbol, self.data_source, self.source_symbol, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def get_all_symbols(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT symbol FROM assets")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    
    @classmethod
    def get_gold_details(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets WHERE symbol = 'XAUUSD'")
        rows = cursor.fetchall()
        conn.close()
        return rows[0] if rows else None
    
    @classmethod
    def get_btc_details(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets WHERE symbol = 'BTCUSDT'")
        rows = cursor.fetchall()
        conn.close()
        return rows[0] if rows else None
