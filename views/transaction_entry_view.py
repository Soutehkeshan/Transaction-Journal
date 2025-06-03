from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QTextEdit, QCompleter, QDateTimeEdit, QCheckBox, QDoubleSpinBox
)
from PyQt5.QtCore import QStringListModel, QDateTime, pyqtSignal
from typing import List


class TransactionEntryView(QWidget):
    submitted = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Journal")

        self.init_inputs()
        self.init_layout()
        self.init_connections()

    def init_inputs(self):
        # Symbol input with autocompletion
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Asset Symbol (e.g., BTCUSDT)")
        self.symbol_model = QStringListModel()
        self.symbol_completer = QCompleter()
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

        self.manual_dollar_checkbox = QCheckBox("Enter exchange rate manually")
        self.manual_dollar_checkbox.setChecked(False)

        self.dollar_price_input = QDoubleSpinBox()
        self.dollar_price_input.setPrefix("1 unit = $")
        self.dollar_price_input.setMaximum(100000)
        self.dollar_price_input.setDecimals(4)
        self.dollar_price_input.setEnabled(False)

        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText("Optional note...")

        self.date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_input.setCalendarPopup(True)

        self.now_checkbox = QCheckBox("Use current time")
        self.now_checkbox.setChecked(True)
        self.date_input.setEnabled(False)

        self.use_market_prices_checkbox = QCheckBox("Use current BTC/Gold prices")
        self.use_market_prices_checkbox.setChecked(True)

        self.gold_price_input = QDoubleSpinBox()
        self.gold_price_input.setPrefix("Gold $")
        self.gold_price_input.setMaximum(100000)
        self.gold_price_input.setDecimals(2)
        self.gold_price_input.setEnabled(False)

        self.btc_price_input = QDoubleSpinBox()
        self.btc_price_input.setPrefix("BTC $")
        self.btc_price_input.setMaximum(1000000)
        self.btc_price_input.setDecimals(2)
        self.btc_price_input.setEnabled(False)

        self.submit_button = QPushButton("Submit")
        self.status_label = QLabel("")

    def init_layout(self):
        layout = QVBoxLayout()

        # Row 1: Symbol + Type
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Symbol:"))
        row1.addWidget(self.symbol_input)
        row1.addWidget(QLabel("Type:"))
        row1.addWidget(self.type_input)
        layout.addLayout(row1)

        # Row 2: Amount + Price + Unit
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Amount:"))
        row2.addWidget(self.amount_input)
        row2.addWidget(QLabel("Price:"))
        row2.addWidget(self.price_input)
        row2.addWidget(QLabel("Unit:"))
        row2.addWidget(self.unit_input)
        layout.addLayout(row2)

        # Row 3: Manual dollar checkbox + input
        row3 = QHBoxLayout()
        row3.addWidget(self.manual_dollar_checkbox)
        row3.addWidget(self.dollar_price_input)
        layout.addLayout(row3)

        # Note input
        layout.addWidget(QLabel("Note:"))
        layout.addWidget(self.note_input)

        # Row 4: Date picker + checkbox
        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Date:"))
        row4.addWidget(self.date_input)
        row4.addWidget(self.now_checkbox)
        layout.addLayout(row4)

        # Row 5: BTC + Gold prices + checkbox
        row5 = QHBoxLayout()
        row5.addWidget(self.use_market_prices_checkbox)
        row5.addWidget(self.gold_price_input)
        row5.addWidget(self.btc_price_input)
        layout.addLayout(row5)

        # Submission and status
        layout.addWidget(self.submit_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def init_connections(self):
        self.now_checkbox.stateChanged.connect(self.toggle_date_input)
        self.use_market_prices_checkbox.stateChanged.connect(self.toggle_price_inputs)
        self.manual_dollar_checkbox.stateChanged.connect(
            lambda state: self.dollar_price_input.setEnabled(state == 2)
        )
        self.submit_button.clicked.connect(self.submitted.emit)

    def toggle_date_input(self, state):
        self.date_input.setEnabled(not state)

    def toggle_price_inputs(self, state):
        manual = not state
        self.gold_price_input.setEnabled(manual)
        self.btc_price_input.setEnabled(manual)

    def get_form_data(self):
        return {
            "symbol": self.symbol_input.text().strip(),
            "type": self.type_input.currentText(),
            "amount": self.amount_input.text().strip(),
            "price": self.price_input.text().strip(),
            "unit": self.unit_input.currentText(),
            "note": self.note_input.toPlainText().strip(),
            "datetime": QDateTime.currentDateTime() if self.now_checkbox.isChecked()
                        else self.date_input.dateTime(),
            "use_market_prices": self.use_market_prices_checkbox.isChecked(),
            "gold_price": self.gold_price_input.value(),
            "btc_price": self.btc_price_input.value(),
            "manual_dollar": self.manual_dollar_checkbox.isChecked(),
            "dollar_price": self.dollar_price_input.value()
        }

    def update_symbol_completer(self, symbols: List[str]):
        self.symbol_model.setStringList(symbols)

    def show_status(self, message: str):
        self.status_label.setText(message)
