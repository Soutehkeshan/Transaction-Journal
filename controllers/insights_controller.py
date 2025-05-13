from PyQt5.QtCore import QObject
from models.asset import Asset
from models.transaction import Transaction
from data_fetcher import fetch_price

class InsightsController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view

        # Connect view signal to controller slot
        self.view.calculate_gains_signal.connect(self.calculate_gains)

    def calculate_gains(self):
        # Fetch latest prices
        gold = Asset.get_gold_details()
        btc = Asset.get_btc_details()

        if not gold or not btc:
            print("Error: Could not fetch gold or BTC details.")
            return

        latest_gold_price = fetch_price(gold)
        latest_btc_price = fetch_price(btc)

        # Get all transactions
        for tx in Transaction.get_all():
            asset = Asset.get_by_symbol(tx.asset_id)
            if asset:
                latest_asset_price = fetch_price(asset)
                tx.calculate_gains(latest_asset_price, latest_gold_price, latest_btc_price)
                tx.save()

        print("Gains calculated and saved.")
