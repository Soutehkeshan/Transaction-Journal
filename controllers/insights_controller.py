from PyQt5.QtCore import QObject

class InsightsController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        