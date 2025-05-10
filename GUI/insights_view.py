from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QComboBox, QDateEdit, QGridLayout, QGroupBox
)
from PyQt5.QtCore import QDate, pyqtSignal

class InsightsView(QWidget):
    refresh_prices_signal = pyqtSignal()
    generate_graph_signal = pyqtSignal(str, QDate, QDate)
    
    def __init__(self):
        super().__init__()
        
        # Main layout
        self.layout = QVBoxLayout(self)
        
        # Current prices section
        self.prices_group = QGroupBox("Current Market Prices")
        prices_layout = QGridLayout()
        
        self.gold_price_label = QLabel("Gold: $0.00")
        self.btc_price_label = QLabel("BTC: $0.00")
        self.last_updated_label = QLabel("Last updated: Never")
        self.refresh_button = QPushButton("Refresh Prices")
        
        prices_layout.addWidget(QLabel("Gold Price:"), 0, 0)
        prices_layout.addWidget(self.gold_price_label, 0, 1)
        prices_layout.addWidget(QLabel("Bitcoin Price:"), 1, 0)
        prices_layout.addWidget(self.btc_price_label, 1, 1)
        prices_layout.addWidget(self.last_updated_label, 2, 0, 1, 2)
        prices_layout.addWidget(self.refresh_button, 3, 0, 1, 2)
        
        self.prices_group.setLayout(prices_layout)
        
        # Graph options section
        self.graph_group = QGroupBox("Generate Graphs")
        graph_layout = QVBoxLayout()
        
        # Graph type selection
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Graph Type:"))
        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems([
            "Portfolio Value Over Time", 
            "Asset Distribution", 
            "Profit/Loss Analysis",
            "Transaction History"
        ])
        type_layout.addWidget(self.graph_type_combo)
        
        # Date range selection
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date Range:"))
        
        self.from_date = QDateEdit(QDate.currentDate().addMonths(-1))
        self.to_date = QDateEdit(QDate.currentDate())
        self.from_date.setCalendarPopup(True)
        self.to_date.setCalendarPopup(True)
        
        date_layout.addWidget(QLabel("From:"))
        date_layout.addWidget(self.from_date)
        date_layout.addWidget(QLabel("To:"))
        date_layout.addWidget(self.to_date)
        
        # Generate button
        self.generate_button = QPushButton("Generate Graph")
        
        graph_layout.addLayout(type_layout)
        graph_layout.addLayout(date_layout)
        graph_layout.addWidget(self.generate_button)
        
        self.graph_group.setLayout(graph_layout)
        
        # Status section
        self.status_label = QLabel("")
        
        # Add all sections to main layout
        self.layout.addWidget(self.prices_group)
        self.layout.addWidget(self.graph_group)
        self.layout.addWidget(self.status_label)
        
        # Connect signals
        self.refresh_button.clicked.connect(self.refresh_prices_signal.emit)
        self.generate_button.clicked.connect(self.on_generate_graph)
    
    def on_generate_graph(self):
        graph_type = self.graph_type_combo.currentText()
        from_date = self.from_date.date()
        to_date = self.to_date.date()
        self.generate_graph_signal.emit(graph_type, from_date, to_date)
    
    def update_prices(self, gold_price, btc_price, timestamp):
        self.gold_price_label.setText(f"${gold_price:.2f}")
        self.btc_price_label.setText(f"${btc_price:.2f}")
        self.last_updated_label.setText(f"Last updated: {timestamp}")
    
    def set_status(self, message):
        self.status_label.setText(message)