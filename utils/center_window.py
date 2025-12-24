from PyQt5.QtWidgets import QApplication


def cw(window):
    screen = QApplication.primaryScreen().geometry()
    window_geom = window.frameGeometry()
    center_point = screen.center()
    window_geom.moveCenter(center_point)
    window.move(window_geom.topLeft())
