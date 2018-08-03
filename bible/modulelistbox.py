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

class ModuleListBox(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self.set_sort_func(self._sort_func, None)
        self.show_all()

    def _sort_func(self, row1, row2, user_data):
        if row1.installed and not row2.installed:
            return -1
        if not row1.installed and row2.installed:
            return 1
        if row1.get_name() < row2.get_name():
            return -1
        elif row1.get_name() == row2.get_name():
            return 0
        else:
            return 1
