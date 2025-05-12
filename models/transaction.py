from database.db_utils import get_db_connection

class Transaction:
    def __init__(self, asset_id, type, amount, price_per_unit, total,
                 gold_price, btc_price, timestamp, note="", id=None):
        self.id = id
        self.asset_id = asset_id
        self.type = type
        self.amount = amount
        self.price_per_unit = price_per_unit
        self.total = total
        self.gold_price = gold_price
        self.btc_price = btc_price
        self.timestamp = timestamp
        self.note = note

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
                INSERT INTO transactions (asset_id, type, amount, price_per_unit,
                    total, gold_price, btc_price, timestamp, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.asset_id, self.type, self.amount, self.price_per_unit,
                self.total, self.gold_price, self.btc_price, self.timestamp, self.note
            ))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE transactions
                SET asset_id=?, type=?, amount=?, price_per_unit=?, total=?,
                    gold_price=?, btc_price=?, timestamp=?, note=?
                WHERE id=?
            """, (
                self.asset_id, self.type, self.amount, self.price_per_unit,
                self.total, self.gold_price, self.btc_price, self.timestamp, self.note,
                self.id
            ))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is None:
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
        self.id = None

    @classmethod
    def get_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.from_row(row) if row else None

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()
        conn.close()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0],
            asset_id=row[1],
            type=row[2],
            amount=row[3],
            price_per_unit=row[4],
            total=row[5],
            gold_price=row[6],
            btc_price=row[7],
            timestamp=row[8],
            note=row[9]
        )

    def __repr__(self):
        return f"<Transaction id={self.id} asset_id={self.asset_id} type={self.type}>"
