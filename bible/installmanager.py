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

from Sword import InstallMgr, SWBuf, SWMgr
from bible.async import async_method

import os, gi

gi.require_version('Gtk', '3.0')
from gi.repository import GObject

class InstallManager(GObject.GObject):

    __gsignals__ = {
        'modules_refreshed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'source_list_refreshed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'module_installed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'module_removed': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    class ModStat:
        CIPHERED = InstallMgr.MODSTAT_CIPHERED
        CIPHERKEYPRESENT = InstallMgr.MODSTAT_CIPHERKEYPRESENT
        NEW = InstallMgr.MODSTAT_NEW
        OLDER = InstallMgr.MODSTAT_OLDER
        SAMEVERSION = InstallMgr.MODSTAT_SAMEVERSION
        UPDATED = InstallMgr.MODSTAT_UPDATED

    def __init__(self, library):
        GObject.GObject.__init__(self)
        settings_path = os.path.join(os.path.expanduser('~'), '.sword/InstallMgr')
        self._install_manager = InstallMgr(settings_path)
        self._install_manager.setFTPPassive(True)
        self._library = library
        self._selected_module = None

    @async_method(on_done = lambda self, result, error: self.on_source_list_refreshed(result, error))
    def refresh_source_list(self):
        self._install_manager.refreshRemoteSourceConfiguration()

    @async_method(on_done = lambda self, result, error: self.on_install_sources_refreshed(result, error))
    def refresh_install_source(self):
        if self._install_source != None:
            self._install_manager.refreshRemoteSource(self._install_source)

    @async_method(on_done = lambda self, result, error: self.on_modules_refreshed(result, error))
    def refresh_module_list(self):
        bibles = {}
        if self._library != None and self._install_source != None:
            mods = self._install_manager.getModuleStatus(self._library.get_manager(),
                                                         self._install_source.getMgr())
            modtype_bibles = SWMgr().MODTYPE_BIBLES
            for mod in mods:
                if (mod.getType() == modtype_bibles):
                    bibles[mod] = mods[mod]
        return bibles

    def on_install_sources_refreshed(self, result, error):
        return

    def on_module_installed(self, result, error):
        self._library.reload_modules()
        self.refresh_module_list()
        self.emit('module-installed')

    def on_module_removed(self, result, error):
        self._library.reload_modules()
        self.refresh_module_list()
        self.emit('module-removed')

    def on_modules_refreshed(self, result, error):
        self._library.reload_modules()
        self.bibles = result
        self.emit('modules-refreshed')

    def on_source_list_refreshed(self, result, error):
        self.emit('source-list-refreshed')

    def get_source_list(self):
        source_list = []
        for source in self.install_manager.sources:
            source_list.append(source.c_str())
        return source_list

    def get_user_disclaimer_confirmed(self):
        return self._install_manager.isUserDisclaimerConfirmed()

    def set_install_source(self, source):
        self._install_source = self._install_manager.sources[SWBuf(source)]

    def set_user_disclaimer_confirmed(self, confirmed):
        self._install_manager.setUserDisclaimerConfirmed(confirmed)

    def install_local_module(self, file):
        return

    @async_method(on_done = lambda self, result, error: self.on_module_installed(result, error))
    def install_selected_module(self):
        if self._install_source != None:
            self._install_manager.installModule(self._library.get_manager(),
                '0',
                self.get_module_name(),
                self._install_manager.sources[SWBuf('CrossWire')])
        return

    @async_method(on_done = lambda self, result, error: self.on_module_removed(result, error))
    def remove_selected_module(self):
        if self._install_source != None:
            self._install_manager.removeModule(self._library.get_manager(), self.get_module_name())
        return

    def set_selected_module(self, mod):
        self._selected_module = mod

    def get_module_name(self):
        return self._selected_module.getName()

    def get_module_description(self):
        return self._selected_module.getDescription()

    def get_module_about(self):
        return self._selected_module.getConfigEntry('About')

    def get_module_version(self):
        return self._selected_module.getConfigEntry('Version')
