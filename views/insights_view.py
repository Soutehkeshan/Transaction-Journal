from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QLineEdit, QHeaderView, QFrame
)
from PyQt5.QtCore import Qt
from typing import List, Any
from models.asset import Asset
from models.gain import Gain

from views.BaseView import BaseView

class InsightsView(BaseView):
    """
    Provides an interface to view and analyze transaction insights,
    including currency conversion, sorting, and a detailed transaction table.
    """
    def __init__(self):
        super().__init__()

        self._setup_ui()

    def _setup_ui(self):
        """Sets up the layout and widgets for the InsightsView."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15) # Increased spacing between sections
        main_layout.setContentsMargins(20, 20, 20, 20) # Margins around the view

        # --- IRR (USD to IRR) Conversion Section ---
        irr_section_layout = QHBoxLayout()
        irr_section_layout.setAlignment(Qt.AlignRight) # Align content to the right
        irr_section_layout.setSpacing(10)

        self.irr_label = QLabel("قیمت دلار:")
        self.irr_input = QLineEdit()
        self.irr_input.setPlaceholderText("نمونه: 800,000") # Persian example
        self.irr_input.setAlignment(Qt.AlignRight) # Align input text to right

        self.calculate_gains_btn = QPushButton("محاسبه سود") # Persian label

        self.refresh_btn = QPushButton("ریفرش") # Persian label

        # --- Modify Button at the Top ---
        self.modify_btn = QPushButton("ویرایش")

        irr_section_layout.addWidget(self.calculate_gains_btn) # Button on the left in RTL
        irr_section_layout.addWidget(self.irr_label)
        irr_section_layout.addWidget(self.irr_input)
        irr_section_layout.addWidget(self.refresh_btn)
        irr_section_layout.addWidget(self.modify_btn)

        main_layout.addLayout(irr_section_layout)

        # --- Separator below IRR section ---
        separator_irr = QFrame()
        separator_irr.setFrameShape(QFrame.HLine)
        separator_irr.setFrameShadow(QFrame.Sunken)
        separator_irr.setStyleSheet("color: #E0E0E0;")
        main_layout.addWidget(separator_irr)

        # --- Sorting Buttons Section ---
        sorting_buttons_vlayout = QVBoxLayout()
        sorting_buttons_vlayout.setSpacing(8) # Spacing between rows of buttons
        sorting_buttons_vlayout.setAlignment(Qt.AlignRight) # Align button groups to the right

        # --- Separator below Sorting buttons ---
        separator_sort = QFrame()
        separator_sort.setFrameShape(QFrame.HLine)
        separator_sort.setFrameShadow(QFrame.Sunken)
        separator_sort.setStyleSheet("color: #E0E0E0;")
        main_layout.addWidget(separator_sort)

        # --- Transactions Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(13)
        
        # Set Persian Horizontal Header Labels
        self.table.setHorizontalHeaderLabels([
            "نماد", "نوع", "تعداد", "قیمت واحد", "جمع کل",
            "قیمت طلا", "قیمت دلار", "یادداشت",
            "آخرین قیمت دارایی", "سود ریالی",
            "سود دلاری", "سود طلایی", "تاریخ و زمان"
        ])

        # Adjust header behavior: Stretch last section, enable sorting click
        header = self.table.horizontalHeader()
        # Allow manual resizing of all columns
        header.setSectionResizeMode(QHeaderView.Interactive)

        # Let the user rearrange columns (optional)
        header.setSectionsMovable(True)

        # Set default widths to ensure datetime and important fields have space
        column_widths = {
            1: 60,    # نوع
            2: 80,    # تعداد
            3: 100,   # قیمت واحد
            4: 100,   # جمع کل
            5: 90,    # قیمت طلا
            6: 90,    # قیمت دلار
            7: 180,   # یادداشت
            8: 100,   # آخرین قیمت دارایی
            9: 80,    # سود ریالی
            10: 80,    # سود دلاری
            11: 80,   # سود طلایی
            12: 160   # تاریخ و زمان (give more space here)
        }
        for col, width in column_widths.items():
            self.table.setColumnWidth(col, width)

        header.setStretchLastSection(True)

        # Align header text to right
        header.setDefaultAlignment(Qt.AlignRight)
        
        self.table.verticalHeader().setVisible(False) # Hide vertical header (row numbers)
        self.table.setAlternatingRowColors(True) # Enable alternating row colors for readability
        self.table.setSelectionBehavior(QTableWidget.SelectRows) # Select entire rows
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) # Make table read-only
        self.table.setSortingEnabled(True)

        main_layout.addWidget(self.table)

    def update_table(self, transactions: List[Any]):  # Use Any if 'tx' is not a specific type yet
        """
        Populates the table with transaction data and associated gains from the gains table.
        """
        self._transactions = transactions  # Save for later access
        self.table.setRowCount(len(transactions))
        for row, tx in enumerate(transactions):
            total_value = tx.amount * tx.price_per_unit
            # Ensure Asset.get_by_id is correctly implemented in your models
            asset_symbol = Asset.get_by_id(tx.asset_id).symbol if hasattr(tx, 'asset_id') and Asset else "N/A"

            # Retrieve associated gain using the Gain model
            gain = Gain.get_by_transaction_id(tx.id)

            latest_asset_price = gain.latest_asset_price if gain else 0.0
            irr_gain = gain.irr_gain if gain else 0
            usd_gain = gain.usd_gain if gain else 0
            gold_gain = gain.gold_gain if gain else 0

            self.table.setItem(row, 0, QTableWidgetItem(asset_symbol))
            self.table.setItem(row, 1, QTableWidgetItem(tx.type))
            self.table.setItem(row, 2, QTableWidgetItem(f"{tx.amount:.5f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{tx.price_per_unit:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{total_value:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{tx.gold_price:.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{tx.dollar_price:.2f}"))
            self.table.setItem(row, 7, QTableWidgetItem(tx.note))
            self.table.setItem(row, 8, QTableWidgetItem(f"{latest_asset_price:.2f}"))
            self.table.setItem(row, 9, QTableWidgetItem(f"{irr_gain:.2f}"))
            self.table.setItem(row, 10, QTableWidgetItem(f"{usd_gain:.2f}"))
            self.table.setItem(row, 11, QTableWidgetItem(f"{gold_gain:.2f}"))
            self.table.setItem(row, 12, QTableWidgetItem(str(tx.timestamp)))

            # Align content of each cell to the right
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
