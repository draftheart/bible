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
from bible.modulelistbox import ModuleListBox

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Granite

class InstallDialog(Gtk.Window):
    def __init__(self, parent, install_manager):
        Gtk.Window.__init__(self,
            transient_for=parent,
            modal=True,
            window_position = Gtk.WindowPosition.CENTER_ON_PARENT)
        self._install_manager = install_manager
        self.setup_widgets()
        self.show_all()

    def setup_widgets(self):
        self.set_title('Bible Installer')
        alert = Granite.WidgetsAlertView()
        alert.set_title('Warning')
        alert.set_description('If you live in a persecuted country, download Bibles with care.')
        alert.set_icon_name('dialog-warning')
        alert.show_action('I Accept Responsibility')
        alert.connect('action-activated', self._on_action_activated)

        installer = Gtk.Grid()

        self.stack = Gtk.Stack()
        self.stack.add_named(alert, 'alert')
        self.stack.add_named(installer, 'installer')

        self.add(self.stack)
        if self._install_manager.get_user_disclaimer_confirmed():
            self.stack.set_visible_child_name('installer')
        else:
            self.stack.set_visible_child_name('alert')

    def _on_response(self, dialog, response):
        if (response == Gtk.ResponseType.CLOSE):
            dialog.close()

    def _on_action_activated(self, button):
        self._install_manager.set_user_disclaimer_confirmed(True)
        self.stack.set_visible_child_name('installer')
