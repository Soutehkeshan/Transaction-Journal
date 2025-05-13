from database.db_utils import get_db_connection

class Transaction:
    def __init__(self, asset_id, type, amount, price_per_unit, total,
                gold_price, btc_price, timestamp, note="", id=None,
                gold_gain=0, btc_gain=0, gain=0):
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
        self.gold_gain = gold_gain
        self.btc_gain = btc_gain
        self.gain = gain

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
                INSERT INTO transactions (asset_id, type, amount, price_per_unit,
                    total, gold_price, btc_price, timestamp, note, gold_gain, btc_gain, gain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.asset_id, self.type, self.amount, self.price_per_unit, self.total,
                self.gold_price, self.btc_price, self.timestamp, self.note, 0, 0, 0
            ))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE transactions
                SET asset_id=?, type=?, amount=?, price_per_unit=?, total=?,
                    gold_price=?, btc_price=?, timestamp=?, note=?,
                    gold_gain=?, btc_gain=?, gain=?
                WHERE id=?
            """, (
                self.asset_id, self.type, self.amount, self.price_per_unit,
                self.total, self.gold_price, self.btc_price, self.timestamp, self.note,
                self.gold_gain, self.btc_gain, self.gain, self.id
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

    def calculate_gains(self, latest_asset_price, latest_gold_price, latest_btc_price):
        self.gain = latest_asset_price / self.price_per_unit

        self.gold_gain = (
            self.gain * (self.gold_price / latest_gold_price)
            if latest_gold_price and self.gold_price else 0
        )
        self.btc_gain = (
            self.gain * (self.btc_price / latest_btc_price)
            if latest_btc_price and self.btc_price else 0
        )

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
            note=row[9],
            gold_gain=row[10],
            btc_gain=row[11],
            gain=row[12]
        )

    def __repr__(self):
        return f"<Transaction id={self.id} asset_id={self.asset_id} type={self.type}>"
