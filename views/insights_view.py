from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QLineEdit, QHeaderView, QFrame
)
from PyQt5.QtCore import Qt
from typing import List, Any
from models.asset import Asset

class InsightsView(QWidget):
    """
    Provides an interface to view and analyze transaction insights,
    including currency conversion, sorting, and a detailed transaction table.
    """
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.RightToLeft) # Set layout direction for the widget
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F8F8;
                font-family: "Segoe UI", "Tahoma", "Arial", "B Nazanin", "IRANSans";
                font-size: 10pt;
                color: #333333;
            }
            QLabel {
                font-weight: bold;
                color: #4A4A4A;
                padding: 5px 0;
            }
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 8px;
                background-color: #FFFFFF;
                color: #333333;
                min-width: 150px; /* Adjust width as needed */
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #005F99;
            }
            QPushButton:pressed {
                background-color: #004C80;
            }
            /* Styling for sorting buttons specifically */
            QPushButton.SortButton { /* Using a class-like selector */
                background-color: #6C757D; /* Grey background for sorting buttons */
                color: white;
                padding: 8px 12px;
                font-size: 9pt;
                min-width: 100px;
            }
            QPushButton.SortButton:hover {
                background-color: #5A6268;
            }
            QPushButton.SortButton:pressed {
                background-color: #495057;
            }
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #EEEEEE; /* Lighter grid lines */
                font-size: 9pt;
            }
            QHeaderView::section {
                background-color: #E0E5EC; /* Header background color */
                color: #333333;
                padding: 8px;
                border: 1px solid #D1D5DA;
                font-weight: bold;
                font-size: 9pt;
                text-align: right; /* Align header text to right for RTL */
            }
            QTableWidget::item {
                padding: 5px;
                text-align: right; /* Align item text to right for RTL */
            }
            QTableWidget::item:selected {
                background-color: #B0D9FF; /* Light blue on selection */
                color: #333333;
            }
        """)

        self._setup_ui() # Encapsulate UI setup
        self._setup_connections() # Encapsulate connections

    def _setup_ui(self):
        """Sets up the layout and widgets for the InsightsView."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15) # Increased spacing between sections
        main_layout.setContentsMargins(20, 20, 20, 20) # Margins around the view

        # --- IRR (USD to IRR) Conversion Section ---
        irr_section_layout = QHBoxLayout()
        irr_section_layout.setAlignment(Qt.AlignRight) # Align content to the right
        irr_section_layout.setSpacing(10)

        self.irr_label = QLabel("نرخ دلار به ریال (USD/IRR):")
        self.irr_input = QLineEdit()
        self.irr_input.setPlaceholderText("مثال: 800,000") # Persian example
        self.irr_input.setAlignment(Qt.AlignRight) # Align input text to right

        self.calculate_gains_btn = QPushButton("محاسبه سود") # Persian label

        self.refresh_btn = QPushButton("ریفرش") # Persian label

        irr_section_layout.addWidget(self.calculate_gains_btn) # Button on the left in RTL
        irr_section_layout.addWidget(self.irr_label)
        irr_section_layout.addWidget(self.irr_input)
        irr_section_layout.addWidget(self.refresh_btn)

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
        self.table.setColumnCount(11)
        
        # Set Persian Horizontal Header Labels
        self.table.setHorizontalHeaderLabels([
            "نماد", "نوع", "تعداد", "قیمت واحد", "جمع کل",
            "قیمت طلا", "قیمت دلار", "یادداشت",
            "سود ریالی", "سود دلاری", "تاریخ و زمان"
        ])

        # Adjust header behavior: Stretch last section, enable sorting click
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch) # Make columns fill available space
        header.setStretchLastSection(True) # Ensure the last column stretches to fill
        header.setDefaultAlignment(Qt.AlignRight) # Default alignment for headers
        
        self.table.verticalHeader().setVisible(False) # Hide vertical header (row numbers)
        self.table.setAlternatingRowColors(True) # Enable alternating row colors for readability
        self.table.setSelectionBehavior(QTableWidget.SelectRows) # Select entire rows
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) # Make table read-only
        self.table.setSortingEnabled(True)

        main_layout.addWidget(self.table)
    
    def _setup_connections(self):
        """Sets up connections for buttons (implementation will be in controller)."""
        # Connect buttons to placeholder methods or signals to be handled by controller
        self.calculate_gains_btn.clicked.connect(lambda: print("Calculate Gains clicked"))


    def update_table(self, transactions: List[Any]): # Use Any if 'tx' is not a specific type yet
        """
        Populates the table with transaction data.
        Assumes 'transactions' is a list of objects with attributes like tx.amount, tx.price_per_unit, etc.
        """
        self.table.setRowCount(len(transactions))
        for row, tx in enumerate(transactions):
            total_value = tx.amount * tx.price_per_unit
            # Ensure Asset.get_by_id is correctly implemented in your models
            asset_symbol = Asset.get_by_id(tx.asset_id).symbol if hasattr(tx, 'asset_id') and Asset else "N/A"

            self.table.setItem(row, 0, QTableWidgetItem(asset_symbol))
            self.table.setItem(row, 1, QTableWidgetItem(tx.type))
            self.table.setItem(row, 2, QTableWidgetItem(f"{tx.amount:.5f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{tx.price_per_unit:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{total_value:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{tx.gold_price}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{tx.dollar_price}"))
            self.table.setItem(row, 7, QTableWidgetItem(tx.note))
            self.table.setItem(row, 8, QTableWidgetItem(f"{tx.gain:.2f}"))
            self.table.setItem(row, 9, QTableWidgetItem(f"{tx.gold_gain:.6f}"))
            self.table.setItem(row, 10, QTableWidgetItem(str(tx.timestamp)))

            # Align content of each cell to the right
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
