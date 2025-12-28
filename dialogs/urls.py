from PyQt5.QtCore import QUrl, QDir

URLS = [
    QUrl.fromLocalFile(QDir.homePath()),
    QUrl.fromLocalFile("/storage/emulated/0"),
    QUrl.fromLocalFile("/data/data/com.termux/files/home"),
    QUrl.fromLocalFile("/")
]
