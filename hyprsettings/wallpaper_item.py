from gi.repository import Adw, Gtk, GObject, GdkPixbuf
from .utils import GProperty


@Gtk.Template(resource_path="/io/github/posaydone/hyprsettings/wallpaper_item.ui")
class WallpaperItem(Gtk.Box):
    __gtype_name__ = "WallpaperItem"

    wallpaper_widget = Gtk.Template.Child("wallpaper")

    filepath = GProperty(str)

    def __init__(self, pathname, **props):
        super().__init__(**props)
        self.set_image(pathname)

    def set_image(self, filepath):
        self.filepath = filepath
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filepath)
        self.wallpaper_widget.set_pixbuf(pixbuf)
