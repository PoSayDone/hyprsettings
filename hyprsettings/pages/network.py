from gi.repository import Gtk


@Gtk.Template(resource_path="/io/github/posaydone/hyprsettings/pages/network.ui")
class NetworkPage(Gtk.ScrolledWindow):
    __gtype_name__ = "NetworkPage"

    def __init__(self, **props):
        super().__init__(**props)
