from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.core import encryption,storage


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(900,400,600,600)
    window.setFixedSize(600,600)
    window.setWindowTitle("pyManager")
    window.size
    window.show()
    sys.exit(app.exec_())

main()