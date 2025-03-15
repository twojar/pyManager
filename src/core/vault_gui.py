from idlelib import window

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, \
    QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView



import src.core.storage
from src.core import encryption,storage
from src.core.add_entry_dialog import AddEntryDialog
from src.core.auth import verify_master_hash, load_master_password_hash, create_master_hash, store_master_hash
from src.core import login_gui
from src.core.storage import remove_password

class VaultWindow(QMainWindow):
    def __init__(self, key:bytes):
        #create window
        super().__init__()
        self.key = key
        self.setWindowTitle("pyManager")
        self.setGeometry(900,400,600,400)
        self.setFixedSize(600,400)

        #central widget and layout
        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #Title Label
        self.title_label = QLabel("pyManager Vault")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title_label)

        #table for password entries
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Site","Username", "Password"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.table)

        #button layout
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        #add password button
        self.add_button = QPushButton("Add")
        button_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.handle_add_entry)

        #remove password button
        self.remove_button = QPushButton("Remove")
        button_layout.addWidget(self.remove_button)
        self.remove_button.clicked.connect(self.handle_remove)

        #logout button
        self.logout_button = QPushButton("Logout")
        button_layout.addWidget(self.logout_button)

        self.load_passwords()

    def load_passwords(self):
        from src.core.storage import get_all_passwords
        entries = get_all_passwords(self.key)
        self.table.setRowCount(len(entries))

        for row_index, entry in enumerate(entries):
            #create table items
            site_item = QTableWidgetItem(entry["site"])
            #store record id in UserRole data for later retrieval
            site_item.setData(QtCore.Qt.UserRole, entry["id"])
            user_item = QTableWidgetItem(entry["username"])
            pass_item = QTableWidgetItem(entry["password"])

            #put items in table
            self.table.setItem(row_index, 0, site_item)
            self.table.setItem(row_index, 1, user_item)
            self.table.setItem(row_index, 2, pass_item)


    def handle_add_entry(self):
        dialog = AddEntryDialog(self.key,self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_passwords()

    def handle_remove(self):
        selected_row = self.table.currentRow()
        if selected_row:
            return
        id_item = self.table.item(selected_row,0)
        if id_item is None:
            return
        record_id = id_item.data(QtCore.Qt.UserRole)
        if record_id is None:
            return
        remove_password(record_id)
        self.load_passwords()














