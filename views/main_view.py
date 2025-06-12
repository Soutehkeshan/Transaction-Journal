from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QStackedWidget, QFrame
)
from PyQt5.QtCore import Qt
from views.transaction_entry_view import TransactionEntryView
from views.insights_view import InsightsView


class MainView(QMainWindow):
    """
    Main application window managing different views (Transaction Entry, Insights).
    This class sets up the main layout, navigation, and overall styling.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("دفترچه تراکنش") # Set window title in Persian
        self.resize(1300, 750)
        self.setLayoutDirection(Qt.RightToLeft) # Set main window layout direction to RTL

        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """
        Sets up the central widget, main layout, navigation buttons,
        and the stacked widget for managing different application screens.
        """
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.nav_layout = QHBoxLayout()
        self.nav_layout.setContentsMargins(20, 15, 20, 15)
        self.nav_layout.setSpacing(15)
        self.nav_layout.setAlignment(Qt.AlignCenter)

        self.transactions_button = QPushButton("ثبت تراکنش")
        self.transactions_button.setObjectName("navButton")
        self.transactions_button.setCheckable(True)
        self.transactions_button.setChecked(True) # Default to Transactions view
        
        self.insights_button = QPushButton("گزارش‌ها")
        self.insights_button.setObjectName("navButton")
        self.insights_button.setCheckable(True)

        self.nav_layout.addWidget(self.transactions_button)
        self.nav_layout.addWidget(self.insights_button)

        self.nav_separator = QFrame()
        self.nav_separator.setFrameShape(QFrame.HLine)
        self.nav_separator.setFrameShadow(QFrame.Sunken)
        self.nav_separator.setStyleSheet("color: #E0E0E0;")

        self.stacked_widget = QStackedWidget()
        self.transaction_view = TransactionEntryView()
        self.insights_view = InsightsView()
        
        self.stacked_widget.addWidget(self.transaction_view) # Index 0
        self.stacked_widget.addWidget(self.insights_view) # Index 1
        
        self.main_layout.addLayout(self.nav_layout)
        self.main_layout.addWidget(self.nav_separator)
        self.main_layout.addWidget(self.stacked_widget)

        self._apply_styles()

    def _setup_connections(self):
        """
        Connects signals from buttons to their respective slot methods.
        """
        # Connect clicked signals to a lambda that updates view and button state
        self.transactions_button.clicked.connect(lambda: self._set_current_view(0))
        self.insights_button.clicked.connect(lambda: self._set_current_view(1))

        # Use button groups or manual state management for checkable buttons
        # For simplicity, we'll manually manage the check state for now
        self.transactions_button.clicked.connect(lambda: self._update_nav_button_state(self.transactions_button))
        self.insights_button.clicked.connect(lambda: self._update_nav_button_state(self.insights_button))


    def _set_current_view(self, index: int):
        """
        Sets the current visible widget in the stacked widget.
        """
        self.stacked_widget.setCurrentIndex(index)

    def _update_nav_button_state(self, clicked_button: QPushButton):
        """
        Updates the checked state of navigation buttons to ensure only one is active.
        """
        # Ensure only the clicked button is checked, and others are unchecked
        for button in [self.transactions_button, self.insights_button]:
            if button is clicked_button:
                button.setChecked(True)
            else:
                button.setChecked(False)

    def _apply_styles(self):
        """
        Applies consistent QSS styling to the QMainWindow and its child widgets.
        """
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F2F5; /* Light background for the main window */
            }
            QPushButton {
                font-size: 10pt;
                padding: 10px 15px;
                border-radius: 8px; /* Slightly more rounded corners */
                background-color: #E0E5EC; /* Light gray background */
                color: #333333;
                border: none;
                /* Removed: transition: background-color 0.3s ease; */
            }
            QPushButton:hover {
                background-color: #D1D5DA; /* Darker on hover */
            }

            /* Specific styling for navigation buttons using their objectName */
            QPushButton#navButton {
                font-size: 11pt;
                font-weight: bold;
                padding: 12px 25px; /* More padding for navigation */
                border-radius: 8px;
                background-color: #E0E5EC;
                color: #555555;
                min-width: 150px; /* Ensure buttons have a minimum width */
                border: 1px solid #DCDCDC; /* Subtle border */
                /* Removed: transition: background-color 0.3s ease; */
            }
            QPushButton#navButton:hover {
                background-color: #D1D5DA;
                border-color: #C0C0C0;
            }
            QPushButton#navButton:checked { /* Style for the active/checked navigation button */
                background-color: #007ACC; /* Blue for active state */
                color: white;
                border: 1px solid #007ACC;
            }
            QPushButton#navButton:checked:hover {
                background-color: #005F99;
            }

            /* Styling for the QStackedWidget content area */
            QStackedWidget {
                background-color: #FFFFFF; /* White background for the content area */
                border: 1px solid #E0E0E0;
                border-radius: 10px; /* Rounded corners for the content area */
                margin: 20px; /* Margin around the stacked widget to give it space from edges */
                padding: 0px; /* No internal padding, views handle their own */
            }
            /* Style the central widget to match the general background if needed */
            QWidget#centralWidget {
                background-color: #F0F2F5;
            }
        """)

    # Getter methods to access individual views
    def get_transaction_entry_view(self) -> TransactionEntryView:
        """Returns the TransactionEntryView instance."""
        return self.transaction_view
        
    def get_insights_view(self) -> InsightsView:
        """Returns the InsightsView instance."""
        return self.insights_view
    