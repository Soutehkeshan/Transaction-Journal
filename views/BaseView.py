from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class BaseView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(self.default_stylesheet())

    @staticmethod
    def default_stylesheet():
        return """
        QWidget {
            background-color: #F9F9F9;
            font-size: 10pt;
            color: #333;
            line-height: 1.6;
        }

        QLabel {
            color: #444;
            background-color: #F1F5F9;
            border: 1px solid #DADDE1;
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 12pt;
            font-weight: bold;
            margin-left: 10px;
            margin-bottom: 6px;
            letter-spacing: 0.4px;
        }

        #statusLabel {
            color: #D32F2F;
            font-weight: bold;
            margin-top: 12px;
        }

        QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox {
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 10px;
            background-color: #FFFFFF;
            color: #333;
            min-width: 350px;
        }

         QComboBox {
            min-width: 325px;
        }

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
            border: 1px solid #007ACC;
            outline: none;
        }

        QPushButton {
            background-color: #007ACC;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: bold;
            min-width: 130px;
        }

        QPushButton:hover {
            background-color: #005F99;
        }

        QPushButton:pressed {
            background-color: #004C80;
        }

        QPushButton.SortButton {
            background-color: #6C757D;
            color: white;
            padding: 8px 14px;
            font-size: 9pt;
            min-width: 110px;
            border-radius: 5px;
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
            gridline-color: #EEEEEE;
            font-size: 9pt;
        }

        QHeaderView::section {
            background-color: #E0E5EC;
            color: #333;
            padding: 8px;
            border: 1px solid #D1D5DA;
            font-weight: bold;
            font-size: 9pt;
            text-align: right;
        }

        QTableWidget::item {
            padding: 6px;
            text-align: right;
        }

        QTableWidget::item:selected {
            background-color: #B0D9FF;
            color: #333;
        }

        QCheckBox {
            color: #333;
            spacing: 8px;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 1px solid #999;
            border-radius: 4px;
            background-color: #FFF;
        }

        QCheckBox::indicator:checked {
            background-color: #007ACC;
            border: 1px solid #007ACC;
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: left;
            width: 22px;
            border-left: 1px solid #CCC;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
        }

        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
            width: 22px;
            border-left: 1px solid #CCC;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
        }

            """
    