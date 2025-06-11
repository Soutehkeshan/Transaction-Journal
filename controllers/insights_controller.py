from datetime import datetime
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox, QDialog
from models.asset import Asset
from models.transaction import Transaction
from data_fetcher import fetch_gold_price, fetch_price
from views.modify_transaction_dialog import ModifyTransactionDialog
from views.PopUp import PopUp

class InsightsController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view

        # Connect calculate button
        self.view.calculate_gains_btn.clicked.connect(self.calculate_gains)
        self.view.refresh_btn.clicked.connect(lambda: self.sort_and_display("timestamp", reverse=True))
        self.view.modify_btn.clicked.connect(self.modify_selected_transaction)

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

    def modify_selected_transaction(self):
        selected = self.view.table.selectedItems()
        if not selected:
            PopUp.show_warning(title="انتخاب تراکنش", message="لطفاً یک ردیف را انتخاب کنید.")
            return
        row = self.view.table.currentRow()
        if not hasattr(self.view, "_transactions") or row >= len(self.view._transactions):
            PopUp.show_warning(title="خطا", message="تراکنش انتخاب‌شده یافت نشد.")
            return
        tx = self.view._transactions[row]
        dialog = ModifyTransactionDialog(tx, self.view)
        
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            symbol = data["symbol"]
            asset = Asset.get_by_symbol(symbol)
            if not asset:
                new_asset = Asset(symbol=symbol).save()  # Save new asset if it doesn't exist
                tx.asset_id = new_asset.id
            elif asset.id != tx.asset_id:
                tx.asset_id = asset.id
            
            tx.type = data["type"]
            tx.amount = data["amount"]
            tx.price_per_unit = data["price_per_unit"]
            tx.gold_price = data["gold_price"]
            tx.dollar_price = data["dollar_price"]
            tx.timestamp = data["timestamp"]
            tx.note = data["note"]
            tx.save()
            self.view.update_table(self.view._transactions)

    def validate_inputs(self):
        """Validate input fields before calculating gains"""
        dollar_price_text = self.view.irr_input.text().replace(',', '')  # Remove commas
        
        if not dollar_price_text:
            QMessageBox.warning(
                self.view, 
                "هشدار ورودی", 
                "قیمت دلار ۰ ذخیره شد زیرا آن را وارد نکردید"
            )
            self.view.irr_input.setText("0")
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