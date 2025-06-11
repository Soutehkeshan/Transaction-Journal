from database.db_utils import get_db_connection
from models.gain import Gain

class Transaction:
    def __init__(self, asset_id, type, amount, price_per_unit,
                 gold_price, dollar_price, timestamp, note="", id=None):
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

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
                INSERT INTO transactions (asset_id, type, amount, price_per_unit,
                gold_price, dollar_price, timestamp, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.asset_id, self.type, self.amount, self.price_per_unit,
                self.gold_price, self.dollar_price, self.timestamp, self.note
            ))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE transactions
                SET asset_id = ?, type = ?, amount = ?, price_per_unit = ?,
                    gold_price = ?, dollar_price = ?, timestamp = ?, note = ?
                WHERE id = ?
            """, (
                self.asset_id, self.type, self.amount, self.price_per_unit,
                self.gold_price, self.dollar_price, self.timestamp, self.note, self.id
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

    def calculate_gains(self, latest_price, latest_dollar_price, latest_gold_price, tx_type):
        if not latest_price:
            irr_gain = 0
        else:
            irr_gain = (
                latest_price / self.price_per_unit if tx_type == "خرید"
                else self.price_per_unit / latest_price
            )

        # Dollar-relative gain
        if latest_dollar_price and self.dollar_price:
            dollar_gain = (
                irr_gain * (self.dollar_price / latest_dollar_price)
                if tx_type == "خرید"
                else irr_gain * (latest_dollar_price / self.dollar_price)
            )
        else:
            dollar_gain = 0

        # Gold-relative gain
        if latest_gold_price and self.gold_price:
            gold_gain = (
                irr_gain * (self.gold_price / latest_gold_price)
                if tx_type == "خرید"
                else irr_gain * (latest_gold_price / self.gold_price)
            )
        else:
            gold_gain = 0

        # Save gains in the gains table using the Gain model
        existing_gain = Gain.get_by_transaction_id(self.id)
        if existing_gain:
            # Update existing gain
            existing_gain.irr_gain = irr_gain
            existing_gain.usd_gain = dollar_gain
            existing_gain.gold_gain = gold_gain
            existing_gain.save_or_update()
        else:
            # Create new gain
            gain = Gain(transaction_id=self.id, irr_gain=irr_gain, usd_gain=dollar_gain, gold_gain=gold_gain)
            gain.save_or_update()

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
        )

    def __repr__(self):
        return f"<Transaction id={self.id} asset_id={self.asset_id} type={self.type}>"
