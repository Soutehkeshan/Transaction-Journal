import sys
from PyQt5.QtWidgets import QApplication
from GUI.view import TransactionView
from GUI.controller import TransactionController
from GUI.model import TransactionModel

def main():
    app = QApplication(sys.argv)

    model = TransactionModel()
    view = TransactionView()
    controller = TransactionController(model, view)

    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
