from database.db_utils import get_db_connection

class Transaction:
    def __init__(self, asset_id, type, amount, price_per_unit,
                 gold_price, dollar_price, timestamp, note="", id=None, gold_gain=0, gain=0):
        self.id = id
        self.asset_id = asset_id
        self.type = type
        self.amount = amount
        self.price_per_unit = price_per_unit
        self.total = self.amount * self.price_per_unit
        self.gold_price = gold_price
        self.dollar_price = dollar_price
        self.timestamp = timestamp
        self.note = note
        self.gold_gain = gold_gain
        self.gain = gain

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                        INSERT INTO transactions (asset_id, type, amount, price_per_unit,
                        gold_price, dollar_price, timestamp, note, gold_gain, gain)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            self.asset_id, self.type, self.amount, self.price_per_unit,
                            self.gold_price, self.dollar_price, self.timestamp, self.note, 0, 0
                            ))
        self.id = cursor.lastrowid
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

    def calculate_gains(self, original_price, latest_price, latest_gold_price, tx_type):
        if not original_price or not latest_price:
            self.gain = 0
        else:
            self.gain = (
                latest_price / original_price if tx_type == "خرید"
                else original_price / latest_price
            )

        # Gold-relative gain
        if latest_gold_price and self.gold_price:
            self.gold_gain = (
                self.gain * (self.gold_price / latest_gold_price)
                if tx_type == "خرید"
                else self.gain * (latest_gold_price / self.gold_price)
            )
        else:
            self.gold_gain = 0

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
            gold_price=row[5],
            dollar_price=row[6],
            timestamp=row[7],
            note=row[8],
            gold_gain=row[9],
            gain=row[10]
        )

    def __repr__(self):
        return f"<Transaction id={self.id} asset_id={self.asset_id} type={self.type}>"
