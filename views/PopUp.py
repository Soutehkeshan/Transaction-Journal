from PyQt5.QtWidgets import QMessageBox

class PopUp:
    @staticmethod
    def show_message(message: str, title: str = "پیام"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    @staticmethod
    def show_warning(message: str, title: str = "هشدار"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.exec_()

    @staticmethod
    def show_error(message: str, title: str = "خطا"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_()