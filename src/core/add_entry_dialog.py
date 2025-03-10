from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from src.core.storage import add_password
from src.core.encryption import encrypt_data

class AddEntryDialog(QDialog):
    def __init__(self,key,parent=None):
        super().__init__(parent)
        self.key = key
        self.setWindowTitle("Add Entry")
        self.setFixedSize(300, 220)

        layout = QVBoxLayout()
        self.setLayout(layout)

        #site
        self.site_label = QLabel("Site: ")
        self.site_input = QLineEdit()
        layout.addWidget(self.site_label)
        layout.addWidget(self.site_input)

        #username
        self.username_label = QLabel("Username: ")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        #password
        self.password_label = QLabel("Password: ")
        self.password_input = QLineEdit()
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        #save/cancel buttons layout
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        #connect buttons
        self.save_button.clicked.connect(self.save_entry)
        self.cancel_button.clicked.connect(self.reject)

    def save_entry(self):
        site = self.site_input.text().strip()
        username = self.username_input.text().strip()
        plaintext_password = self.password_input.text().strip()

        #cannot be empty
        if not site or not username or not plaintext_password:
            return
        iv, ciphertext = encrypt_data(plaintext_password, self.key)
        add_password(site, username, iv, ciphertext)
        self.accept()



