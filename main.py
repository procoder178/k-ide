import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from qdarktheme import load_stylesheet as ls
from window import MainWindow

app = QApplication(sys.argv)
app.setStyleSheet(ls("dark"))
win = MainWindow()
win.show()
sys.exit(app.exec())
