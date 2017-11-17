
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')

from gi.repository import Gtk, GLib, Gio, Gdk, Granite
from gettext import gettext as _

from bible.window import Window

class Application(Gtk.Application):

	def __init__(self):
		Gtk.Application.__init__(self,
									application_id='com.github.dahenson.bible',
									flags=Gio.ApplicationFlags.FLAGS_NONE)
		GLib.set_application_name(_("Bible"))
		GLib.set_prgname('com.github.dahenson.bible')
		self.settings = Gio.Settings.new('com.github.dahenson.bible')

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