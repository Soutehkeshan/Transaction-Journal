from database.db_utils import get_db_connection

class Asset:
    def __init__(self, symbol, id=None):
        self.id=id
        self.symbol = symbol

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO assets (symbol)
            VALUES (?)
        """, (self.symbol,))
        self.id = cursor.lastrowid
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
    def get_by_symbol(cls, symbol):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets WHERE symbol = ?", (symbol,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row[0], symbol=row[1])
        return None
    
    @classmethod
    def get_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row[0], symbol=row[1])
        return None