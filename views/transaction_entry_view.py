from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QTextEdit, QCompleter, QCheckBox, QFormLayout,
    QFrame
)
from PyQt5.QtCore import QStringListModel, pyqtSignal, Qt
import jdatetime

from views.BaseView import BaseView

class TransactionEntryView(BaseView):
    submitted = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ثبت تراکنش جدید")

        self.init_inputs()
        self.init_layout()
        self.init_connections()

    def init_inputs(self):
        # Symbol input with autocompletion
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("نماد سهام (مثلاً: پارسیان)")
        self.symbol_input.setAlignment(Qt.AlignRight)

        self.symbol_model = QStringListModel()
        self.symbol_completer = QCompleter(self.symbol_model)
        self.symbol_completer.setCaseSensitivity(False)
        self.symbol_input.setCompleter(self.symbol_completer)

        self.type_input = QComboBox()
        self.type_input.addItems(["خرید", "فروش"])
        self.type_input.setEditable(False)
        self.type_input.setLayoutDirection(Qt.RightToLeft)
        self.type_input.setStyleSheet("QComboBox { text-align: right; }") # Align text in combobox

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("مثلاً: 100")
        self.amount_input.setAlignment(Qt.AlignRight)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("مثلاً: 2500")
        self.price_input.setAlignment(Qt.AlignRight)

        self.equilibrium_price_input = QLineEdit()
        self.equilibrium_price_input.setPlaceholderText("مثلاً: 2400")
        self.equilibrium_price_input.setAlignment(Qt.AlignRight)

        self.equilibrium_price_date_input = QLineEdit()
        now_jalali = jdatetime.datetime.now().date()
        self.equilibrium_price_date_input.setText(now_jalali.strftime('%Y-%m-%d'))
        self.equilibrium_price_date_input.setPlaceholderText("تاریخ شمسی (مثلاً: 1403-03-00)")
        self.equilibrium_price_date_input.setAlignment(Qt.AlignRight)
        self.equilibrium_price_date_input.setMinimumWidth(350) # Increased width

        self.equilibrium_price_now_checkbox = QCheckBox("استفاده از زمان فعلی")
        self.equilibrium_price_now_checkbox.setChecked(True)
        self.equilibrium_price_now_checkbox.setLayoutDirection(Qt.RightToLeft)
        self.equilibrium_price_date_input.setEnabled(False)

        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText("توضیح اختیاری...")
        self.note_input.setAlignment(Qt.AlignRight)
        self.note_input.setMinimumHeight(100) # Increased height for more space

        self.date_input = QLineEdit()
        now_jalali = jdatetime.datetime.now()
        self.date_input.setText(now_jalali.strftime('%Y-%m-%d %H:%M:%S'))
        self.date_input.setPlaceholderText("تاریخ شمسی (مثلاً: 1403-03-16 17:45:00)")
        self.date_input.setAlignment(Qt.AlignRight)
        self.date_input.setMinimumWidth(350) # Increased width

        self.now_checkbox = QCheckBox("استفاده از زمان فعلی")
        self.now_checkbox.setChecked(True)
        self.now_checkbox.setLayoutDirection(Qt.RightToLeft)
        self.date_input.setEnabled(False)

        self.use_market_price_checkbox = QCheckBox("استفاده از قیمت لحظه‌ای طلا")
        self.use_market_price_checkbox.setChecked(True)
        self.use_market_price_checkbox.setLayoutDirection(Qt.RightToLeft)

        self.gold_price_input = QLineEdit()
        self.gold_price_input.setEnabled(False)
        self.gold_price_input.setAlignment(Qt.AlignRight)

        self.dollar_price_input = QLineEdit()
        self.dollar_price_input.setAlignment(Qt.AlignRight)

        self.submit_button = QPushButton("ثبت تراکنش") # More descriptive text

    def init_layout(self):
        # Overall main layout to center the content
        overall_vlayout = QVBoxLayout(self)
        overall_vlayout.setContentsMargins(0, 0, 0, 0) # No extra margins for overall layout

        # A horizontal layout to push the main content to the center
        center_hlayout = QHBoxLayout()
        center_hlayout.addStretch(1) # Pushes content to the right
        
        main_content_vlayout = QVBoxLayout()
        main_content_vlayout.setSpacing(15) # Increased spacing
        main_content_vlayout.setContentsMargins(30, 30, 30, 30) # Increased margins for the content itself
        main_content_vlayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop) # Align content horizontally center

        # Form layout for inputs
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignRight | Qt.AlignTop) # Align form to top for textedit
        form_layout.setSpacing(12) # Increased spacing in form
        form_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)

        # Added QLabel wrappers for better styling consistency
        form_layout.addRow(QLabel("نماد سهام:"), self.symbol_input)
        form_layout.addRow(QLabel("نوع تراکنش:"), self.type_input)
        form_layout.addRow(QLabel("تعداد:"), self.amount_input)
        form_layout.addRow(QLabel("قیمت واحد:"), self.price_input)
        form_layout.addRow(QLabel("قیمت تعادلی:"), self.equilibrium_price_input)

        # Date input and checkbox in a horizontal layout
        date_hbox = QHBoxLayout()
        date_hbox.addWidget(self.equilibrium_price_date_input)
        date_hbox.addWidget(self.equilibrium_price_now_checkbox)
        date_hbox.addStretch(1) # Pushes the checkbox and input to the right
        date_hbox.setAlignment(Qt.AlignRight)
        form_layout.addRow(QLabel("تاریخ:"), date_hbox)
        
        form_layout.addRow(QLabel("یادداشت:"), self.note_input)

        # Date input and checkbox in a horizontal layout
        date_hbox = QHBoxLayout()
        date_hbox.addWidget(self.date_input)
        date_hbox.addWidget(self.now_checkbox)
        date_hbox.addStretch(1) # Pushes the checkbox and input to the right
        date_hbox.setAlignment(Qt.AlignRight)
        form_layout.addRow(QLabel("تاریخ:"), date_hbox)

        # Gold price section in a horizontal layout
        gold_hbox = QHBoxLayout()
        gold_hbox.addWidget(self.gold_price_input)
        gold_hbox.addWidget(self.use_market_price_checkbox)
        gold_hbox.addStretch(1)
        gold_hbox.setAlignment(Qt.AlignRight)
        form_layout.addRow(QLabel("قیمت طلا:"), gold_hbox)

        # Dollar price section in a horizontal layout
        dollar_hbox = QHBoxLayout()
        dollar_hbox.addWidget(self.dollar_price_input)
        dollar_hbox.addStretch(1)
        dollar_hbox.setAlignment(Qt.AlignRight)
        form_layout.addRow(QLabel("قیمت دلار:"), dollar_hbox)

        # Add a separator line (optional, but good for visual separation)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #E0E0E0;") # Lighter separator color

        # Add form layout and other widgets to the main content layout
        main_content_vlayout.addLayout(form_layout)
        main_content_vlayout.addSpacing(15)

        # Button and status in their own vertical sub-layout to place status below button
        button_and_status_vlayout = QVBoxLayout()
        button_and_status_vlayout.setAlignment(Qt.AlignHCenter) # Center the button and status horizontally
        button_and_status_vlayout.addWidget(self.submit_button)
        
        main_content_vlayout.addLayout(button_and_status_vlayout)
        main_content_vlayout.addStretch(1) # Pushes content to top

        center_hlayout.addLayout(main_content_vlayout)
        center_hlayout.addStretch(1) # Pushes content to the left (balancing the first stretch)

        overall_vlayout.addLayout(center_hlayout)
        overall_vlayout.addStretch(1) # Pushes content to the top (vertically centering)

        self.setLayout(overall_vlayout)


    def init_connections(self):
        self.now_checkbox.stateChanged.connect(self.toggle_date_input)
        self.use_market_price_checkbox.stateChanged.connect(self.toggle_price_inputs)
        self.submit_button.clicked.connect(self.submitted.emit)
        self.equilibrium_price_now_checkbox.stateChanged.connect(self.toggle_equilibrium_date_input)

    def toggle_date_input(self, state):
        self.date_input.setEnabled(not state)
        if state:
            self.date_input.setText(jdatetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def toggle_price_inputs(self, state):
        self.gold_price_input.setEnabled(not state)

    def toggle_equilibrium_date_input(self, state):
        self.equilibrium_price_date_input.setEnabled(not state)
        if state:
            self.equilibrium_price_date_input.setText(jdatetime.datetime.now().strftime('%Y-%m-%d'))


    def reset_form(self):
        self.symbol_input.clear()
        self.amount_input.clear()
        self.price_input.clear()
        self.equilibrium_price_input.clear()
        self.note_input.clear()
        self.dollar_price_input.clear()
        self.gold_price_input.clear()

        # Reset checkboxes
        self.now_checkbox.setChecked(True)
        self.equilibrium_price_now_checkbox.setChecked(True)
        self.use_market_price_checkbox.setChecked(True)

        # Reset dates
        self.date_input.setText(jdatetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.equilibrium_price_date_input.setText(jdatetime.datetime.now().strftime('%Y-%m-%d'))

        # Reset dropdown
        self.type_input.setCurrentIndex(0)
