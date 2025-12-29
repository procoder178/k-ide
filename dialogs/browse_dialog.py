from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from qtawesome import icon
import subprocess

class OpenBrowserDialog(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Browse Link")
        self.resize(400, 400)
        
        self.link_box = QLineEdit()
        self.link_box.setFont(QFont("Consolas",15))
        self.link_box.setCursor(Qt.IBeamCursor)
        
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFont(QFont("Consolas",20))
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setIcon(icon("fa5s.globe", color="white"))
        self.browse_btn.setIconSize(QSize(25, 25))
        self.browse_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #FCAF21;
            }
            QPushButton:hover {
                background-color: #FCE221;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_link)
        
        layout = QVBoxLayout()
        layout.addWidget(self.link_box)
        layout.addWidget(self.browse_btn)
        self.setLayout(layout)
        
    def browse_link(self):
        link = self.link_box.text()
        subprocess.Popen(["python3","utils/browser.py",link])
