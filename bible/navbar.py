
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gettext import gettext as _

class NavBar(Gtk.Revealer):

    def __init__(self):
        Gtk.Revealer.__init__(self,
            margin=12,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.END)
        self._setup_widgets()
        self.show_all()

    def _setup_widgets(self):
        self.first_button = Gtk.Button.new_from_icon_name('go-first-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        self.prev_button = Gtk.Button.new_from_icon_name('go-previous-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        self.label = Gtk.Label.new_with_mnemonic('0/0')
        self.next_button = Gtk.Button.new_from_icon_name('go-next-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        self.last_button = Gtk.Button.new_from_icon_name('go-last-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        self._navbar_box = Gtk.Grid(column_spacing=12)
        self._navbar_box.add(self.first_button)
        self._navbar_box.add(self.prev_button)
        self._navbar_box.add(self.label)
        self._navbar_box.add(self.next_button)
        self._navbar_box.add(self.last_button)

        self._navbar_frame = Gtk.Frame()
        self._navbar_frame.get_style_context().add_class('app-notification')
        self._navbar_frame.add(self._navbar_box)
        self.add(self._navbar_frame)

    def show_navbar(self):
        if not self.props.child_revealed:
            self.set_reveal_child(True)