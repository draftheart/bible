"""
    Copyright (c) 2018 Dane Henson (http://brainofdane.com)

    This file is part of Bible.

    Bible is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Bible is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Bible.  If not, see <http://www.gnu.org/licenses/>.

    Authored by: Dane Henson <thegreatdane@gmail.com>
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GObject

class ModuleRow(Gtk.ListBoxRow):

    def __init__(self, module):
        Gtk.ListBoxRow.__init__(self)
        self.module = module
        self.installed = False
        self.update_available = False
        self.status_icon = Gtk.Image()
        self.setup_widgets()
        self.set_installed(self.installed)
        self.show_all()

    def setup_widgets(self):
        main_grid = Gtk.Grid()
        main_grid.props.column_spacing = 24
        main_grid.props.margin = 6
        main_grid.props.margin_start = 12
        main_grid.props.margin_end = 12

        module_name = Gtk.Label(self.module.getName())
        module_name.get_style_context().add_class('h3')
        module_name.props.valign = Gtk.Align.END
        module_name.props.xalign = 0

        module_description = Gtk.Label(self.module.getDescription())
        module_description.props.valign = Gtk.Align.END
        module_description.props.xalign = 0
        module_description.set_ellipsize(Pango.EllipsizeMode.END)
        module_description.set_tooltip_text(self.module.getDescription())

        info_grid = Gtk.Grid()
        info_grid.props.column_spacing = 12
        info_grid.props.row_spacing = 6
        info_grid.props.valign = Gtk.Align.START
        info_grid.attach(module_name, 0, 0, 1, 1)
        info_grid.attach(module_description, 0, 1, 1, 1)

        status_grid = Gtk.Grid()
        status_grid.props.column_spacing = 6
        status_grid.props.halign = Gtk.Align.CENTER
        status_grid.props.valign = Gtk.Align.CENTER

        self.status_icon.set_from_icon_name('user-offline', Gtk.IconSize.SMALL_TOOLBAR)
        self.status_icon.set_tooltip_text('Not Installed')

        status_grid.add(self.status_icon)

        main_grid.attach(status_grid, 0, 0, 1, 1)
        main_grid.attach(info_grid, 1, 0, 1, 1)
        self.add(main_grid)

    def set_installed(self, installed):

        self.installed = installed

        if installed:
            self.status_icon.set_from_icon_name('user-available', Gtk.IconSize.SMALL_TOOLBAR)
            self.status_icon.set_tooltip_text('Installed')
        else:
            self.status_icon.set_from_icon_name('user-offline', Gtk.IconSize.SMALL_TOOLBAR)
            self.status_icon.set_tooltip_text('Not Installed')

    def set_update_available(self, update_available):

        self.update_available = update_available

        if update_available:
            self.status_icon.set_from_icon_name('user-idle', Gtk.IconSize.SMALL_TOOLBAR)
            self.status_icon.set_tooltip_text('Update Available')
        elif installed and not update_available:
            self.set_installed(True)
        else:
            self.set_installed(False)

    def get_name(self):
        return self.module.getName()

    def get_description(self):
        return self.module.getDescription()
