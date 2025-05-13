from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QComboBox, QDateEdit, QGridLayout, QGroupBox
)
from PyQt5.QtCore import QDate, pyqtSignal

class InsightsView(QWidget):
    refresh_prices_signal = pyqtSignal()
    generate_graph_signal = pyqtSignal(str, QDate, QDate)
    calculate_gains_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create and add the Calculate Gains button
        self.calculate_gains_btn = QPushButton("Calculate Gains")
        layout.addWidget(self.calculate_gains_btn)

        # Connect button signal to custom signal
        self.calculate_gains_btn.clicked.connect(self.calculate_gains_signal.emit)

        self.setLayout(layout)
