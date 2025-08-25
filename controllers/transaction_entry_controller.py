from operator import eq
import jdatetime
from data_fetcher import fetch_gold_price
from models.transaction import Transaction
from models.asset import Asset
from views.PopUp import PopUp

class TransactionEntryController:
    def __init__(self, view):
        self.view = view

        # Populate symbol suggestions
        self.update_symbol_suggestions()

        self.view.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):
        symbol = self.view.symbol_input.text().strip().upper()

        existing_symbols = Asset.get_all_symbols()
        if symbol not in existing_symbols:
            asset = Asset(symbol)
            asset.save()
        
        asset_id = Asset.get_by_symbol(symbol).id

        tx_type = self.view.type_input.currentText()

        try:
            amount = float(self.view.amount_input.text())
        except Exception as e:
            PopUp.show_error("مقدار وارد شده برای مقدار دارایی معتبر نیست. لطفاً یک عدد وارد کنید.")
            return
        try:
            price = float(self.view.price_input.text())
        except Exception as e:
            PopUp.show_error("مقدار وارد شده برای قیمت دارایی معتبر نیست. لطفاً یک عدد وارد کنید.")
            return
        
        try:
            equilibrium_price = float(self.view.equilibrium_price_input.text())
        except Exception as e:
            PopUp.show_error("مقدار وارد شده برای قیمت تعادلی معتبر نیست. لطفاً یک عدد وارد کنید.")
            return
        
        # --- Date handling ---
        if self.view.equilibrium_price_now_checkbox.isChecked():
            equilibrium_price_date = jdatetime.datetime.now().strftime('%Y-%m-%d')
        else:
            try:
                equilibrium_price_date_qt = self.view.equilibrium_price_date_input.toPyDate()
            except Exception as e:
                PopUp.show_error("تاریخ وارد شده برای قیمت تعادلی معتبر نیست. لطفاً یک تاریخ صحیح وارد کنید.")
                return
            equilibrium_price_date = equilibrium_price_date_qt.toPyDate()

        # --- Date handling ---
        if self.view.now_checkbox.isChecked():
            timestamp = jdatetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            try:
                timestamp_qt = self.view.date_input.toPyDateTime()
            except Exception as e:
                PopUp.show_error("تاریخ وارد شده برای تراکنش معتبر نیست. لطفاً یک تاریخ صحیح وارد کنید.")
                return
            timestamp = timestamp_qt.toPyDateTime()

        # --- Market prices ---
        if self.view.use_market_price_checkbox.isChecked():
            gold_price = fetch_gold_price()
        else:
            try:
                gold_price = float(self.view.gold_price_input.text())
            except Exception as e:
                PopUp.show_error("مقدار وارد شده برای قیمت طلا معتبر نیست. لطفاً یک عدد وارد کنید.")
                return
            
        try:
            dollar_price = float(self.view.dollar_price_input.text())
        except Exception as e:
            PopUp.show_error("مقدار وارد شده برای قیمت دلار معتبر نیست. لطفاً یک عدد وارد کنید.")
            return

        note = self.view.note_input.toPlainText().strip()

        transaction = Transaction(asset_id, tx_type, amount, price, equilibrium_price, equilibrium_price_date, gold_price, dollar_price, timestamp, note)
        transaction.save()
        PopUp.show_message("تراکنش با موفقیت ثبت شد! ✅")

    def update_symbol_suggestions(self):
        try:
            symbols = Asset.get_all_symbols()
            self.view.symbol_model.setStringList(symbols)
        except Exception as e:
            print(f"Error loading symbols: {e}")
