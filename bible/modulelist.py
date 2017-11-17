
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib, GObject

from gettext import gettext as _

class ModuleList(Gtk.ComboBox):

    def __init__(self):
        Gtk.ComboBox.__init__(self)

        renderer = Gtk.CellRendererText()
        self.pack_start(renderer, True)
        self.add_attribute(renderer, 'text', 1)

        #renderer = Gtk.CellRendererText()
        #self.pack_start(renderer, True)
        #self.add_attribute(renderer, 'text', 2)

        self._list_store = Gtk.ListStore(int, str, str)
        self.set_model(self._list_store)

        self.set_id_column(1)

        self.show_all()

    def add_module(self, index, name, description):
        self._list_store.append([index, name, description])