from gi.repository import Adw, Gtk, GObject
from .utils import GProperty


@Gtk.Template(resource_path="/io/github/posaydone/hyprsettings/sidebar_item.ui")
class SidebarItem(Adw.Bin):
    __gtype_name__ = "SidebarItem"

    icon_widget: Gtk.Image = Gtk.Template.Child("icon")
    label_widget: Gtk.Label = Gtk.Template.Child("label")
    click_gesture: Gtk.GestureClick = Gtk.Template.Child("click")

    __gsignals__ = {"section-clicked": (GObject.SignalFlags.RUN_FIRST, None, (object,))}

    icon_name = GProperty(str)
    label = GProperty(str)

    def __init__(self, **props):
        super().__init__(**props)

        self.bind_property("label", self.label_widget, "label")
        self.bind_property("icon-name", self.icon_widget, "icon-name")
