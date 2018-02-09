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

from gi.repository import Gtk, Gio, GLib
from bible.library import Library
from bible.booklist import BookList
from bible.passageview import PassageView
from bible.navbar import NavBar
from bible.modulelist import ModuleList
from bible.welcome import Welcome
from bible.installdialog import InstallDialog
from bible.installmanager import InstallManager

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
        self.library.connect('reference-changed', self._on_reference_changed)

        self.setup_widgets()

        self.show_all()
        self.restore_saved_module()
        self.restore_saved_passage()

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

    def restore_saved_pane_position(self):
        position = self.settings.get_value('pane-position')
        if (isinstance(position, int)):
            self.paned_view.set_position(position)

    def restore_saved_module(self):
        active_module = self.settings.get_string('module')
        if (isinstance(active_module, str)
            & self.library.has_module(active_module)):
            self.module_list.set_active_id(active_module)
        else:
            self.module_list.set_active(0)

    def restore_saved_passage(self):
        location = self.settings.get_value('passage')
        if(len(location) == 3 and
            isinstance(location[0], int) and
            isinstance(location[1], int) and
            isinstance(location[2], int)):
            self.library.set_testament(location[0])
            self.library.set_book(location[1])
            self.library.set_chapter(location[2])

    def setup_widgets(self):
        self.module_list = ModuleList(self.library)
        self.module_list.connect('changed', self._on_module_selected)

        install_button = Gtk.Button.new_from_icon_name('document-import', Gtk.IconSize.LARGE_TOOLBAR)
        install_button.connect('clicked', self._on_install_button_pressed)

        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_title('Bible')
        self.header.pack_start(self.module_list)
        self.header.pack_end(install_button)
        self.set_titlebar(self.header)

        self.book_list = BookList(self.library)

        self.paned_view = Gtk.Paned(position=160)
        self.paned_view.set_size_request(700, 400)
        self.restore_saved_pane_position()

        self.scrolled = Gtk.ScrolledWindow(None, None)
        self.scrolled.add(self.book_list)
        self.scrolled.set_size_request(150, -1)

        self.passage_view = PassageView(self.library)

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

        self.welcome = Welcome()

        self.stack = Gtk.Stack()
        self.stack.set_size_request(600, -1)
        self.stack.add_named(self.overlay, 'passage-view')
        self.stack.add_named(self.welcome, 'welcome')

        self.paned_view.pack1(self.scrolled, True, False)
        self.paned_view.pack2(self.stack, True, False)
        self.settings.bind('pane-position',
            self.paned_view,
            'position',
            Gio.SettingsBindFlags.DEFAULT)

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

    def _on_install_button_pressed(self, button):
        install_manager = InstallManager(self.library)
        install_dialog = InstallDialog(self, install_manager)

    def _on_window_state_event(self, widget, event):
        self.settings.set_boolean('window-maximized',
                'GDK_WINDOW_STATE_MAXIMIZED' in
                event.new_window_state.value_names)

    def _on_reference_changed(self, library):
        self.header.set_title(library.get_book_name())
        self.update_navbar_label()
        self.settings.set_value('passage',
                                GLib.Variant('ai',[library.get_testament(),
                                                   library.get_book(),
                                                   library.get_chapter()]))

    def _on_module_selected(self, selection):
        active = self.module_list.get_active_id()
        if ((self.module_list.empty) &
            (self.stack.get_visible_child_name() == 'passage-view')):
            self.stack.set_visible_child_name('welcome')
        elif ((self.module_list.empty == False) &
            (self.stack.get_visible_child_name() == 'welcome')):
            self.stack.set_visible_child_name('passage-view')

        self.library.set_module(active)

        if self.library.get_passage_valid() != True:
            p = self.library.get_first_valid_passage()
            self.library.set_reference(p[0], p[1], p[2], 1)
        self.settings.set_value('module', GLib.Variant('s', active))

    def _on_navbar_first_clicked(self, button):
        self.library.set_chapter(1)
        self.update_navbar_label()

    def _on_navbar_prev_clicked(self, button):
        self.library.decrement_chapter()
        self.update_navbar_label()

    def _on_navbar_next_clicked(self, button):
        self.library.increment_chapter()
        self.update_navbar_label()

    def _on_navbar_last_clicked(self, button):
        self.library.set_chapter(self.library.get_chapter_max())
        self.update_navbar_label()
