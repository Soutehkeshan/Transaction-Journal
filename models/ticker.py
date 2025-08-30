from database.db_utils import get_db_connection

class Ticker:
    def __init__(self, id, symbol, group_name):
        self.id = id
        self.symbol = symbol
        self.group_name = group_name

    @classmethod
    def get_all_symbols(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT symbol FROM tickers")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    @classmethod
    def get_by_symbol(cls, symbol):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickers WHERE symbol = ?", (symbol,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row[0], symbol=row[1], group_name=row[2])
        return None
    
    @classmethod
    def get_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickers WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row[0], symbol=row[1], group_name=row[2])
        return None