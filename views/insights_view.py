from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

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
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Asset", "Amount", "Price per Unit", "Total",
            "Gain", "BTC Gain", "Gold Gain", "DateTime"
        ])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update_table(self, transactions):
        self.table.setRowCount(len(transactions))
        for row, tx in enumerate(transactions):
            total_value = tx.amount * tx.price_per_unit
            self.table.setItem(row, 0, QTableWidgetItem(str(tx.asset_id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(tx.amount)))
            self.table.setItem(row, 2, QTableWidgetItem(str(tx.price_per_unit)))
            self.table.setItem(row, 3, QTableWidgetItem(f"{total_value:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{tx.gain:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{tx.btc_gain:.6f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{tx.gold_gain:.6f}"))
            self.table.setItem(row, 7, QTableWidgetItem(str(tx.timestamp)))
