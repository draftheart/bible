from gi.repository import Gtk, Gio, GLib
from bible.library import Library
from bible.booklist import BookList
from bible.passageview import PassageView
from bible.navbar import NavBar
from bible.modulelist import ModuleList

import gi
gi.require_version('Gtk', '3.0')


class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title='Bible')

        self.settings = Gio.Settings.new('com.github.dahenson.bible')
        self.set_size_request(300, 200)
        self.set_default_size(200, 100)

        self.restore_saved_size()

        self.window_size_update_timeout = None
        self.connect('window-state-event', self._on_window_state_event)
        self.connect('configure-event', self._on_configure_event)

        self.library = Library()

        self.module_list = ModuleList()
        for mod in self.library.bibles:
            self.module_list.add_module(mod[0], mod[1], mod[2])

        self.module_list.set_active(0)
        self.module_list.connect('changed', self._on_module_selected)

        active_module = self.settings.get_value('module')
        self.module_list.set_active(active_module)

        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_title('Bible')
        self.header.pack_start(self.module_list)
        self.set_titlebar(self.header)

        self.setup_widgets()

        self.update_navbar_label()
        self.refresh_book_list()
        self.refresh_view()
        self.show_all()

    def refresh_book_list(self):
        self.book_list.set_selected(self.library.get_testament(),
                                     self.library.get_book(),
                                     self.library.get_chapter())

    def refresh_view(self):
        self.header.set_title(self.library.get_book_name())
        self.passage_view.load_html(self.library.render_chapter())

    def restore_saved_size(self):
        size_setting = self.settings.get_value('window-size')
        if (isinstance(size_setting[0], int) and
                isinstance(size_setting[1], int)):
            self.resize(size_setting[0], size_setting[1])

        position_setting = self.settings.get_value('window-position')
        if (len(position_setting) == 2 and
                isinstance(position_setting[0], int) and
                isinstance(position_setting[1], int)):
            self.move(position_setting[0], position_setting[1])

        if self.settings.get_value('window-maximized'):
            self.maximize()

    def setup_widgets(self):
        self.book_list = BookList()
        self.book_select = self.book_list.get_selection()
        self.book_list.connect('row-activated', self._on_book_selected)
        self.paned_view = Gtk.Paned(position=200)

        self.scrolled = Gtk.ScrolledWindow(None, None)
        self.scrolled.add(self.book_list)

        self.passage_view = PassageView()

        self.navbar = NavBar()
        self.navbar.first_button.connect('clicked',
                                          self._on_navbar_first_clicked)
        self.navbar.prev_button.connect('clicked',
                                         self._on_navbar_prev_clicked)
        self.navbar.next_button.connect('clicked',
                                         self._on_navbar_next_clicked)
        self.navbar.last_button.connect('clicked',
                                         self._on_navbar_last_clicked)

        self.overlay = Gtk.Overlay()
        self.overlay.add_overlay(self.passage_view)
        self.overlay.add_overlay(self.navbar)
        self.navbar.show_navbar()
        self.overlay.set_overlay_pass_through(self.navbar, True)

        self.paned_view.add1(self.scrolled)
        self.paned_view.add2(self.overlay)

        self.add(self.paned_view)

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

    def update_navbar_label(self):
        self.navbar.label.set_text('{}/{}'.format(self.library.get_chapter(),
                self.library.get_chapter_max()))

    def _on_configure_event(self, widget, event):
        if self.window_size_update_timeout is None:
            self.window_size_update_timeout = GLib.timeout_add(500,
                    self.store_window_size_and_position, widget)

    def _on_window_state_event(self, widget, event):
        self.settings.set_boolean('window-maximized',
                'GDK_WINDOW_STATE_MAXIMIZED' in
                event.new_window_state.value_names)

    def _on_book_selected(self, tree_view, path, column):
        model, treeiter = self.book_select.get_selected()
        if (treeiter is not None):
            if (model[treeiter][1] != 0) and (model[treeiter][2] != 0):
                self.library.set_testament(model[treeiter][0])
                self.library.set_book(model[treeiter][1])
                self.library.set_chapter(model[treeiter][2])
                self.refresh_view()
            if (model[treeiter][1] == 0) or (model[treeiter][2] == 0):
                if tree_view.row_expanded(path):
                    tree_view.collapse_row(path)
                else:
                    tree_view.expand_row(path, False)
        self.update_navbar_label()

    def _on_module_selected(self, selection):
        active = self.module_list.get_active_id()
        self.library.set_module(active)
        self.settings.set_value('module', GLib.Variant("i", active))
        self.refresh_view()

    def _on_navbar_first_clicked(self, button):
        self.library.set_chapter(1)
        self.update_navbar_label()
        self.refresh_book_list()
        self.refresh_view()

    def _on_navbar_prev_clicked(self, button):
        self.library.decrement_chapter()
        self.update_navbar_label()
        self.refresh_book_list()
        self.refresh_view()

    def _on_navbar_next_clicked(self, button):
        self.library.increment_chapter()
        self.update_navbar_label()
        self.refresh_book_list()
        self.refresh_view()

    def _on_navbar_last_clicked(self, button):
        self.library.set_chapter(self.library.get_chapter_max())
        self.update_navbar_label()
        self.refresh_book_list()
        self.refresh_view()
