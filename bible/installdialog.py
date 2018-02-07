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

from bible.modulerow import ModuleRow

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class InstallDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent)
        self.setup_widgets()
        self.show_all()

    def setup_widgets(self):
        module_list = Gtk.ListBox()
        module1 = ModuleRow('ESV2011', 'This is a really good translation.')
        module2 = ModuleRow('KJV', 'This is a really old translation.')
        module_list.add(module1)
        module_list.add(module2)

        content_area = self.get_content_area()
        content_area.add(module_list)

        self.add_button('Close', Gtk.ResponseType.CLOSE)
        self.connect('response', self._on_response)

    def _on_response(self, dialog, response):
        if (response == Gtk.ResponseType.CLOSE):
            dialog.close()
