from datetime import datetime
from data_fetcher import fetch_price
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

            tx_type = self.view.type_input.currentText()
            amount = float(self.view.amount_input.text())
            price = float(self.view.price_input.text())

            if self.view.use_market_prices_checkbox.isChecked():
                gold_price = fetch_price(Asset.get_gold_details())
                btc_price = fetch_price(Asset.get_btc_details())
            else:
                gold_price = self.view.gold_price_input.value()
                btc_price = self.view.btc_price_input.value()

            note = self.view.note_input.toPlainText().strip()
            if self.view.now_checkbox.isChecked():
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                timestamp = self.view.date_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")


            transaction = Transaction(symbol, tx_type, amount, price, gold_price, btc_price, timestamp, note)
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
