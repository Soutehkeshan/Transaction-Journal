from time import strptime
import jdatetime
from data_fetcher import fetch_gold_price
from models.transaction import Transaction
from models.asset import Asset
from views.PopUp import PopUp
from utility.persian_number_handler import PersianNumberHandler


class TransactionEntryController:
    def __init__(self, view):
        self.view = view

        # Populate symbol suggestions
        self.update_symbol_suggestions()

        self.view.submit_button.clicked.connect(self.handle_submit)

    # --- Utility Methods ---
    def parse_number(self, text, field_name):
        """Parse Persian/English number and return float (always English)."""
        try:
            text = text.strip()
            language = PersianNumberHandler.detect_number_language(text)
            if language == "persian":
                return float(PersianNumberHandler.fa_to_en(text))
            elif language == "english":
                return float(text)
            else:
                PopUp.show_error(f"مقدار وارد شده برای {field_name} معتبر نیست. لطفاً یک عدد وارد کنید.")
                return None
        except Exception:
            PopUp.show_error(f"مقدار وارد شده برای {field_name} معتبر نیست. لطفاً یک عدد وارد کنید.")
            return None

    def parse_date(self, text, fmt, field_name):
        """Parse Persian/English date and validate format (always English)."""
        try:
            text = text.strip()
            language = PersianNumberHandler.detect_number_language(text)
            if language == "persian":
                text = PersianNumberHandler.fa_to_en(text)
            elif language != "english":
                PopUp.show_error(f"تاریخ وارد شده برای {field_name} معتبر نیست. لطفاً یک تاریخ صحیح وارد کنید.")
                return None

            strptime(text, fmt)  # validate format
            return text
        except Exception:
            PopUp.show_error(f"تاریخ وارد شده برای {field_name} معتبر نیست. لطفاً یک تاریخ صحیح وارد کنید.")
            return None

    # --- Main Logic ---
    def handle_submit(self):
        # --- Symbol ---
        symbol = self.view.symbol_input.text().strip().upper()
        existing_symbols = Asset.get_all_symbols()
        if symbol not in existing_symbols:
            Asset(symbol).save()
        asset_id = Asset.get_by_symbol(symbol).id

        tx_type = self.view.type_input.currentText()

        # --- Amount ---
        amount = self.parse_number(self.view.amount_input.text(), "مقدار دارایی")
        if amount is None:
            return

        # --- Price ---
        price = self.parse_number(self.view.price_input.text(), "قیمت دارایی")
        if price is None:
            return

        # --- Equilibrium Price ---
        equilibrium_price = self.parse_number(self.view.equilibrium_price_input.text(), "قیمت تعادلی")
        if equilibrium_price is None:
            return

        # --- Equilibrium Price Date ---
        if self.view.equilibrium_price_now_checkbox.isChecked():
            equilibrium_price_date = jdatetime.datetime.now().strftime('%Y-%m-%d')
        else:
            equilibrium_price_date = self.parse_date(
                self.view.equilibrium_price_date_input.text(), "%Y-%m-%d", "قیمت تعادلی"
            )
            if equilibrium_price_date is None:
                return

        # --- Transaction Timestamp ---
        if self.view.now_checkbox.isChecked():
            timestamp = jdatetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp = self.parse_date(
                self.view.date_input.text(), "%Y-%m-%d %H:%M:%S", "تراکنش"
            )
            if timestamp is None:
                return

        # --- Gold Price ---
        if self.view.use_market_price_checkbox.isChecked():
            gold_price = fetch_gold_price()
        else:
            gold_price = self.parse_number(self.view.gold_price_input.text(), "قیمت طلا")
            if gold_price is None:
                return

        # --- Dollar Price ---
        dollar_price = self.parse_number(self.view.dollar_price_input.text(), "قیمت دلار")
        if dollar_price is None:
            return

        # --- Note ---
        note = self.view.note_input.toPlainText().strip()

        # --- Save Transaction ---
        transaction = Transaction(
            asset_id, tx_type, amount, price, equilibrium_price,
            equilibrium_price_date, gold_price, dollar_price, timestamp, note
        )
        transaction.save()
        PopUp.show_message("تراکنش با موفقیت ثبت شد! ✅")

        self.view.reset_form()

    def update_symbol_suggestions(self):
        try:
            symbols = Asset.get_all_symbols()
            self.view.symbol_model.setStringList(symbols)
        except Exception as e:
            print(f"Error loading symbols: {e}")
