from idlelib import window

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit
from src.core import encryption,storage
from src.core.auth import verify_master_hash, load_master_password_hash, create_master_hash, store_master_hash
from src.core import login_gui

class VaultWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pyManager Vault")
        self.setGeometry(900,400,600,400)


