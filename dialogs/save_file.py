from PyQt5.QtWidgets import QFileDialog
from dialogs.urls import URLS

class SaveFileDialog(QFileDialog):
    def __init__(self, parent=None, title="Save File"):
        super().__init__(parent, title)
        
        self.setAcceptMode(QFileDialog.AcceptSave)
        self.setFileMode(QFileDialog.AnyFile)
        
        self.setSidebarUrls(URLS)
