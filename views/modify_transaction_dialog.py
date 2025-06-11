from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox, QLabel, QCompleter
from PyQt5.QtCore import Qt, QStringListModel
from models.asset import Asset  # Make sure this is your Asset model

class ModifyTransactionDialog(QDialog):
    def __init__(self, tx, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F8F8;
                font-family: "Tahoma", "Arial", "B Nazanin", "IRANSans", sans-serif;
                font-size: 10pt;
            }
            QLabel {
                color: #333;
                background: #F0F4F8;
                border: 1px solid #E0E0E0;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12pt;
                font-weight: 600;
                margin-left: 10px;
                margin-bottom: 4px;
                letter-spacing: 0.5px;
            }
            #statusLabel {
                color: #D32F2F;
                font-weight: bold;
                margin-top: 10px;
            }
            QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 8px;
                background-color: #FFFFFF;
                color: #333333;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #007ACC; /* Highlight on focus */
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 150px; /* Ensure button has a minimum width */
            }
            QPushButton:hover {
                background-color: #005F99;
            }
            QCheckBox {
                color: #333333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #999999;
                border-radius: 3px;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC; /* Blue background when checked */
                border: 1px solid #007ACC;
                image: url(C:/Users/moham/PycharmProjects/TseClient/assets/icons/tick_white.png); /* Path to your white tick icon */
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: left; /* Align dropdown arrow to the left for RTL */
                width: 20px;
                border-left-width: 1px;
                border-left-color: #CCCCCC;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(C:/Users/moham/PycharmProjects/TseClient/assets/icons/arrow_left.png); /* Path to your left-pointing arrow icon */
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                width: 20px;
                border-left: 1px solid #CCCCCC;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QDoubleSpinBox::up-arrow {
                image: url(C:/Users/moham/PycharmProjects/TseClient/assets/icons/arrow_up.png);
            }
            QDoubleSpinBox::down-arrow {
                image: url(C:/Users/moham/PycharmProjects/TseClient/assets/icons/arrow_down.png);
            }
                """)
        self.setWindowTitle("ویرایش تراکنش")
        self.tx = tx
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setFormAlignment(Qt.AlignRight | Qt.AlignTop)
        layout.setSpacing(12)
        layout.setRowWrapPolicy(QFormLayout.DontWrapRows)

        # --- Asset name with autocomplete ---
        self.assets = Asset.get_all_symbols()  # List of all assets

        self.asset_name_edit = QLineEdit()
        self.asset_name_edit.setMinimumWidth(170)
        self.asset_name_edit.setAlignment(Qt.AlignRight)
        self.asset_name_edit.setPlaceholderText("نام دارایی را وارد کنید")

        # Create and assign model and completer
        self.symbol_model = QStringListModel()
        self.symbol_model.setStringList(Asset.get_all_symbols())
        self.symbol_completer = QCompleter(self.symbol_model)
        self.symbol_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.asset_name_edit.setCompleter(self.symbol_completer)
        # Set current asset name
        current_asset = Asset.get_by_id(tx.asset_id) if tx.asset_id else None
        if current_asset:
            self.asset_name_edit.setText(current_asset.symbol)

        self.type_edit = QComboBox()
        self.type_edit.setEditable(False)
        self.type_edit.addItems(['خرید', 'فروش'])
        self.type_edit.setLayoutDirection(Qt.RightToLeft)
        if tx.type in ['خرید', 'فروش']:
            self.type_edit.setCurrentText(tx.type)
        self.type_edit.setMinimumWidth(170)
        self.type_edit.setStyleSheet("QComboBox { text-align: right; }")
        self.amount_edit = QLineEdit(str(tx.amount))
        self.price_edit = QLineEdit(str(tx.price_per_unit))
        self.gold_price_edit = QLineEdit(str(tx.gold_price))
        self.dollar_price_edit = QLineEdit(str(tx.dollar_price))
        self.timestamp_edit = QLineEdit(str(tx.timestamp))
        self.note_edit = QLineEdit(tx.note)

        layout.addRow(QLabel("نام دارایی:"), self.asset_name_edit)
        layout.addRow(QLabel("نوع:"), self.type_edit)
        layout.addRow(QLabel("تعداد:"), self.amount_edit)
        layout.addRow(QLabel("قیمت واحد:"), self.price_edit)
        layout.addRow(QLabel("قیمت طلا:"), self.gold_price_edit)
        layout.addRow(QLabel("قیمت دلار:"), self.dollar_price_edit)
        layout.addRow(QLabel("تاریخ و زمان:"), self.timestamp_edit)
        layout.addRow(QLabel("یادداشت:"), self.note_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Rename buttons to Persian
        buttons.button(QDialogButtonBox.Save).setText("ذخیره")
        buttons.button(QDialogButtonBox.Cancel).setText("انصراف")
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        return {
            "symbol": self.asset_name_edit.text().strip(),
            "type": self.type_edit.currentText(),
            "amount": float(self.amount_edit.text()),
            "price_per_unit": float(self.price_edit.text()),
            "gold_price": float(self.gold_price_edit.text()),
            "dollar_price": float(self.dollar_price_edit.text()),
            "timestamp": self.timestamp_edit.text(),
            "note": self.note_edit.text()
        }