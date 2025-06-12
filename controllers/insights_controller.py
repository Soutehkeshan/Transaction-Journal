from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog
from models.asset import Asset
from models.transaction import Transaction
from data_fetcher import fetch_gold_price, fetch_min_price, fetch_max_price
from views.modify_transaction_dialog import ModifyTransactionDialog
from views.PopUp import PopUp

class InsightsController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view

        # Connect buttons
        self.view.calculate_gains_btn.clicked.connect(self.calculate_gains)
        self.view.refresh_btn.clicked.connect(lambda: self.sort_and_display("timestamp", reverse=True))
        self.view.modify_btn.clicked.connect(self.modify_selected_transaction)

        self.sort_and_display("timestamp", reverse=True)

    def calculate_gains(self):
        # Validate inputs first
        if not self.validate_inputs():
            return  # Stop execution if validation fails
        
        try:
            latest_gold_price = fetch_gold_price()
            self.view.latest_gold_price_label.setText(f"آخرین قیمت طلا: {latest_gold_price:,.0f}")
        except Exception as e:
            PopUp.show_error("خطا در دریافت قیمت طلا. لطفاً دوباره تلاش کنید.")
            return

        try:
            latest_dollar_price = float(self.view.irr_input.text().replace(',', '')) 
        except ValueError:
            PopUp.show_error("قیمت دلار وارد شده معتبر نیست. لطفاً یک عدد وارد کنید.")
            return

        for tx in Transaction.get_all():
            asset = Asset.get_by_id(tx.asset_id)
            if not asset:
                continue

            try:
                latest_asset_price = (
                    fetch_min_price(asset) if tx.type == "خرید" else fetch_max_price(asset)
                )
                tx.calculate_gains(latest_asset_price, latest_dollar_price, latest_gold_price, tx.type)
            except Exception as e:
                print(f"خطا در محاسبه سود برای {asset.symbol}: {e}")

    def sort_and_display(self, key, reverse):
        transactions = Transaction.get_all()
        transactions = [tx for tx in transactions if hasattr(tx, key)]
        sorted_tx = sorted(transactions, key=lambda t: getattr(t, key), reverse=reverse)
        self.view.update_table(sorted_tx)

    def modify_selected_transaction(self):
        selected = self.view.table.selectedItems()
        if not selected:
            PopUp.show_warning(message="لطفاً یک ردیف را انتخاب کنید.")
            return
        row = self.view.table.currentRow()
        if not hasattr(self.view, "_transactions") or row >= len(self.view._transactions):
            PopUp.show_error(message="تراکنش انتخاب‌ شده یافت نشد.")
            return

        tx = self.view._transactions[row]
        dialog = ModifyTransactionDialog(tx, self.view)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return  # Invalid input; error already shown by dialog
            try:
                symbol = data["symbol"]
                asset = Asset.get_by_symbol(symbol)
                if not asset:
                    asset = Asset(symbol=symbol)
                    asset.save()
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
                PopUp.show_message("تراکنش با موفقیت ویرایش شد ✅")
            except Exception as e:
                PopUp.show_error("ویرایش تراکنش با خطا مواجه شد. لطفاً دوباره تلاش کنید.")

    def validate_inputs(self):
        """Validate input fields before calculating gains"""
        dollar_price_text = self.view.irr_input.text().replace(',', '')  # Remove commas

        if not dollar_price_text:
            PopUp.show_warning(
                message="قیمت دلار وارد نشده است. مقدار آن صفر در نظر گرفته می‌شود."
            )
            self.view.irr_input.setText("0")
            return True

        try:
            dollar_price = float(dollar_price_text)
            if dollar_price < 200000:
                PopUp.show_error(
                    message="قیمت دلار بسیار کم است. آیا مطمئن هستید که واحد را به ریال وارد کرده‌اید؟"
                )
                return False
        except ValueError:
            PopUp.show_error("لطفاً یک عدد معتبر برای قیمت دلار وارد کنید.")
            return False

        return True
