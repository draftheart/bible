
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib, GObject, Pango

from gettext import gettext as _

class ModuleList(Gtk.ComboBox):

    def __init__(self):
        Gtk.ComboBox.__init__(self)

        id_text = Gtk.CellRendererText()
        self.pack_start(id_text, True)
        self.add_attribute(id_text, 'text', 1)

        #description_text = Gtk.CellRendererText()
        #description_text.props.ellipsize = Pango.EllipsizeMode.END
        #self.pack_start(description_text, True)
        #self.add_attribute(description_text, 'text', 2)

        self._list_store = Gtk.ListStore(int, str, str)
        self.set_model(self._list_store)

        self.set_tooltip_text("Select Translation")

        self.set_id_column(1)

        self.show_all()

    def add_module(self, index, name, description):
        self._list_store.append([index, name, description])