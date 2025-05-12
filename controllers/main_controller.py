from PyQt5.QtCore import QObject
from controllers.transaction_entry_controller import TransactionEntryController
from controllers.insights_controller import InsightsController
from controllers.asset_entry_controller import AssetEntryController
from views.main_view import MainView

class MainController(QObject):
    def __init__(self):
        super().__init__()

        # Initialize the main view
        self.main_view = MainView()
        
        # Initialize sub-controllers
        self.transaction_entry_page_controller = TransactionEntryController(
            self.main_view.get_transaction_entry_view()
        )
        
        self.insights_controller = InsightsController(
            self.main_view.get_insights_view()
        )

        self.asset_entry_controller = AssetEntryController(
            self.main_view.get_asset_entry_view()
        )

    def show(self):
        self.main_view.show()