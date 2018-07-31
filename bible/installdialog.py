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
from bible.moduleviewer import ModuleViewer

import threading
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, GLib, Granite

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

        installer = Gtk.Paned(position=210)
        self.module_info = ModuleViewer()
        self.module_info.set_size_request(200, -1)
        self.module_info.connect('action-button-clicked', self._on_moduleviewer_action_activated)

        self.module_list = ModuleListBox()
        self.module_list.connect('row-selected', self._on_module_selected)

        scrolled = Gtk.ScrolledWindow(None, None)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_size_request(200, -1)
        scrolled.add(self.module_list)

        installer.pack1(scrolled, True, False)
        installer.pack2(self.module_info, True, False)

        spinner_grid = Gtk.Grid()
        spinner_grid.props.halign = Gtk.Align.CENTER
        spinner_grid.props.valign = Gtk.Align.CENTER
        self.spinner = Gtk.Spinner()
        spinner_grid.add(self.spinner)

        self.stack = Gtk.Stack()
        self.stack.add_named(alert, 'alert')
        self.stack.add_named(installer, 'installer')
        self.stack.add_named(spinner_grid, 'spinner')
        self.stack.set_size_request(700, 400)

        self.add(self.stack)
        if self._install_manager.get_user_disclaimer_confirmed():
            self.spinner.start()
            self.stack.set_visible_child_name('spinner')
        else:
            self.stack.set_visible_child_name('alert')

        self._install_manager.connect('source-list-refreshed', self._on_source_list_refreshed)
        self._install_manager.connect('modules-refreshed', self._on_modules_refreshed)
        self._install_manager.connect('module-installed', self._on_module_installed)

    def _on_action_activated(self, button):
        self._install_manager.set_user_disclaimer_confirmed(True)
        self.spinner.start()
        self.stack.set_visible_child_name('spinner')
        self._install_manager.refresh_source_list()

    def _on_source_list_refreshed(self, install_manager):
        self._install_manager.set_install_source('CrossWire')
        self._install_manager.refresh_module_list()

    def _on_modules_refreshed(self, install_manager):
        self._refresh_module_list()
        if (self.stack.get_visible_child_name() != 'installer'):
            self.spinner.stop()
            self.stack.set_visible_child_name('installer')

    def _refresh_module_list(self):
        children = self.module_list.get_children()
        for child in children:
            child.destroy()

        mods = self._install_manager.bibles
        for k in mods.keys():
            mod = ModuleRow(k)
            if (mods[k] == self._install_manager.ModStat.SAMEVERSION):
                mod.set_installed(True)
            elif (mods[k] == self._install_manager.ModStat.UPDATED):
                mod.set_installed(True)
                mod.set_update_available(True)
            else:
                mod.set_installed(False)
            self.module_list.add(mod)
        row = self.module_list.get_row_at_index(0)
        if row != None:
            self.module_list.select_row(row)

    def _on_module_installed(self, install_manager):
        self._refresh_module_list()

    def _on_module_selected(self, list_box, row):
        if row != None:
            self._install_manager.set_selected_module(row.module)
            self.module_info.set_module(row.module, row.installed, row.update_available)
            self.module_info.refresh_view()

    def _on_moduleviewer_action_activated(self, module_viewer):
        if not module_viewer.installed:
            self._install_manager.install_selected_module()
        if module_viewer.installed:
            self._install_manager.remove_selected_module()
