from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout

class AssetEntryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Asset")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.symbol_input = QLineEdit()
        self.data_source_input = QLineEdit()
        self.source_symbol_input = QLineEdit()

        form_layout.addRow("Symbol:", self.symbol_input)
        form_layout.addRow("Data Source:", self.data_source_input)
        form_layout.addRow("Source Symbol:", self.source_symbol_input)

        self.add_button = QPushButton("Add Asset")
        self.status_label = QLabel()

        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def clear_inputs(self):
        self.symbol_input.clear()
        self.data_source_input.clear()
        self.source_symbol_input.clear()