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
    