from PyQt5.QtCore import QObject
from GUI.controller import TransactionController
from GUI.insights_controller import InsightsController

class MainController(QObject):
    def __init__(self, transaction_model, insights_model, main_view):
        super().__init__()
        self.transaction_model = transaction_model
        self.insights_model = insights_model
        self.main_view = main_view
        
        # Initialize sub-controllers
        self.transaction_controller = TransactionController(
            self.transaction_model, 
            self.main_view.get_transaction_view()
        )
        
        self.insights_controller = InsightsController(
            self.insights_model,
            self.main_view.get_insights_view()
        )