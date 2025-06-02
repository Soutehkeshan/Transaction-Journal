from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,
    QTextEdit, QCompleter, QDateTimeEdit, QCheckBox, QDoubleSpinBox
)
from PyQt5.QtCore import QStringListModel, QDateTime, pyqtSignal
from typing import List


class TransactionEntryView(QWidget):
    submitted = pyqtSignal()  # Controller will connect to this

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Journal")

        # --- Inputs ---
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Asset Symbol (e.g., BTCUSDT)")

        self.symbol_completer = QCompleter()
        self.symbol_model = QStringListModel()
        self.symbol_completer.setModel(self.symbol_model)
        self.symbol_completer.setCaseSensitivity(False)
        self.symbol_input.setCompleter(self.symbol_completer)

        self.type_input = QComboBox()
        self.type_input.addItems(["buy", "sell"])

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price per unit")

        self.unit_input = QComboBox()
        self.unit_input.addItems(["USD", "GBP", "IRR"])

        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText("Optional note...")

        self.date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_input.setCalendarPopup(True)

        self.now_checkbox = QCheckBox("Use current time")
        self.now_checkbox.setChecked(True)
        self.date_input.setEnabled(False)
        self.now_checkbox.stateChanged.connect(self.toggle_date_input)

        self.gold_price_input = QDoubleSpinBox()
        self.gold_price_input.setPrefix("Gold $")
        self.gold_price_input.setMaximum(100000)
        self.gold_price_input.setDecimals(2)

        self.btc_price_input = QDoubleSpinBox()
        self.btc_price_input.setPrefix("BTC $")
        self.btc_price_input.setMaximum(1000000)
        self.btc_price_input.setDecimals(2)

        self.use_market_prices_checkbox = QCheckBox("Use current BTC/Gold prices")
        self.use_market_prices_checkbox.setChecked(True)
        self.gold_price_input.setEnabled(False)
        self.btc_price_input.setEnabled(False)
        self.use_market_prices_checkbox.stateChanged.connect(self.toggle_price_inputs)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submitted.emit)

        self.status_label = QLabel("")  # Optional: this could also move to a dialog/messagebox

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Asset Symbol:"))
        layout.addWidget(self.symbol_input)
        layout.addWidget(QLabel("Transaction Type:"))
        layout.addWidget(self.type_input)
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Price per Unit:"))
        layout.addWidget(self.price_input)
        layout.addWidget(QLabel("Currency Unit:"))
        layout.addWidget(self.unit_input)
        layout.addWidget(QLabel("Note:"))
        layout.addWidget(self.note_input)
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_input)
        layout.addWidget(self.now_checkbox)
        layout.addWidget(self.use_market_prices_checkbox)
        layout.addWidget(self.gold_price_input)
        layout.addWidget(self.btc_price_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def toggle_date_input(self, state):
        self.date_input.setEnabled(not state)

    def toggle_price_inputs(self, state):
        use_manual = not state
        self.gold_price_input.setEnabled(use_manual)
        self.btc_price_input.setEnabled(use_manual)

    def get_form_data(self):
        return {
            "symbol": self.symbol_input.text().strip(),
            "type": self.type_input.currentText(),
            "amount": self.amount_input.text().strip(),
            "price": self.price_input.text().strip(),
            "unit": self.unit_input.currentText(),
            "note": self.note_input.toPlainText().strip(),
            "datetime": QDateTime.currentDateTime() if self.now_checkbox.isChecked() else self.date_input.dateTime(),
            "use_market_prices": self.use_market_prices_checkbox.isChecked(),
            "gold_price": self.gold_price_input.value(),
            "btc_price": self.btc_price_input.value()
        }

    def update_symbol_completer(self, symbols: List[str]):
        self.symbol_model.setStringList(symbols)

    def show_status(self, message: str):
        self.status_label.setText(message)
