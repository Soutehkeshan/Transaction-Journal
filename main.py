import sys
from PyQt5.QtWidgets import QApplication
from GUI.main_view import MainView
from GUI.main_controller import MainController
from GUI.model import TransactionModel
from GUI.insights_model import InsightsModel

def main():
    app = QApplication(sys.argv)

    # Initialize models
    transaction_model = TransactionModel()
    insights_model = InsightsModel(transaction_model)
    
    # Initialize main view
    main_view = MainView()
    
    # Initialize main controller
    main_controller = MainController(transaction_model, insights_model, main_view)

    main_view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()