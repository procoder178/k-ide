import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def open_color_picker():
    dialog = Gtk.ColorChooserDialog(title="Choose a Color")

    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        color = dialog.get_rgba()

        r = int(color.red * 255)
        g = int(color.green * 255)
        b = int(color.blue * 255)

        hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        dialog.destroy()
        return hex_color

    dialog.destroy()
    return None
