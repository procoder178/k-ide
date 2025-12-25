import sys
import os
import vlc
import json

os.environ["QT_XCB_GL_INTEGRATION"] = "none"

from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QSlider, QLabel, QCheckBox,
    QFileDialog, QAction
)
from PyQt5.QtCore import Qt, QTimer, QSize, QUrl
from PyQt5.QtGui import QIcon
from qtawesome import icon


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setWindowIcon(QIcon("assets/music_player.png"))
        self.setFixedSize(320, 360)

        # ---------- VLC ----------
        self.player = vlc.MediaPlayer()
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached,
            self.song_finished
        )

        # ---------- DATA ----------
        self.playlist = []
        self.file_path = "utils/playlist.json"
        self.index = 0
        self.loop = False

        # ---------- UI ----------
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.load_song)
        layout.addWidget(self.list_widget)

        # ---------- BUTTONS ----------
        btn_layout = QHBoxLayout()

        self.btn_prev = QPushButton()
        self.btn_play = QPushButton()
        self.btn_pause = QPushButton()
        self.btn_next = QPushButton()

        self.btn_prev.setIcon(icon("fa5s.backward", color="#FFA500"))
        self.btn_play.setIcon(icon("fa5s.play", color="#40DC16"))
        self.btn_pause.setIcon(icon("fa5s.pause", color="#DB0707"))
        self.btn_next.setIcon(icon("fa5s.forward", color="#FFA500"))

        for b in (self.btn_prev, self.btn_play, self.btn_pause, self.btn_next):
            b.setIconSize(QSize(28, 28))
            btn_layout.addWidget(b)

        self.btn_prev.clicked.connect(self.prev_song)
        self.btn_play.clicked.connect(self.play_music)
        self.btn_pause.clicked.connect(self.pause_music)
        self.btn_next.clicked.connect(self.next_song)

        layout.addLayout(btn_layout)

        # ---------- SEEK ----------
        self.seek = QSlider(Qt.Horizontal)
        self.seek.setRange(0, 1000)
        self.seek.sliderMoved.connect(self.set_position)
        layout.addWidget(self.seek)

        # ---------- TIME ----------
        self.time_label = QLabel("00:00 / 00:00", alignment=Qt.AlignCenter)
        layout.addWidget(self.time_label)

        # ---------- LOOP ----------
        self.loop_check = QCheckBox("Play with Loop 🔁")
        self.loop_check.stateChanged.connect(self.toggle_loop)
        layout.addWidget(self.loop_check)
        
        hide_btn = QPushButton("Hide Button")
        hide_btn.clicked.connect(self.hide)
        
        layout.addWidget(hide_btn)

        # ---------- TIMER ----------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(500)

        # ---------- MENU ----------
        self.initMenu()
        
        if os.path.exists(self.file_path):
            data = json.load(open(self.file_path, "r"))
            if data:
                for p in data["PlayList-Files"]:
                    self.add_in_ui(p)

    # ================= MENU =================
    def initMenu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        add_file = QAction(icon("fa5s.file", color="#DB8607"), "Add File", self)
        delete_file = QAction(icon("fa5s.trash", color="red"), "Remove File", self)
        exit_app = QAction(icon("fa5s.sign-out-alt", color="#F03F07"), "Exit", self)

        add_file.triggered.connect(self.add_file)
        delete_file.triggered.connect(self.delete_selected)
        exit_app.triggered.connect(self.close_window)

        file_menu.addAction(add_file)
        file_menu.addAction(delete_file)
        file_menu.addSeparator()
        file_menu.addAction(exit_app)

    def close_window(self):
        self.player.stop()
        self.close()

    def delete_selected(self):
        row = self.list_widget.currentRow()

        if row == -1:
            return

        if row == self.index:
            self.player.stop()

        self.playlist.pop(row)
        self.update_json()

        self.list_widget.takeItem(row)

        if self.index >= len(self.playlist):
            self.index = len(self.playlist) - 1

        if self.playlist:
            self.list_widget.setCurrentRow(self.index)
            self.load_song(self.index)
        else:
            self.index = 0

    def add_file(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter(
            "Audio Files (*.mp3 *.wav *.aac *.ogg *.flac *.m4a *.opus *.wma *.amr)"
        )

        dialog.setSidebarUrls([
            QUrl.fromLocalFile("/home/krish/Music"),
            QUrl.fromLocalFile("/data/data/com.termux/files/home"),
            QUrl.fromLocalFile("/storage/emulated/0"),
            QUrl.fromLocalFile("/")
        ])

        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            self.add_in_ui(path)
            self.update_json()
            
    def update_json(self):
        data = {
            "PlayList-Files": self.playlist
        }
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def add_in_ui(self, path):
        if path not in self.playlist:
            self.playlist.append(path)
            self.list_widget.addItem(os.path.basename(path))

            # First song auto-load
            if len(self.playlist) == 1:
                self.list_widget.setCurrentRow(0)
                self.load_song(0)

    # ================= PLAYER =================
    def load_song(self, index):
        if 0 <= index < len(self.playlist):
            self.index = index
            self.player.set_media(vlc.Media(self.playlist[index]))

    def play_music(self):
        if self.playlist:
            self.player.play()

    def pause_music(self):
        self.player.pause()

    def next_song(self):
        if not self.playlist:
            return

        self.index += 1
        if self.index >= len(self.playlist):
            if self.loop:
                self.index = 0
            else:
                return

        self.list_widget.setCurrentRow(self.index)
        self.play_music()

    def prev_song(self):
        if not self.playlist:
            return

        self.index = (self.index - 1) % len(self.playlist)
        self.list_widget.setCurrentRow(self.index)
        self.play_music()

    def toggle_loop(self, state):
        self.loop = state == Qt.Checked

    def song_finished(self, event):
        QTimer.singleShot(0, self.next_song)

    # ================= UI UPDATE =================
    def set_position(self, value):
        self.player.set_position(value / 1000)

    def update_ui(self):
        if self.player.is_playing():
            pos = self.player.get_position()
            self.seek.setValue(int(pos * 1000))

            self.time_label.setText(
                f"{self.format_time(self.player.get_time())} / "
                f"{self.format_time(self.player.get_length())}"
            )

    def format_time(self, ms):
        if ms <= 0:
            return "00:00"
        s = ms // 1000
        return f"{s // 60:02d}:{s % 60:02d}"
