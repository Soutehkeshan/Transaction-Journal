from datetime import datetime
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox
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
        # Validate inputs first
        if not self.validate_inputs():
            return  # Stop execution if validation fails
        
        latest_gold_price = fetch_gold_price()
        latest_dollar_price = float(self.view.irr_input.text().replace(',', '')) 

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

    def validate_inputs(self):
        """Validate input fields before calculating gains"""
        dollar_price_text = self.view.irr_input.text().replace(',', '')  # Remove commas
        
        if not dollar_price_text:
            QMessageBox.warning(
                self.view, 
                "هشدار ورودی", 
                "قیمت دلار ۰ ذخیره شد زیرا آن را وارد نکردید"
            )
            return True
        
        try:
            dollar_price = float(dollar_price_text)
            if dollar_price < 200000:
                QMessageBox.warning(
                    self.view, 
                    "خطای ورودی", 
                    " توجه داشته باشید که قیمت دلار به ریال است و عدد ورودی شما کم است"
                )
                return False
        except ValueError:
            QMessageBox.warning(
                self.view, 
                "خطای ورودی", 
                "لطفاً یک عدد معتبر برای قیمت دلار وارد کنید."
            )
            return False
        
        return True