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
from gi.repository import Gtk

class ModuleViewer(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        self._setup_widgets()
        self.module = None
        self.show_all()

    def set_module(self, module):
        self.module = module

    def _setup_widgets(self):
        main_grid = Gtk.Grid()
        main_grid.props.column_spacing = 24
        main_grid.props.margin = 6
        main_grid.props.margin_start = 12
        main_grid.props.margin_end = 12

        self.module_name = Gtk.Label()
        self.module_name.get_style_context().add_class('h2')
        self.module_name.props.valign = Gtk.Align.END
        self.module_name.props.xalign = 0

        self.module_description = Gtk.Label()

        self.module_version = Gtk.Label()

        self.module_about = Gtk.Label()
        self.module_about.set_line_wrap(True)

        main_grid.attach(self.module_name, 0, 0, 1, 1)
        main_grid.attach(self.module_version, 1, 0, 1, 1)
        main_grid.attach(self.module_description, 0, 1, 2, 1)
        main_grid.attach(self.module_about, 0, 2, 2, 1)

        self.add(main_grid)

    def refresh_view(self):
        if self.module != None:
            self.module_name.set_text(self.module.getName())
            self.module_description.set_text(self.module.getDescription())
            self.module_version.set_text(self.module.getConfigEntry('Version'))
            self.module_about.set_text(self.module.getConfigEntry('About'))