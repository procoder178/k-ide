from PyQt5.QtWidgets import QFileDialog
from dialogs.urls import URLS

class OpenFolderDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "Open Folder")
        
        self.setFileMode(QFileDialog.Directory)
        self.setOption(QFileDialog.ShowDirsOnly, True)
        
        self.setSidebarUrls(URLS)
