from datetime import datetime
from data_fetcher import fetch_price, get_exchange_rate
from database.db_utils import get_asset_id_by_symbol
from models.transaction import Transaction
from models.asset import Asset

class TransactionEntryController:
    def __init__(self, view):
        self.view = view

        # Populate symbol suggestions
        self.update_symbol_suggestions()

        self.view.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):
        try:
            symbol = self.view.symbol_input.text().strip().upper()
            existing_symbols = Asset.get_all_symbols()
            if symbol not in existing_symbols:
                self.view.status_label.setText("❌ Error: This asset does not exist. Please add it first.")
                return
            
            asset_id = get_asset_id_by_symbol(symbol)

            tx_type = self.view.type_input.currentText()
            amount = float(self.view.amount_input.text())
            price = float(self.view.price_input.text())
            unit = self.view.unit_input.currentText()

            # --- Date handling ---
            if self.view.now_checkbox.isChecked():
                timestamp_dt = datetime.now()
            else:
                timestamp_qt = self.view.date_input.dateTime()
                timestamp_dt = timestamp_qt.toPyDateTime()

            # --- Dollar price per unit logic ---
            if self.view.manual_dollar_checkbox.isChecked():
                currency_exchange_rate = self.view.currency_exchange_rate.value()
            else:
                exchange_rate = get_exchange_rate(unit, timestamp_dt)
                if unit == "IRR":
                    self.view.status_label.setText(f"❌ Fetching IRR is not supported. Please enter it manually.")
                    return
                if exchange_rate is None:
                    self.view.status_label.setText(f"❌ Could not find exchange rate for {unit} on {timestamp_dt.date()}")
                    return
                currency_exchange_rate = exchange_rate

            # --- Market prices ---
            if self.view.use_market_prices_checkbox.isChecked():
                gold_price = fetch_price(Asset.get_gold_details())
                btc_price = fetch_price(Asset.get_btc_details())
            else:
                gold_price = self.view.gold_price_input.value()
                btc_price = self.view.btc_price_input.value()

            note = self.view.note_input.toPlainText().strip()
            timestamp_str = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")

            transaction = Transaction(asset_id, tx_type, amount, price, unit, currency_exchange_rate, gold_price, btc_price, timestamp_str, note)
            transaction.save()
            self.view.status_label.setText("✅ Transaction added successfully!")

        except Exception as e:
            self.view.status_label.setText(f"❌ Error: {str(e)}")

    def update_symbol_suggestions(self):
        try:
            symbols = Asset.get_all_symbols()
            self.view.symbol_model.setStringList(symbols)
        except Exception as e:
            print(f"Error loading symbols: {e}")
