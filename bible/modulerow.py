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
from gi.repository import Gtk, Pango

class ModuleRow(Gtk.ListBoxRow):
    def __init__(self, name, description):
        Gtk.ListBoxRow.__init__(self)
        self.name = name
        self.description = description
        self.set_tooltip_text(self.description)
        self.setup_widgets()

    def setup_widgets(self):
        main_grid = Gtk.Grid()
        main_grid.props.column_spacing = 24
        main_grid.props.margin = 6
        main_grid.props.margin_start = 12
        main_grid.props.margin_end = 12

        module_name = Gtk.Label(self.name)
        module_name.get_style_context().add_class('h3')
        module_name.props.valign = Gtk.Align.END
        module_name.props.xalign = 0

        module_description = Gtk.Label(self.description)
        module_description.props.valign = Gtk.Align.END
        module_description.props.xalign = 0

        info_grid = Gtk.Grid()
        info_grid.props.column_spacing = 12
        info_grid.props.row_spacing = 6
        info_grid.props.valign = Gtk.Align.START
        info_grid.attach(module_name, 0, 0, 1, 1)
        info_grid.attach(module_description, 0, 1, 1, 1)

        button_grid = Gtk.Grid()
        button_grid.props.hexpand = True
        button_grid.props.column_spacing = 6
        button_grid.props.halign = Gtk.Align.END
        button_grid.props.valign = Gtk.Align.CENTER

        action_button = Gtk.Button.new_with_label('Install')
        button_grid.add(action_button)

        main_grid.attach(info_grid, 0, 0, 1, 1)
        main_grid.attach(button_grid,1,0,1,1)
        self.add(main_grid)
