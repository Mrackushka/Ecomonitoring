import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from logic.slots import Slots
from ui.ui import Ui_MainWindow
from logic.database import DB

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('ui/styles/toolery.qss') as style:
        app.setStyleSheet(style.read())
    MainWindow = QMainWindow()
    ui = Ui_MainWindow(MainWindow, Slots, DB)
    MainWindow.show()
    sys.exit(app.exec())
