from datetime import datetime
from PyQt5.QtCore import QObject
from models.asset import Asset
from models.transaction import Transaction
from data_fetcher import fetch_gold_price, fetch_price

class InsightsController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view

        # Connect calculate button
        self.view.calculate_gains_btn.clicked.connect(self.calculate_gains)
        self.view.refresh_btn.clicked.connect(lambda: self.sort_and_display("timestamp", reverse=True))

        self.sort_and_display("timestamp", reverse=True)

    def calculate_gains(self):
        latest_gold_price = fetch_gold_price()
        latest_dollar_price = float(self.view.irr_input.text()) if self.view.irr_input.text() else 0

        for tx in Transaction.get_all():
            asset = Asset.get_by_id(tx.asset_id)
            if not asset:
                continue

            # Get latest asset price in original currency
            latest_asset_price = fetch_price(asset)

            tx_type = tx.type  # "buy" or "sell"
            tx.calculate_gains(latest_asset_price, latest_dollar_price, latest_gold_price, tx_type)

    def sort_and_display(self, key, reverse):
        transactions = Transaction.get_all()
        transactions = [tx for tx in transactions if hasattr(tx, key)]
        sorted_tx = sorted(transactions, key=lambda t: getattr(t, key), reverse=reverse)
        self.view.update_table(sorted_tx)
