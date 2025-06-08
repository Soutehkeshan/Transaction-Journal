from datetime import datetime
from PyQt5.QtCore import QObject
from models.asset import Asset
from models.transaction import Transaction
from data_fetcher import fetch_price, get_exchange_rate

class InsightsController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view

        # Connect calculate button
        self.view.calculate_gains_btn.clicked.connect(self.calculate_gains)

        # Connect sort buttons
        self.view.most_asset_btn.clicked.connect(lambda: self.sort_and_display("gain", reverse=True))
        self.view.least_asset_btn.clicked.connect(lambda: self.sort_and_display("gain", reverse=False))
        self.view.most_btc_btn.clicked.connect(lambda: self.sort_and_display("btc_gain", reverse=True))
        self.view.least_btc_btn.clicked.connect(lambda: self.sort_and_display("btc_gain", reverse=False))
        self.view.most_gold_btn.clicked.connect(lambda: self.sort_and_display("gold_gain", reverse=True))
        self.view.least_gold_btn.clicked.connect(lambda: self.sort_and_display("gold_gain", reverse=False))
        self.view.date_asc_btn.clicked.connect(lambda: self.sort_and_display("timestamp", reverse=False))
        self.view.date_desc_btn.clicked.connect(lambda: self.sort_and_display("timestamp", reverse=True))

    def calculate_gains(self):
        gold = Asset.get_gold_details()
        btc = Asset.get_btc_details()

        if not gold or not btc:
            print("Error: Could not fetch gold or BTC details.")
            return

        latest_gold_price = fetch_price(gold)
        latest_btc_price = fetch_price(btc)
        timestamp_dt = datetime.now()
        GBP_to_USD = get_exchange_rate("GBP", timestamp_dt)
        IRR_to_USD = (1/float(self.view.irr_input.text())) if self.view.irr_input.text() else None

        for tx in Transaction.get_all():
            asset = Asset.get_by_id(tx.asset_id)
            if not asset:
                continue

            # Get latest asset price in original currency
            latest_asset_price = fetch_price(asset)

            # Convert both to USD
            if tx.unit == "USD":
                original_price_usd = tx.price_per_unit
                latest_price_usd = latest_asset_price
            elif tx.unit == "GBP":
                original_price_usd = tx.price_per_unit * tx.currency_exchange_rate
                latest_price_usd = latest_asset_price * GBP_to_USD
            elif tx.unit == "IRR":
                original_price_usd = tx.price_per_unit * tx.currency_exchange_rate
                latest_price_usd = latest_asset_price * IRR_to_USD
            else:
                print(f"Unsupported currency unit: {tx.unit}")
                continue

            tx_type = tx.type  # "buy" or "sell"
            print(original_price_usd, latest_price_usd, latest_gold_price, latest_btc_price, tx_type)
            tx.calculate_gains(original_price_usd, latest_price_usd, latest_gold_price, latest_btc_price, tx_type)
            tx.save()

        print("Gains calculated and saved.")


    def sort_and_display(self, key, reverse):
        transactions = Transaction.get_all()
        transactions = [tx for tx in transactions if hasattr(tx, key)]
        sorted_tx = sorted(transactions, key=lambda t: getattr(t, key), reverse=reverse)
        self.view.update_table(sorted_tx)
