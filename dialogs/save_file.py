from PyQt5.QtWidgets import QFileDialog
from dialogs.urls import URLS

class SaveFileDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "Save File")
        
        self.setAcceptMode(QFileDialog.AcceptSave)
        self.setFileMode(QFileDialog.AnyFile)
        
        self.setSidebarUrls(URLS)
