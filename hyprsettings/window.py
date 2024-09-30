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

from gi.repository import Adw, Gtk, Gio

from hyprsettings.utils import GProperty
from hyprsettings.pages.appearance import AppearancePage
from hyprsettings.pages.network import NetworkPage
from hyprsettings.widgets.sidebar_item import SidebarItem
from hyprsettings.widgets.sidebar_box import SidebarBox


@Gtk.Template(resource_path="/io/github/posaydone/hyprsettings/window.ui")
class HyprsettingsWindow(Adw.ApplicationWindow):
    __gtype_name__ = "HyprsettingsWindow"

    split_view = Gtk.Template.Child()
    sidebar_box: Gtk.Box = Gtk.Template.Child()
    pages_stack = Gtk.Template.Child()
    navigation_page = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pages_stack.connect("notify::visible-child", self.notify_visible_child)
        # self.sidebar_box.connect("network-button-clicked", self.on_network_clicked)
        # self.sidebar_box.connect(
        #     "appearance-button-clicked", self.on_appearance_clicked
        # )

    # def on_network_clicked(self, _):
    #     self.pages_stack.set_visible_child_name("network")
    #
    # def on_appearance_clicked(self, _):
    #     self.pages_stack.set_visible_child_name("appearance")

    def notify_visible_child(self, _, __):
        child = self.pages_stack.get_visible_child()
        page = self.pages_stack.get_page(child)
        self.navigation_page.set_title(page.get_title())
        self.split_view.collapsed = True
        self.split_view.set_show_content(True)
