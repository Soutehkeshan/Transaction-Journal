from database.db_utils import get_db_connection

class Gain:
    def __init__(self, transaction_id, latest_asset_price, irr_gain, usd_gain, gold_gain, id=None):
        self.id                 = id
        self.latest_asset_price = latest_asset_price
        self.transaction_id     = transaction_id
        self.irr_gain           = irr_gain
        self.usd_gain           = usd_gain
        self.gold_gain          = gold_gain

    def save_or_update(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        if self.id is None:
            # Perform INSERT operation
            cursor.execute("""
                           INSERT INTO gains (transaction_id,
                           latest_asset_price, irr_gain,
                           usd_gain, gold_gain)
                           VALUES (?, ?, ?, ?, ?)
                           """, (self.transaction_id, self.latest_asset_price,
                                 self.irr_gain, self.usd_gain, self.gold_gain))
            self.id = cursor.lastrowid
        else:
            # Perform UPDATE operation
            cursor.execute("""
                           UPDATE gains
                           SET transaction_id = ?, latest_asset_price = ?,
                           irr_gain = ?, usd_gain = ?, gold_gain = ?
                           WHERE id = ?
                           """, (self.transaction_id, self.latest_asset_price, self.irr_gain,
                                 self.usd_gain, self.gold_gain, self.id))

        conn.commit()
        conn.close()

    @classmethod
    def get_by_transaction_id(cls, transaction_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, transaction_id, latest_asset_price, irr_gain, usd_gain, gold_gain FROM gains WHERE transaction_id = ?", (transaction_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], transaction_id=row[1], latest_asset_price=row[2], irr_gain=row[3], usd_gain=row[4], gold_gain=row[5])
        return None