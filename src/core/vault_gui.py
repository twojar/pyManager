from idlelib import window

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, \
    QPushButton, QTableWidget
from src.core import encryption,storage
from src.core.auth import verify_master_hash, load_master_password_hash, create_master_hash, store_master_hash
from src.core import login_gui

class VaultWindow(QMainWindow):
    def __init__(self):
        #create window
        super().__init__()
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
        layout.addWidget(self.table)

        #button layout
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        #add password button
        self.add_button = QPushButton("Add")
        button_layout.addWidget(self.add_button)

        #remove password button
        self.remove_button = QPushButton("Remove")
        button_layout.addWidget(self.remove_button)

        #logout button
        self.logout_button = QPushButton("Logout")
        button_layout.addWidget(self.logout_button)








