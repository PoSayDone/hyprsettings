from gi.repository import Gtk, GObject


@Gtk.Template(resource_path="/io/github/posaydone/hyprsettings/sidebar_box.ui")
class SidebarBox(Gtk.Box):
    __gtype_name__ = "SidebarBox"

    __gsignals__ = {
        "network-button-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "appearance-button-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    icons = {
        "movie": "camera-video-symbolic",
    }

    section_list = Gtk.Template.Child()

    def __init__(self, **props):
        super().__init__(**props)
        self.section_list.connect("row-selected", self.__on_section_clicked)

    def __on_section_clicked(self, _, listboxrow):
        if listboxrow != None:
            child = listboxrow.get_child()
            if child.label == "Network":
                self.emit("network-button-clicked")
            elif child.label == "Appearance":
                self.emit("appearance-button-clicked")
