import os
import sys

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
os.environ["QT_QUICK_BACKEND"] = "software"

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)

app = QApplication(sys.argv)

view = QWebEngineView()
view.setWindowTitle("K-Web Browser")
view.resize(900, 700)
view.move(10, 150)

url = sys.argv[1]
if url.startswith("http://") or url.startswith("https://"):
    view.load(QUrl(url))
else:
    view.load(QUrl.fromLocalFile(url))

view.show()

sys.exit(app.exec())
