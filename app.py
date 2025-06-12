import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)

    # Load custom Persian font
    font_id = QFontDatabase.addApplicationFont("resources/fonts/Far_Nazanin.ttf")
    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            app.setFont(QFont(families[0]))
    
    # Initialize main controller
    main_controller = MainController()

    main_controller.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()