from PyQt6.QtWidgets import QMenu
from PyQt6 import QtGui
from PyQt6.QtCore import QTimer
from random import choice

from ui.ui import Ui_MainWindow


class Slots:
    def __init__(self, ui_obj: Ui_MainWindow):
        self.ui_obj = ui_obj

    def pushButton_get_result_slot(self):

        factory = self.ui_obj.comboBox_factory.currentText()
        start_date = self.ui_obj.comboBox_start_date.currentText()
        end_date = self.ui_obj.comboBox_end_date.currentText()
        self.ui_obj.lineEdit_result.setText(
            f"{factory}, {start_date}, {end_date}, {', '.join([field.text() for field in self.ui_obj.line_edits])}"
        )

    def table_context_menu_slot(self):
        menu = QMenu(self.ui_obj.tableWidget_1)
        add_row_action = menu.addAction("Add row")
        add_row_action.triggered.connect(  # type: ignore
            lambda: self.ui_obj.tableWidget_1.insertRow(self.ui_obj.tableWidget_1.rowCount())
        )
        menu.exec(QtGui.QCursor.pos())

    def add_row(self):
        self.ui_obj.tableWidget_1.insertRow(self.ui_obj.tableWidget_1.rowCount())

    def pushButton_save_changes_to_db_slot(self):
        choice((self.save_changes_to_db_success, self.save_changes_to_db_failure))()

    def save_changes_to_db_success(self):
        self.ui_obj.label_save_changes_to_db_status.setText('БД успішно оновлено')
        timer = QTimer(self.ui_obj)
        timer.setSingleShot(True)
        timer.start(3000)
        self.ui_obj.label_save_changes_to_db_status.setStyleSheet("color: green;")
        timer.timeout.connect(lambda: self.ui_obj.label_save_changes_to_db_status.setText(''))  # type: ignore

    def save_changes_to_db_failure(self):
        self.ui_obj.label_save_changes_to_db_status.setText('При оновленні БД виникла помилка')
        timer = QTimer(self.ui_obj)
        timer.setSingleShot(True)
        timer.start(3000)
        self.ui_obj.label_save_changes_to_db_status.setStyleSheet("color: red;")
        timer.timeout.connect(lambda: self.ui_obj.label_save_changes_to_db_status.setText(''))  # type: ignore
