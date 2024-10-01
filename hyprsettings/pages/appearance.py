import subprocess
from pathlib import Path
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gio, Gdk
import time

from hyprsettings.utils import GProperty
from hyprsettings.widgets.wallpaper_item import WallpaperItem


@Gtk.Template(resource_path="/io/github/posaydone/hyprsettings/pages/appearance.ui")
class AppearancePage(Gtk.ScrolledWindow):
    __gtype_name__ = "AppearancePage"

    wallpapers_folder = f"{Path.home()}/.local/share/hyprsettings/wallpapers"
    current_wallpaper_picture: Gtk.Picture = Gtk.Template.Child()
    wallpapers_flowbox: Gtk.FlowBox = Gtk.Template.Child()
    add_wallpaper_button: Gtk.Button = Gtk.Template.Child()
    file_filter_image = Gtk.Template.Child()
    theme_box = Gtk.Template.Child()
    dark_mode_toggle = Gtk.Template.Child()
    light_mode_toggle = Gtk.Template.Child()

    current_mode = GProperty(str)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restore_wallpapers()
        self.settings = Gio.Settings(schema_id="io.github.posaydone.hyprsettings")
        self.settings.bind(
            "current-mode", self, "current-mode", Gio.SettingsBindFlags.DEFAULT
        )

        if self.current_mode == "dark":
            self.dark_mode_toggle.set_active(True)
        else:
            self.light_mode_toggle.set_active(True)

        self.add_wallpaper_button.connect("clicked", self.on_add_wallpaper)
        self.wallpapers_flowbox.connect(
            "child-activated", self.on_wallpaper_flowbox_child_activated
        )
        self.dark_mode_toggle.connect(
            "notify::active",
            lambda _, status: self.on_mode_active("dark") if status else "",
        )
        self.light_mode_toggle.connect(
            "notify::active",
            lambda _, status: self.on_mode_active("light") if status else "",
        )

    def on_mode_active(self, mode):
        self.set_property("current-mode", mode)
        self.on_wallpaper_set(
            f"{Path.home()}/.local/share/hyprsettings/current_wallpaper", False
        )

    def restore_wallpapers(self):

        try:
            self.current_wallpaper_picture.set_filename(
                f"{Path.home()}/.local/share/hyprsettings/current_wallpaper"
            )
        except:
            print("no current wp")

        subprocess.Popen(
            [
                "mkdir",
                "-p",
                self.wallpapers_folder,
            ],
        )

        files = Gio.File.new_for_path(self.wallpapers_folder).enumerate_children(
            "standard::name,standard::type",
            Gio.FileQueryInfoFlags.NONE,
            None,
        )

        info = files.next_file(None)

        while info:
            if info.get_file_type() == Gio.FileType.REGULAR:
                name = info.get_name()
                self.create_image_widget(f"{self.wallpapers_folder}/{name}")
            info = files.next_file(None)

    def create_image_widget(self, filepath):
        image = WallpaperItem()
        self.wallpapers_flowbox.append(image)
        image.set_image(filepath)

    def on_add_wallpaper(self, _):
        file_dialog = Gtk.FileDialog(default_filter=self.file_filter_image)
        file_dialog.open(None, None, self.on_wallpaper_picked)

    def on_wallpaper_picked(self, file_dialog, result):
        file = file_dialog.open_finish(result)
        filepath = file.get_path()
        subprocess.Popen(
            ["cp", filepath, self.wallpapers_folder],
        )
        self.create_image_widget(filepath)

    def on_wallpaper_flowbox_child_activated(self, _flowbox, child):
        self.on_wallpaper_set(child.get_child().filepath, True)

    def on_wallpaper_set(self, filepath, symlink=True):
        self.current_wallpaper_picture.set_filename(filepath)
        subprocess.Popen(
            ["matugen", "image", filepath, "-m", self.current_mode],
        )
        subprocess.Popen(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.interface",
                "gtk-theme",
                f"adw-gtk3-{self.current_mode}",
            ]
        )
        subprocess.Popen(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.interface",
                "color-scheme",
                f"prefer-{self.current_mode}",
            ]
        )
        if symlink:
            subprocess.Popen(
                [
                    "ln",
                    "-sf",
                    filepath,
                    f"{Path.home()}/.local/share/hyprsettings/current_wallpaper",
                ]
            )
        time.sleep(1)
        self.reload_gtk_theme()

    def reload_gtk_theme(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{Path.home()}/.config/gtk-4.0/colors.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )
