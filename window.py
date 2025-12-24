import os
import re
import subprocess

from editors.cpp_editor import CppEditorTextArea
from editors.css_editor import CssEditorTextArea
from editors.html_editor import HtmlEditorTextArea
from editors.java_editor import JavaEditorTextArea
from editors.js_editor import JavaScriptEditorTextArea
from editors.lua_editor import LuaEditorTextArea
from editors.python_editor import PythonEditorTextArea
from PyQt5.QtCore import QDir, QModelIndex, Qt, QUrl
from PyQt5.QtGui import QFont, QIcon, QKeyEvent
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QFileSystemModel,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QStatusBar,
    QTabWidget,
    QTreeView,
    QVBoxLayout,
    QWidget,
)
from qtawesome import icon
from utils.boiler_plates import cpp_plate, html_plate, java_plate
from utils.center_window import cw
from utils.color_picker import open_color_picker
from utils.formatter import format_code
from utils.terminal import TerminalWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.root_dir = os.getcwd()
        
        self.setWindowTitle("Code Editor")
        self.setWindowIcon(QIcon(os.path.join(self.root_dir,"icons/editor.png")))
        self.setFixedSize(1200, 700)
        cw(self)

        self.files = {}

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.tree_area = QFrame()
        self.tree_area.setFixedWidth(280)
        self.tree_area.setFixedHeight(450)

        self.path_label = QLabel("Home (Ubuntu)")
        self.path_label.setFont(QFont("Consolas", 10, QFont.Bold))
        self.path_label.setAlignment(Qt.AlignTop)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath()))
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)
        self.tree.setAnimated(True)
        self.tree.setSortingEnabled(False)
        self.tree.setHeaderHidden(True)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.clicked.connect(self.control_tree)

        self.main_area = QFrame()
        self.main_area.setFixedWidth(920)
        self.main_area.setFixedHeight(450)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.remove_tab)

        self.term = TerminalWidget()
        self.term.setFixedHeight(120)

        py_layout = QVBoxLayout()
        layout = QHBoxLayout()
        tree_layout = QVBoxLayout()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.main_area.setLayout(main_layout)
        tree_layout.addWidget(self.path_label)
        tree_layout.addWidget(self.tree)
        self.tree_area.setLayout(tree_layout)
        layout.addWidget(self.tree_area)
        layout.addWidget(self.main_area)
        py_layout.addLayout(layout)
        py_layout.addWidget(self.term)
        self.central.setLayout(py_layout)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.status_label = QLabel("Word: 0 | Character: 0")
        self.statusbar.addPermanentWidget(self.status_label)

        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.initMenu()

    def initMenu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        build_menu = menubar.addMenu("Build")

        new_file_menu = QMenu("New File", self)
        new_python_file_action = QAction(
            self.get_icon("python"), "Python", self
        )
        new_java_file_action = QAction(self.get_icon("java"), "Java", self)
        new_cpp_file_action = QAction(self.get_icon("cpp"), "C++", self)
        new_html_file_action = QAction(self.get_icon("html"), "HTML", self)
        new_css_file_action = QAction(self.get_icon("css"), "CSS", self)
        new_js_file_action = QAction(
            self.get_icon("js"), "javaScript", self
        )
        new_lua_file_action = QAction(self.get_icon("lua"), "Lua", self)
        open_folder_action = QAction(
            icon("fa5s.folder-open", color="#EE9F00"), "Open Folder", self
        )
        open_file_action = QAction(
            icon("fa5s.file-alt", color="#FFBF2A"), "Open File", self
        )
        save_file_action = QAction(
            icon("fa5s.save", color="#2AFF9C"), "Save File", self
        )
        cut_action = QAction(
            icon("fa5s.cut", color="#EC0B0B"), "Cut", self
        )
        copy_action = QAction(
            icon("fa5s.copy", color="#27E8D3"), "Copy", self
        )
        paste_action = QAction(
            icon("fa5s.paste", color="#DC9011"), "Paste", self
        )
        select_all_action = QAction(
            icon("fa5s.i-cursor", color="#16A9E8"), "Select All", self
        )
        undo_action = QAction(
            icon("fa5s.undo", color="#BBBBBB"), "Undo", self
        )
        redo_action = QAction(
            icon("fa5s.redo", color="#BBBBBB"), "Redo", self
        )
        exit_action = QAction(
            icon("fa5s.sign-out-alt", color="#D50000"), "Exit", self
        )
        arrange_code_action = QAction(
            icon("fa5s.magic", color="#9312CA"), "Arrange Code", self
        )
        color_picker_action = QAction(
            icon("fa5s.paint-brush", color="#70A2C9"), "Color Picker", self
        )
        run_code_action = QAction(
            icon("fa5s.play", color="#04E216"), "Run", self
        )

        new_python_file_action.triggered.connect(lambda: self.add_tab())
        new_java_file_action.triggered.connect(
            lambda: self.add_tab(tp="java")
        )
        new_cpp_file_action.triggered.connect(
            lambda: self.add_tab(tp="cpp")
        )
        new_html_file_action.triggered.connect(
            lambda: self.add_tab(tp="html")
        )
        new_css_file_action.triggered.connect(
            lambda: self.add_tab(tp="css")
        )
        new_js_file_action.triggered.connect(lambda: self.add_tab(tp="js"))
        new_lua_file_action.triggered.connect(
            lambda: self.add_tab(tp="lua")
        )
        open_folder_action.triggered.connect(self.open_folder)
        open_file_action.triggered.connect(self.open_file)
        save_file_action.triggered.connect(self.save_file)
        cut_action.triggered.connect(self.cut_text)
        copy_action.triggered.connect(self.copy_text)
        paste_action.triggered.connect(self.paste_text)
        undo_action.triggered.connect(self.undo_text)
        redo_action.triggered.connect(self.redo_text)
        select_all_action.triggered.connect(self.select_all_text)
        exit_action.triggered.connect(self.close)
        arrange_code_action.triggered.connect(self.arrange_code)
        color_picker_action.triggered.connect(self.pick_color)
        run_code_action.triggered.connect(self.run_code)

        open_file_action.setShortcut("Ctrl+O")
        open_folder_action.setShortcut("Shift+Ctrl+O")
        save_file_action.setShortcut("Ctrl+S")
        cut_action.setShortcut("Ctrl+X")
        copy_action.setShortcut("Ctrl+C")
        paste_action.setShortcut("Ctrl+V")
        select_all_action.setShortcut("Ctrl+A")
        undo_action.setShortcut("Ctrl+Z")
        redo_action.setShortcut("Ctrl+Y")
        exit_action.setShortcut("Ctrl+Q")
        arrange_code_action.setShortcut("F1")
        color_picker_action.setShortcut("F2")
        run_code_action.setShortcut("F5")

        file_menu.addMenu(new_file_menu)
        new_file_menu.addActions(
            [
                new_python_file_action,
                new_java_file_action,
                new_cpp_file_action,
                new_html_file_action,
                new_css_file_action,
                new_js_file_action,
                new_lua_file_action,
            ]
        )
        file_menu.addActions(
            [open_folder_action, open_file_action, save_file_action]
        )
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        edit_menu.addActions([cut_action, copy_action, paste_action])
        edit_menu.addSeparator()
        edit_menu.addActions([select_all_action, undo_action, redo_action])
        build_menu.addActions(
            [arrange_code_action, color_picker_action, run_code_action]
        )

    def get_icon(self, lang):
        icon = QIcon()
        for size in (16, 24, 32):
            icon.addFile(os.path.join(self.root_dir, f"icons/{lang}/{lang}_{size}.png"))
        return icon

    def pick_color(self):
        color = open_color_picker()
        if color:
            editor = self.get_current_editor()
            if editor:
                editor.insert(color)
                line, idx = editor.getCursorPosition()
                editor.setCursorPosition(line, idx + len(color))

    def control_tree(self, index: QModelIndex):
        if self.model.isDir(index):
            if self.tree.isExpanded(index):
                self.tree.collapse(index)
            else:
                self.tree.expand(index)
        else:
            file_path = self.model.filePath(index)
            files_path = []
            for f in self.files.values():
                files_path.append(f[0])
            if file_path not in files_path:
                self.add_tab(file=file_path)
            else:
                self.tabs.setCurrentIndex(
                    self.files[os.path.basename(file_path)][1]
                )

    def add_tab(self, file=None, tp="python"):
        if file is None:
            if tp == "python":
                self.editor = PythonEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)

                tab_idx = self.tabs.addTab(self.editor, "Untitled.py")
                self.tabs.setCurrentIndex(tab_idx)
                self.editor.setFocus()
                self.update_status_bar()
            elif tp == "java":
                self.editor = JavaEditorTextArea()
                self.editor.setText("\n".join(java_plate))
                self.editor.textChanged.connect(self.update_status_bar)

                tab_idx = self.tabs.addTab(self.editor, "Untitled.java")
                self.tabs.setCurrentIndex(tab_idx)
                self.editor.setFocus()
                self.editor.setSelection(0, 13, 0, 21)
                self.update_status_bar()
            elif tp == "cpp":
                self.editor = CppEditorTextArea()
                self.editor.setText("\n".join(cpp_plate))
                self.editor.textChanged.connect(self.update_status_bar)

                tab_idx = self.tabs.addTab(self.editor, "Untitled.cpp")
                self.tabs.setCurrentIndex(tab_idx)
                self.editor.setFocus()
                self.editor.setCursorPosition(5, len(cpp_plate[5]))
                self.update_status_bar()
            elif tp == "html":
                self.editor = HtmlEditorTextArea()
                self.editor.setText("\n".join(html_plate))
                self.editor.textChanged.connect(self.update_status_bar)

                tab_idx = self.tabs.addTab(self.editor, "Untitled.html")
                self.tabs.setCurrentIndex(tab_idx)
                self.editor.setFocus()
                self.editor.setCursorPosition(7, 8)
                self.update_status_bar()
            elif tp == "css":
                self.editor = CssEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)

                tab_idx = self.tabs.addTab(self.editor, "Untitled.css")
                self.tabs.setCurrentIndex(tab_idx)
                self.editor.setFocus()
                self.update_status_bar()
            elif tp == "js":
                self.editor = JavaScriptEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)

                tab_idx = self.tabs.addTab(self.editor, "Untitled.js")
                self.tabs.setCurrentIndex(tab_idx)
                self.editor.setFocus()
                self.update_status_bar()
            elif tp == "lua":
                self.editor = LuaEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)

                tab_idx = self.tabs.addTab(self.editor, "Untitled.lua")
                self.tabs.setCurrentIndex(tab_idx)
                self.editor.setFocus()
                self.update_status_bar()
        else:
            if os.path.basename(file).split(".")[-1] == "py":
                self.editor = PythonEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)
                self.editor.setText(
                    open(file, "r", encoding="utf-8").read()
                )

                tab_idx = self.tabs.addTab(
                    self.editor, os.path.basename(file)
                )
                self.tabs.setCurrentIndex(tab_idx)
                self.update_status_bar()
                self.files[os.path.basename(file)] = [file, tab_idx]
            elif os.path.basename(file).split(".")[-1] == "java":
                self.editor = JavaEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)
                self.editor.setText(
                    open(file, "r", encoding="utf-8").read()
                )

                tab_idx = self.tabs.addTab(
                    self.editor, os.path.basename(file)
                )
                self.tabs.setCurrentIndex(tab_idx)
                self.update_status_bar()
                self.files[os.path.basename(file)] = [file, tab_idx]
            elif os.path.basename(file).split(".")[-1] == "cpp":
                self.editor = CppEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)
                self.editor.setText(
                    open(file, "r", encoding="utf-8").read()
                )

                tab_idx = self.tabs.addTab(
                    self.editor, os.path.basename(file)
                )
                self.tabs.setCurrentIndex(tab_idx)
                self.update_status_bar()
                self.files[os.path.basename(file)] = [file, tab_idx]
            elif os.path.basename(file).split(".")[-1] == "html":
                self.editor = HtmlEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)
                self.editor.setText(
                    open(file, "r", encoding="utf-8").read()
                )

                tab_idx = self.tabs.addTab(
                    self.editor, os.path.basename(file)
                )
                self.tabs.setCurrentIndex(tab_idx)
                self.update_status_bar()
                self.files[os.path.basename(file)] = [file, tab_idx]
            elif os.path.basename(file).split(".")[-1] == "css":
                self.editor = CssEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)
                self.editor.setText(
                    open(file, "r", encoding="utf-8").read()
                )

                tab_idx = self.tabs.addTab(
                    self.editor, os.path.basename(file)
                )
                self.tabs.setCurrentIndex(tab_idx)
                self.update_status_bar()
                self.files[os.path.basename(file)] = [file, tab_idx]
            elif os.path.basename(file).split(".")[-1] == "js":
                self.editor = JavaScriptEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)
                self.editor.setText(
                    open(file, "r", encoding="utf-8").read()
                )

                tab_idx = self.tabs.addTab(
                    self.editor, os.path.basename(file)
                )
                self.tabs.setCurrentIndex(tab_idx)
                self.update_status_bar()
                self.files[os.path.basename(file)] = [file, tab_idx]
            elif os.path.basename(file).split(".")[-1] == "lua":
                self.editor = LuaEditorTextArea()
                self.editor.textChanged.connect(self.update_status_bar)
                self.editor.setText(
                    open(file, "r", encoding="utf-8").read()
                )

                tab_idx = self.tabs.addTab(
                    self.editor, os.path.basename(file)
                )
                self.tabs.setCurrentIndex(tab_idx)
                self.update_status_bar()
                self.files[os.path.basename(file)] = [file, tab_idx]
            else:
                QMessageBox.critical(
                    self,
                    "Unsupported File",
                    f"This is an python code editor\nit cannot support '{os.path.basename(file).split(".")[-1]}' extension files",
                )

    def remove_tab(self, index):
        if self.tabs.tabText(index) in self.files.keys():
            del self.files[self.tabs.tabText(index)]
        self.tabs.removeTab(index)

    def on_tab_changed(self, index):
        self.update_status_bar()

    def update_status_bar(self):
        editor = self.get_current_editor()
        if editor:
            word = len(editor.text().split())
            char = len(editor.text())
            self.status_label.setText(f"Word: {word} | Character: {char}")
        else:
            self.status_label.setText("Word: 0 | Character: 0")

    def open_folder(self):
        dialog = QFileDialog(self, "Open Folder")
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setSidebarUrls(
            [
                QUrl.fromLocalFile("/home/krish"),
                QUrl.fromLocalFile("/storage/emulated/0"),
                QUrl.fromLocalFile("/data/data/com.termux/files/home"),
                QUrl.fromLocalFile("/"),
            ]
        )
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            lbl = ""
            if path == "/home/krish":
                lbl = "Home (Ubuntu)"
            elif path == "/":
                lbl = "File System"
            elif path == "/storage/emulated/0":
                lbl = "Storage"
            elif path == "/data/data/com.termux/files/home":
                lbl = "Home (Termux)"
            else:
                lbl = os.path.basename(path)
            self.path_label.setText(lbl)
            self.tree.setRootIndex(self.model.index(path))

    def open_file(self):
        dialog = QFileDialog(self, "Open File")
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setSidebarUrls(
            [
                QUrl.fromLocalFile("/home/krish"),
                QUrl.fromLocalFile("/storage/emulated/0"),
                QUrl.fromLocalFile("/data/data/com.termux/files/home"),
                QUrl.fromLocalFile("/"),
            ]
        )
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            files_path = []
            for f in self.files.values():
                files_path.append(f[0])
            if file_path not in files_path:
                self.add_tab(file=file_path)
            else:
                self.tabs.setCurrentIndex(
                    self.files[os.path.basename(file_path)][1]
                )

    def save_file(self):
        editor = self.get_current_editor()
        if editor:
            if (
                self.tabs.tabText(self.tabs.currentIndex()).split(".")[0]
                == "Untitled"
            ):
                text = editor.text()
                dialog = QFileDialog(self, "Save File")
                dialog.setAcceptMode(QFileDialog.AcceptSave)
                dialog.setFileMode(QFileDialog.AnyFile)
                dialog.setSidebarUrls(
                    [
                        QUrl.fromLocalFile("/home/krish"),
                        QUrl.fromLocalFile("/storage/emulated/0"),
                        QUrl.fromLocalFile(
                            "/data/data/com.termux/files/home"
                        ),
                        QUrl.fromLocalFile("/"),
                    ]
                )
                if dialog.exec():
                    file_path = dialog.selectedFiles()[0]
                    text = self.format_code(text)
                    with open(file_path, "w") as f:
                        f.write(text)
                    editor.setText(open(file_path, "r").read())

            else:
                file_path = self.files[
                    self.tabs.tabText(self.tabs.currentIndex())
                ][0]
                with open(file_path, "w") as f:
                    f.write(editor.text())
                editor.setText(open(file_path, "r").read())

    def get_current_editor(self):
        return self.tabs.widget(self.tabs.currentIndex())

    def cut_text(self):
        editor = self.get_current_editor()
        if editor is not None:
            editor.cut()

    def copy_text(self):
        editor = self.get_current_editor()
        if editor is not None:
            editor.copy()

    def paste_text(self):
        editor = self.get_current_editor()
        if editor is not None:
            editor.paste()

    def undo_text(self):
        editor = self.get_current_editor()
        if editor is not None:
            editor.undo()

    def redo_text(self):
        editor = self.get_current_editor()
        if editor is not None:
            editor.redo()

    def select_all_text(self):
        editor = self.get_current_editor()
        if editor is not None:
            editor.selectAll()

    def arrange_code(self):
        tab_name = self.tabs.tabText(self.tabs.currentIndex())
        code_ext = self.tabs.tabText(self.tabs.currentIndex()).split(".")[
            -1
        ]
        if code_ext == "py":
            editor = self.get_current_editor()
            if editor is not None:
                editor.setText(format_code(editor.text()))
        elif code_ext == "html":
            editor = self.get_current_editor()
            if editor is not None:
                file_path = self.files[tab_name][0]
                subprocess.Popen(["tidy", "-i", "-m", f"{file_path}"])
                editor.setText(open(file_path, "r").read())
        else:
            QMessageBox.warning(
                self,
                "Arrange Code",
                "Arrange Code feature is only supported for Python",
            )

    def run_code(self):
        global code
        tab_name = self.tabs.tabText(self.tabs.currentIndex())
        ext = tab_name.split(".")[-1]
        editor = self.get_current_editor()
        if editor is not None:
            if ext == "py":
                if tab_name == "Untitled.py":
                    subprocess.Popen(
                        [
                            "xfce4-terminal",
                            "--hold",
                            "-e",
                            f"python3 -c '{editor.text()}'",
                        ]
                    )
                else:
                    file_path = self.files[tab_name][0]
                    subprocess.Popen(
                        [
                            "xfce4-terminal",
                            "--hold",
                            "-e",
                            f"python3 {file_path}",
                        ]
                    )
            elif ext == "java":
                file_path = self.files.get(tab_name, None)
                if file_path is not None:
                    file_path = file_path[0]
                    cls_name = self.get_java_class_name(file_path)
                    parts = file_path.split("/")
                    parts[0] = "/"
                    del parts[-1]
                    for p in parts:
                        os.chdir(p)
                    cmd = f"javac {tab_name} && java {cls_name}"
                    subprocess.Popen(
                        [
                            "xfce4-terminal",
                            "--hold",
                            "-e",
                            f"sh -c '{cmd}'",
                        ]
                    )
                else:
                    QMessageBox.critical(
                        self, "File Not Found", "404 - File Not Found"
                    )
            elif ext == "cpp":
                file_path = self.files.get(tab_name, None)
                if file_path is not None:
                    file_path = file_path[0]
                    parts = file_path.split("/")
                    bin_file = tab_name.split(".")[0]
                    parts[0] = "/"
                    del parts[-1]
                    for p in parts:
                        os.chdir(p)
                    cmd = (
                        f"clang++ {tab_name} -o {bin_file} && ./{bin_file}"
                    )
                    subprocess.Popen(
                        [
                            "xfce4-terminal",
                            "--hold",
                            "-e",
                            f"sh -c '{cmd}'",
                        ]
                    )
                else:
                    QMessageBox.critical(
                        self, "File Not Found", "404 - File Not Found"
                    )
            elif ext == "html":
                file_path = self.files.get(tab_name, None)
                if file_path is not None:
                    file_path = file_path[0]
                    cmd = f"python3 utils/browser.py {file_path} &"
                    subprocess.Popen(cmd.split())
                else:
                    QMessageBox.critical(
                        self, "File Not Found", "404 - File Not Found"
                    )
            elif ext == "lua":
                file_path = self.files.get(tab_name, None)
                if file_path is not None:
                    file_path = file_path[0]
                    subprocess.Popen(
                        [
                            "xfce4-terminal",
                            "--hold",
                            "-e",
                            f"lua {file_path}",
                        ]
                    )
                else:
                    QMessageBox.critical(
                        self, "File Not Found", "404 - File Not Found"
                    )

    def get_java_class_name(self, file):
        content = open(file, "r").read()
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
        content = re.sub(r"//.*?", "", content)
        name = re.search(r"\bclass\s+([A-Za-z][A-Za-z0-9_]*)", content)
        if name:
            return name.group(1)
        else:
            return None
