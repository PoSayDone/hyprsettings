from gi.repository import Adw, Gtk, GObject, GdkPixbuf, GLib
from hyprsettings.utils import GProperty
from threading import Thread
import concurrent.futures


@Gtk.Template(
    resource_path="/io/github/posaydone/hyprsettings/widgets/wallpaper_item.ui"
)
class WallpaperItem(Gtk.Box):
    __gtype_name__ = "WallpaperItem"

    wallpaper_widget = Gtk.Template.Child("wallpaper")
    filepath = GProperty(str)

    def __init__(self, **props):
        super().__init__(**props)

    def set_image(self, filepath):
        self.filepath = filepath
        executor = concurrent.futures.ThreadPoolExecutor()
        executor.submit(self.load_image, filepath)

    def load_image(self, filepath):
        # Load the image in a separate thread
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filepath)
        # Calculate new dimensions while keeping aspect ratio
        max_width = 400
        max_height = 400
        width = pixbuf.get_width()
        height = pixbuf.get_height()

        # Maintain aspect ratio
        aspect_ratio = width / height

        if width > max_width or height > max_height:
            if width / max_width > height / max_height:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
        else:
            # If the image is smaller than the target size, keep the original size
            new_width, new_height = width, height

        # Scale the image
        scaled_pixbuf = pixbuf.scale_simple(
            new_width, new_height, GdkPixbuf.InterpType.BILINEAR
        )
        # Schedule the UI update in the main thread
        GLib.idle_add(self.set_pixbuf, scaled_pixbuf)

    def set_pixbuf(self, pixbuf):
        self.wallpaper_widget.set_pixbuf(pixbuf)
