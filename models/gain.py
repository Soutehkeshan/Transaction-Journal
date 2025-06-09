from database.db_utils import get_db_connection

class Gain:
    def __init__(self, transaction_id, irr_gain, usd_gain, gold_gain, id=None):
        self.id                 = id
        self.transaction_id     = transaction_id
        self.irr_gain           = irr_gain
        self.usd_gain           = usd_gain
        self.gold_gain          = gold_gain

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO gains (transaction_id,
                       irr_gain, usd_gain, gold_gain)
                       VALUES (?, ?, ?, ?, ?)
                       """, (self.transaction_id, self.irr_gain,
                             self.usd_gain, self.gold_gain,))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def update(self):
        if self.id is None:
            raise ValueError("Cannot update Gain: id is None. Did you mean to call save()?")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE gains
                       SET transaction_id = ?, irr_gain = ?, usd_gain = ?, gold_gain = ?
                       WHERE id = ?
                       """, (self.transaction_id, self.irr_gain, self.usd_gain, self.gold_gain, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_transaction_id(cls, transaction_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, transaction_id, irr_gain, usd_gain, gold_gain FROM gains WHERE transaction_id = ?", (transaction_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], transaction_id=row[1], irr_gain=row[2], usd_gain=row[3], gold_gain=row[4])
        return None