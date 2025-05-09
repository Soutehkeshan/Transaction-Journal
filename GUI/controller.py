from datetime import datetime
from data_fetcher import fetch_price

class TransactionController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Populate symbol suggestions
        self.update_symbol_suggestions()

        self.view.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):
        try:
            symbol = self.view.symbol_input.text().strip().upper()
            tx_type = self.view.type_input.currentText()
            amount = float(self.view.amount_input.text())
            price = float(self.view.price_input.text())

            if self.view.use_market_prices_checkbox.isChecked():
                # You can later replace these with actual API calls
                gold_price = fetch_price(self.model.get_asset_info("XAUUSD"))
                btc_price = fetch_price(self.model.get_asset_info("BTCUSDT"))
            else:
                gold_price = self.view.gold_price_input.value()
                btc_price = self.view.btc_price_input.value()

            note = self.view.note_input.toPlainText().strip()
            if self.view.now_checkbox.isChecked():
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                timestamp = self.view.date_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")


            self.model.add_transaction(symbol, tx_type, amount, price, gold_price, btc_price, timestamp, note)
            self.view.status_label.setText("✅ Transaction added successfully!")
        except Exception as e:
            self.view.status_label.setText(f"❌ Error: {str(e)}")

    def update_symbol_suggestions(self):
        try:
            symbols = self.model.get_all_symbols()
            self.view.symbol_model.setStringList(symbols)
        except Exception as e:
            print(f"Error loading symbols: {e}")
