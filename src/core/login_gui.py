from idlelib import window

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit
from src.core import encryption,storage
from src.core.auth import verify_master_hash, load_master_password_hash, create_master_hash, store_master_hash


def main():
    #create window
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(900, 400, 600, 600)
    window.setFixedSize(500, 350)
    window.setWindowTitle("pyManager")

    #create central widget
    widget = QWidget()
    layout = QVBoxLayout()
    widget.setLayout(layout)
    window.setCentralWidget(widget)

    layout.setAlignment(QtCore.Qt.AlignCenter)

    #pyManager Label
    title_label = QLabel("pyManager")
    title_label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(title_label)


    #create master password field
    password_input = QLineEdit()
    password_input.setEchoMode(QLineEdit.Password) #hide what's being typed
    password_input.setPlaceholderText("Master Password")
    layout.addWidget(password_input)


    #create login button
    login_button = QtWidgets.QPushButton(window)
    login_button.setText("Login")
    layout.addWidget(login_button)
    login_button.hide()

    #create new password button
    create_password_button = QtWidgets.QPushButton(window)
    create_password_button.setText("Create Password")
    layout.addWidget(create_password_button)
    create_password_button.hide()




    # show login button only if password is already created
    stored_hash = load_master_password_hash()
    if(stored_hash is None):
        create_password_button.show()
    else:
        login_button.show()


    #setup password if not already created
    def setup_master_password():
        stored_hash = load_master_password_hash()
        if stored_hash is None:
            master_password = password_input.text()
            hash_value = create_master_hash(master_password)
            store_master_hash(hash_value)
            print("Master Password Set.")
            create_password_button.hide()
            login_button.show()
        else:
            print("Master Password is already set.")

    #handle login logic for button
    def login() -> bool:
        stored_hash = load_master_password_hash()
        input_password = password_input.text()
        if(verify_master_hash(input_password, stored_hash)):
            print("Login Successful")
            #Todo: create gui for password vault
            return True
        else:
            print("Login failed")
            return False

    login_button.clicked.connect(login)
    create_password_button.clicked.connect(setup_master_password)



    window.show()
    sys.exit(app.exec_())