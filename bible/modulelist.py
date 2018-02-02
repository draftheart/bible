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

from gi.repository import Gtk, Gio, GLib, GObject, Pango

from gettext import gettext as _

class ModuleList(Gtk.ComboBox):

    def __init__(self, library):
        Gtk.ComboBox.__init__(self)
        self.library = library

        self.create_model()
        self.populate_list()
        self.show_all()

    def add_module(self, index, name, description):
        self._list_store.append([index, name, description])

    def create_model(self):
        id_text = Gtk.CellRendererText()
        self.pack_start(id_text, True)
        self.add_attribute(id_text, 'text', 1)

        #description_text = Gtk.CellRendererText()
        #description_text.props.ellipsize = Pango.EllipsizeMode.END
        #self.pack_start(description_text, True)
        #self.add_attribute(description_text, 'text', 2)

        self._list_store = Gtk.ListStore(int, str, str)
        self.set_model(self._list_store)

        self.set_tooltip_text('Select Text')

        self.set_id_column(1)

    def populate_list(self):
        if (len(self.library.bibles) > 0):
            for mod in self.library.bibles:
                self.add_module(mod[0], mod[1], mod[2])
        else:
            self.add_module(999, 'No Texts Loaded', '')
