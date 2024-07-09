# window.py
#
# Copyright 2024 Unknown
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
from pathlib import Path
from gi.repository import Adw, Gtk, Gio, Gdk
import time
from threading import Thread

from .utils import GProperty
from .wallpaper_item import WallpaperItem
from .sidebar_item import SidebarItem
from .sidebar_box import SidebarBox


@Gtk.Template(resource_path="/io/github/posaydone/hyprsettings/window.ui")
class HyprsettingsWindow(Adw.ApplicationWindow):
    __gtype_name__ = "HyprsettingsWindow"

    wallpapers_folder = f"{Path.home()}/.cache/hyprsettings/wallpapers"
    current_wallpaper_picture: Gtk.Picture = Gtk.Template.Child()
    wallpapers_flowbox: Gtk.Picture = Gtk.Template.Child()
    add_wallpaper_button: Gtk.Button = Gtk.Template.Child()
    sidebar_box: Gtk.Box = Gtk.Template.Child()
    network_page = Gtk.Template.Child()
    appearance_page = Gtk.Template.Child()
    pages_stack = Gtk.Template.Child()
    file_filter_image = Gtk.Template.Child()
    theme_comborow = Gtk.Template.Child()

    current_theme = GProperty(str)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_property("current_theme", "dark")
        self.restore_wallpapers()

        add_wallpaper_action = Gio.SimpleAction(name="addwallpaper")
        add_wallpaper_action.connect("activate", self.on_add_wallpaper)
        self.add_action(add_wallpaper_action)

        self.sidebar_box.connect("network-button-clicked", self.on_network_clicked)
        self.sidebar_box.connect(
            "appearance-button-clicked", self.on_appearance_clicked
        )

        self.theme_comborow.connect("notify::selected-item", self.on_theme_changed)

    def on_theme_changed(self, widget, _):
        value = widget.get_selected_item().get_string().lower()
        self.set_property("current_theme", value)
        self.on_wallpaper_set(f"{Path.home()}/.cache/current_wallpaper", False),

    def on_network_clicked(self, _):
        self.pages_stack.set_visible_child_name("network")

    def on_appearance_clicked(self, _):
        self.pages_stack.set_visible_child_name("appearance")

    def restore_wallpapers(self):
        self.wallpapers_flowbox.connect(
            "child-activated", self.on_wallpaper_flowbox_child_activated
        )

        try:
            self.current_wallpaper_picture.set_filename(
                f"{Path.home()}/.cache/current_wallpaper"
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
        image = WallpaperItem(filepath)
        self.wallpapers_flowbox.append(image)

    def on_add_wallpaper(self, _action, _):
        file_dialog = Gtk.FileDialog(default_filter=self.file_filter_image)
        file_dialog.open(self, None, self.on_wallpaper_picked)

    def on_wallpaper_picked(self, file_dialog, result):
        file = file_dialog.open_finish(result)
        filepath = file.get_path()
        subprocess.Popen(
            ["cp", filepath, self.wallpapers_folder],
        )
        self.create_image_widget(filepath)

    def on_wallpaper_flowbox_child_activated(self, _flowbox, child):
        self.on_wallpaper_set(child.get_child().filepath)

    def on_wallpaper_set(self, filepath, symlink=True):
        self.current_wallpaper_picture.set_filename(filepath)
        subprocess.Popen(
            ["matugen", "image", filepath, "-m", self.current_theme],
        )
        subprocess.Popen(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.interface",
                "gtk-theme",
                f"adw-gtk3-{self.current_theme}",
            ]
        )
        subprocess.Popen(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.interface",
                "color-scheme",
                f"prefer-{self.current_theme}",
            ]
        )
        if symlink:
            subprocess.Popen(
                ["ln", "-sf", filepath, f"{Path.home()}/.cache/current_wallpaper"]
            )
        time.sleep(0.3)
        self.reload_gtk_theme()

    def reload_gtk_theme(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{Path.home()}/.config/gtk-4.0/colors.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )
