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
        main_grid.props.expand = True
        main_grid.props.column_spacing = 12
        main_grid.props.halign = Gtk.Align.FILL
        main_grid.props.margin = 24

        banner_grid = Gtk.Grid()
        banner_grid.props.hexpand = True
        banner_grid.props.vexpand = False
        banner_grid.props.column_spacing = 12

        self.module_name = Gtk.Label()
        self.module_name.get_style_context().add_class('h1')
        self.module_name.props.valign = Gtk.Align.CENTER
        self.module_name.props.xalign = 0

        self.module_version = Gtk.Label()
        self.module_version.props.xalign = 0
        self.module_version.get_style_context().add_class('h3')

        self.module_description = Gtk.Label()
        self.module_description.props.xalign = 0
        self.module_description.props.margin_top = 6
        self.module_description.set_ellipsize(Pango.EllipsizeMode.END)
        self.module_description.get_style_context().add_class('h3')

        about_label = Gtk.Label('About')
        about_label.get_style_context().add_class('h2')
        about_label.props.xalign = 0
        about_label.props.margin_top = 12

        self.module_about = Gtk.Label()
        self.module_about.props.xalign = 0
        self.module_about.props.margin_top = 6
        self.module_about.props.expand = True
        self.module_about.set_line_wrap(True)
        self.module_about.props.valign = Gtk.Align.START
        self.module_about.props.halign = Gtk.Align.START

        self.action_button = Gtk.Button.new_with_label('Install')
        self.action_button.props.valign = Gtk.Align.START
        self.action_button.props.halign = Gtk.Align.END

        banner_grid.attach(self.module_name, 0, 0, 1, 1)
        banner_grid.attach(self.module_version, 1, 0, 1, 1)

        main_grid.attach(banner_grid, 0, 0, 1, 1)
        main_grid.attach(self.action_button, 1, 0, 1, 1)
        main_grid.attach(self.module_description, 0, 1, 2, 1)
        main_grid.attach(about_label, 0, 2, 2, 1)
        main_grid.attach(self.module_about, 0, 3, 2, 1)

        self.add(main_grid)

    def refresh_view(self):
        if self.module != None:
            self.module_name.set_text(self.module.getName())
            self.module_description.set_text(self.module.getDescription())
            self.module_version.set_text(self.module.getConfigEntry('Version'))
            about_text = self.module.getConfigEntry('About')
            about_text = about_text.replace("\\par", '\n')
            self.module_about.set_text(about_text)
