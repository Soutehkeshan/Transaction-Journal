from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from database.db_utils import get_symbol_by_asset_id

class InsightsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Calculate Gains button
        self.calculate_gains_btn = QPushButton("Calculate Gains")
        layout.addWidget(self.calculate_gains_btn)

        # Sorting buttons
        button_layout_1 = QHBoxLayout()
        self.most_asset_btn = QPushButton("Most Asset Gain")
        self.most_btc_btn = QPushButton("Most BTC Gain")
        self.most_gold_btn = QPushButton("Most Gold Gain")
        self.date_desc_btn = QPushButton("Date Descending")

        button_layout_2 = QHBoxLayout()
        self.least_asset_btn = QPushButton("Least Asset Gain")
        self.least_btc_btn = QPushButton("Least BTC Gain")
        self.least_gold_btn = QPushButton("Least Gold Gain")
        self.date_asc_btn = QPushButton("Date Ascending")

        for btn in [
            self.most_asset_btn, self.most_btc_btn,
            self.most_gold_btn, self.date_desc_btn
        ]:
            button_layout_1.addWidget(btn)

        for btn in [
            self.least_asset_btn, self.least_btc_btn,
            self.least_gold_btn, self.date_asc_btn
        ]:
            button_layout_2.addWidget(btn)

        button_layout = QVBoxLayout()

        button_layout.addLayout(button_layout_1)
        button_layout.addLayout(button_layout_2)

        layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels([
            "Asset", "Type", "Amount", "Price per Unit",
            "Unit", "Dollar Price per Unit", "Total", "Dollar Total",
            "Gold Price", "BTC Price", "Note",
            "Gain", "BTC Gain", "Gold Gain", "DateTime"
        ])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update_table(self, transactions):
        self.table.setRowCount(len(transactions))
        for row, tx in enumerate(transactions):
            total_value = tx.amount * tx.price_per_unit
            dollar_total_value = tx.amount * tx.dollar_price_per_unit
            self.table.setItem(row, 0, QTableWidgetItem(get_symbol_by_asset_id(tx.asset_id)))
            self.table.setItem(row, 1, QTableWidgetItem(tx.type))
            self.table.setItem(row, 2, QTableWidgetItem(f"{tx.amount:.5f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{tx.price_per_unit:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(tx.unit))
            self.table.setItem(row, 5, QTableWidgetItem(f"{tx.dollar_price_per_unit:.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{total_value:.2f}"))
            self.table.setItem(row, 7, QTableWidgetItem(f"{dollar_total_value:.2f}"))

            self.table.setItem(row, 8, QTableWidgetItem(f"{tx.gold_price:.2f}"))
            self.table.setItem(row, 9, QTableWidgetItem(f"{tx.btc_price:.2f}"))
            self.table.setItem(row, 10, QTableWidgetItem(tx.note))

            self.table.setItem(row, 11, QTableWidgetItem(f"{tx.gain:.2f}"))
            self.table.setItem(row, 12, QTableWidgetItem(f"{tx.btc_gain:.6f}"))
            self.table.setItem(row, 13, QTableWidgetItem(f"{tx.gold_gain:.6f}"))
            self.table.setItem(row, 14, QTableWidgetItem(str(tx.timestamp)))
