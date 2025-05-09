from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,
    QTextEdit, QCompleter, QDateTimeEdit, QCheckBox, QDoubleSpinBox
)
from PyQt5.QtCore import QStringListModel, QDateTime


class TransactionView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Journal")

        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Asset Symbol (e.g., BTC)")

        # Placeholder model, will be populated by controller
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

        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText("Optional note...")

        self.date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_input.setCalendarPopup(True)

        self.now_checkbox = QCheckBox("Use current time")
        self.now_checkbox.setChecked(True)
        self.date_input.setEnabled(False)

        # Gold and BTC Price Inputs
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

        # Toggle manual date input
        self.now_checkbox.stateChanged.connect(self.toggle_date_input)

        self.submit_button = QPushButton("Submit")
        self.status_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Asset Symbol:"))
        layout.addWidget(self.symbol_input)
        layout.addWidget(QLabel("Transaction Type:"))
        layout.addWidget(self.type_input)
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Price per Unit:"))
        layout.addWidget(self.price_input)
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

