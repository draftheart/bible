
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib
from bible.library import Library
from bible.booklist import BookList
from bible.passageview import PassageView
from bible.navbar import NavBar
from bible.modulelist import ModuleList

from gettext import gettext as _

class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title=_("Bible"))

        self.settings = Gio.Settings.new('com.github.dahenson.bible')
        self.set_size_request(300, 200)
        self.set_default_size(200, 100)

        self.restore_saved_size()

        self.window_size_update_timeout = None
        self.connect("window-state-event", self._on_window_state_event)
        self.connect("configure-event", self._on_configure_event)

        self._library = Library()

        self.module_list = ModuleList()
        for mod in self._library.bibles:
            self.module_list.add_module(mod[0], mod[1], mod[2])

        self.module_list.set_active(0)
        self.module_list.connect('changed', self._on_module_selected)

        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_title(_("Bible"))
        self.header.pack_start(self.module_list)
        self.set_titlebar(self.header)

        self._setup_widgets()

        self.update_navbar_label()
        self.refresh_book_list()
        self.refresh_view()
        self.show_all()

    def restore_saved_size(self):
        size_setting = self.settings.get_value('window-size')
        if (isinstance(size_setting[0], int) and
            isinstance(size_setting[1], int)):
            self.resize(size_setting[0], size_setting[1])

        position_setting = self.settings.get_value('window-position')
        if len(position_setting) == 2 \
            and isinstance(position_setting[0], int) \
            and isinstance(position_setting[1], int):
            self.move(position_setting[0], position_setting[1])

        if self.settings.get_value('window-maximized'):
            self.maximize()

    def store_window_size_and_position(self, widget):
        size = widget.get_size()
        self.settings.set_value('window-size',
                                GLib.Variant('ai', [size[0], size[1]]))

        position = widget.get_position()
        self.settings.set_value('window-position',
                                GLib.Variant('ai', [position[0], position[1]]))

        GLib.source_remove(self.window_size_update_timeout)
        self.window_size_update_timeout = None
        return False

    def refresh_view(self):
        self.header.set_title(self._library.get_book_name())
        self._passage_view.load_html(self._library.render_chapter())

    def refresh_book_list(self):
        self._book_list.set_selected(self._library.get_testament(),
                                     self._library.get_book())

    def update_navbar_label(self):
        self._navbar.label.set_text('{}/{}'.format(self._library.get_chapter(),
            self._library.get_chapter_max()))

    def _setup_widgets(self):
        self._book_list = BookList()
        self._book_select = self._book_list.get_selection()
        self._book_list.connect('row-activated', self._on_book_selected)

        self._paned_view = Gtk.Paned(position=200)

        self._scrolled = Gtk.ScrolledWindow(None, None)
        self._scrolled.add(self._book_list)

        self._passage_view = PassageView()

        self._navbar = NavBar()
        self._navbar.first_button.connect('clicked',
                                          self._on_navbar_first_clicked)
        self._navbar.prev_button.connect('clicked',
                                         self._on_navbar_prev_clicked)
        self._navbar.next_button.connect('clicked',
                                         self._on_navbar_next_clicked)
        self._navbar.last_button.connect('clicked',
                                         self._on_navbar_last_clicked)

        self._overlay = Gtk.Overlay()
        self._overlay.add_overlay(self._passage_view)
        self._overlay.add_overlay(self._navbar)
        self._navbar.show_navbar()
        self._overlay.set_overlay_pass_through(self._navbar, True)

        self._paned_view.add1(self._scrolled)
        self._paned_view.add2(self._overlay)

        self.add(self._paned_view)

    def _on_configure_event(self, widget, event):
        if self.window_size_update_timeout is None:
            self.window_size_update_timeout = GLib.timeout_add(500,
                self.store_window_size_and_position,
                widget)

    def _on_window_state_event(self, widget, event):
        self.settings.set_boolean('window-maximized',
            'GDK_WINDOW_STATE_MAXIMIZED' in event.new_window_state.value_names)

    def _on_book_selected(self, tree_view, path, column):
        model, treeiter = self._book_select.get_selected()
        if (treeiter != None):
            if (model[treeiter][1] != 0):
                self._library.set_testament(model[treeiter][0])
                self._library.set_book(model[treeiter][1])
                self.refresh_view()
            if (model[treeiter][1] == 0):
                if tree_view.row_expanded(path):
                    tree_view.collapse_row(path)
                else:
                    tree_view.expand_row(path, True)
        self.update_navbar_label()

    def _on_module_selected(self, selection):
        active = self.module_list.get_active_id()
        self._library.set_module(active)
        self.refresh_view()

    def _on_navbar_first_clicked(self, button):
        self._library.set_chapter(1)
        self.update_navbar_label()
        self.refresh_view()

    def _on_navbar_prev_clicked(self, button):
        self._library.decrement_chapter()
        self.update_navbar_label()
        self.refresh_book_list()
        self.refresh_view()

    def _on_navbar_next_clicked(self, button):
        self._library.increment_chapter()
        self.update_navbar_label()
        self.refresh_book_list()
        self.refresh_view()

    def _on_navbar_last_clicked(self, button):
        self._library.set_chapter(self._library.get_chapter_max())
        self.update_navbar_label()
        self.refresh_view()