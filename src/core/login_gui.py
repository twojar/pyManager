import os
from idlelib import window

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit
from src.core.auth import verify_master_hash, load_master_password_hash, create_master_hash, store_master_hash, \
    store_salt, load_salt
from src.core.encryption import derive_key
from src.core.vault_gui import VaultWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(900, 400, 600, 600)
        self.setFixedSize(500, 350)
        self.setWindowTitle("pyManager")

        #create central widget
        widget = QWidget()
        self.layout = QVBoxLayout()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

        #pyManager Label
        self.title_label = QLabel("pyManager Login")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title_label)


        #create master password field
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password) #hide what's being typed
        self.password_input.setPlaceholderText("Master Password")
        self.layout.addWidget(self.password_input)


        #create login button
        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setText("Login")
        self.layout.addWidget(self.login_button)
        self.login_button.hide()

        #create new password button
        self.create_password_button = QtWidgets.QPushButton(self)
        self.create_password_button.setText("Create Password")
        self.layout.addWidget(self.create_password_button)
        self.create_password_button.hide()




        # show login button only if password is already created
        self.stored_hash = load_master_password_hash()
        if(self.stored_hash is None):
            self.create_password_button.show()
        else:
            self.login_button.show()

        #connect button logic
        self.login_button.clicked.connect(self.login)
        self.create_password_button.clicked.connect(self.setup_master_password)

    #setup password if not already created
    def setup_master_password(self):
        stored_hash = load_master_password_hash()
        if stored_hash is None:
            master_password = self.password_input.text()
            hash_value = create_master_hash(master_password)
            store_master_hash(hash_value)
            salt = os.urandom(16)
            store_salt(salt)
            print("Master Password Set.")
            self.create_password_button.hide()
            self.login_button.show()
        else:
            print("Master Password is already set.")

    #handle login logic for button
    def login(self):
        stored_hash = load_master_password_hash()
        input_password = self.password_input.text()
        if(verify_master_hash(input_password, stored_hash)):
            print("Login Successful")
            self.open_vault_window()
        else:
            print("Login failed")

    #logic for opening vault window
    def open_vault_window(self):
        salt = load_salt()
        master_password = self.password_input.text()
        key = derive_key(master_password, salt)
        self._vault_window = VaultWindow(key)
        self._vault_window.show()
        self.close()
