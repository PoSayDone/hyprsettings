import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from gi.repository import AstalNetwork as Network


@Gtk.Template(resource_path="/io/github/posaydone/hyprsettings/pages/network.ui")
class NetworkPage(Gtk.ScrolledWindow):
    __gtype_name__ = "NetworkPage"

    def __init__(self, **props):
        super().__init__(**props)
