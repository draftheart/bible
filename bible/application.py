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
gi.require_version('Granite', '1.0')

from gi.repository import Gtk, GLib, Gio, Gdk, Granite
from gettext import gettext as _

from bible.window import Window

class Application(Gtk.Application):

	def __init__(self):
		Gtk.Application.__init__(self,
									application_id='com.github.draftheart.bible',
									flags=Gio.ApplicationFlags.FLAGS_NONE)
		GLib.set_application_name(_("Bible"))
		GLib.set_prgname('com.github.draftheart.bible')
		self.settings = Gio.Settings.new('com.github.draftheart.bible')

		self._window = None

	def do_startup(self):
		actions = ["quit"]

		for action_name in actions:
			action = Gio.SimpleAction.new(action_name, None)
			action.connect("activate", getattr(self, action_name))
			self.add_action(action)

		Gtk.Application.do_startup(self)

	def quit(self, action=None, param=None):
		self._window.destroy

	def do_activate(self):
		if not self._window:
			self._window = Window(self)

		self._window.present()
