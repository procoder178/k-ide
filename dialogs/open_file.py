from PyQt5.QtWidgets import QFileDialog
from dialogs.urls import URLS

class OpenFileDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "Open File")
        
        self.setFileMode(QFileDialog.ExistingFile)
        self.setSidebarUrls(URLS)
