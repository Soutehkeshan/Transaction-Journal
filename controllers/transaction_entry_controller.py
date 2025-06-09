import jdatetime
from data_fetcher import fetch_gold_price
from models.transaction import Transaction
from models.asset import Asset

class TransactionEntryController:
    def __init__(self, view):
        self.view = view

        # Populate symbol suggestions
        self.update_symbol_suggestions()

        self.view.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):
        # try:
            symbol = self.view.symbol_input.text().strip().upper()

            existing_symbols = Asset.get_all_symbols()
            if symbol not in existing_symbols:
                asset = Asset(symbol)
                asset.save()
            
            asset_id = Asset.get_by_symbol(symbol).id

            tx_type = self.view.type_input.currentText()
            amount = float(self.view.amount_input.text())
            price = float(self.view.price_input.text())

            # --- Date handling ---
            if self.view.now_checkbox.isChecked():
                timestamp = jdatetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                timestamp_qt = self.view.date_input.dateTime()
                timestamp = timestamp_qt.toPyDateTime()

            # --- Market prices ---
            if self.view.use_market_price_checkbox.isChecked():
                gold_price = fetch_gold_price()
            else:
                gold_price = self.view.gold_price_input.value()

            dollar_price = self.view.dollar_price_input.value()

            note = self.view.note_input.toPlainText().strip()

            transaction = Transaction(asset_id, tx_type, amount, price, gold_price, dollar_price, timestamp, note)
            transaction.save()
            self.view.status_label.setText("✅ Transaction added successfully!")

        # except Exception as e:
        #     self.view.status_label.setText(f"❌ Error: {str(e)}")

    def update_symbol_suggestions(self):
        try:
            symbols = Asset.get_all_symbols()
            self.view.symbol_model.setStringList(symbols)
        except Exception as e:
            print(f"Error loading symbols: {e}")
