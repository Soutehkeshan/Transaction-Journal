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
        return Asset(
            symbol='XAUUSD',
            data_source='yahoo_finance',
            source_symbol='GC=F'
        )

    @classmethod
    def get_btc_details(cls):
        return Asset(
            symbol='BTCUSDT',
            data_source='yahoo_finance',
            source_symbol='BTC-USD'
        )

    @classmethod
    def get_by_symbol(cls, symbol):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets WHERE symbol = ?", (symbol,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row[0], symbol=row[1], data_source=row[2], source_symbol=row[3])
        return None
    
    @classmethod
    def get_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row[0], symbol=row[1], data_source=row[2], source_symbol=row[3])
        return None