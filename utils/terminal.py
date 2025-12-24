import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Vte", "2.91")
from gi.repository import GdkX11, GLib, Gtk, Vte
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QFrame, QVBoxLayout


class Terminal(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.vte = Vte.Terminal()
        self.pack_start(self.vte, True, True, 0)

        self.vte.spawn_async(
            Vte.PtyFlags.DEFAULT,
            GLib.get_home_dir(),
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None,
        )

        self.vte.connect("realize", self.on_realize)

    def on_realize(self, *args):
        self.xid = self.vte.get_window().get_xid()


class TerminalWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.gtk_term = Terminal()

        self.gtk_win = Gtk.Window()
        self.gtk_win.add(self.gtk_term)
        self.gtk_win.show_all()

        while not hasattr(self.gtk_term, "xid"):
            while Gtk.events_pending():
                Gtk.main_iteration()

        self.qwindow = QWindow.fromWinId(self.gtk_term.xid)
        self.container = self.createWindowContainer(self.qwindow, self)

        layout.addWidget(self.container)
