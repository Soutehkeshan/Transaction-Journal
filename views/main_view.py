from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget
from views.transaction_entry_view import TransactionEntryView
from views.insights_view import InsightsView
from views.asset_entry_view import AssetEntryView

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Journal")
        self.setMinimumSize(600, 500)
        
        # Create a central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create navigation buttons
        self.nav_layout = QHBoxLayout()
        self.transactions_button = QPushButton("Transactions")
        self.assets_button = QPushButton("Assets")
        self.insights_button = QPushButton("Insights")
        
        self.nav_layout.addWidget(self.transactions_button)
        self.nav_layout.addWidget(self.assets_button)
        self.nav_layout.addWidget(self.insights_button)
        
        # Create stacked widget to hold different screens
        self.stacked_widget = QStackedWidget()
        self.transaction_view = TransactionEntryView()
        self.asset_entry_view = AssetEntryView()
        self.insights_view = InsightsView()
        
        self.stacked_widget.addWidget(self.transaction_view)
        self.stacked_widget.addWidget(self.asset_entry_view)
        self.stacked_widget.addWidget(self.insights_view)
        
        # Add widgets to main layout
        self.main_layout.addLayout(self.nav_layout)
        self.main_layout.addWidget(self.stacked_widget)
        
        # Connect signals
        self.transactions_button.clicked.connect(self.show_transactions)
        self.assets_button.clicked.connect(self.show_assets)
        self.insights_button.clicked.connect(self.show_insights)
    
    def show_transactions(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_assets(self):
        self.stacked_widget.setCurrentIndex(1)
        
    def show_insights(self):
        self.stacked_widget.setCurrentIndex(2)
    
    # Getter methods to access individual views
    def get_transaction_entry_view(self):
        return self.transaction_view
        
    def get_insights_view(self):
        return self.insights_view
    
    def get_asset_entry_view(self):
        return self.asset_entry_view