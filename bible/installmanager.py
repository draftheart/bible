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

from Sword import InstallMgr

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject

class InstallManager(GObject.GObject):

    __gsignals__ = {
        'module_installed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'sources_refreshed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'disclaimer_confirmed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, library):
        GObject.GObject.__init__(self)
        self._install_manager = InstallMgr()
        self._library = library

    def refresh_source_list(self):
        r =  self.install_manager.refreshRemoteSourceConfiguration()
        if (r != 0):
            return False
        self.emit('sources-refreshed')
        return True

    def refresh_install_source(self):
        if self._install_source != None:
            self._install_manager.refreshRemoteSource(self._install_source)
        else:
            return False

    def get_source_list(self):
        source_list = []
        for source in self.install_manager.sources:
            source_list.append(source.c_str())
        return source_list

    def get_user_disclaimer_confirmed(self):
        return self._install_manager.isUserDisclaimerConfirmed()

    def set_install_source(self, source):
        self._install_source = self.install_manager.sources[SWBuf(source)]

    def set_user_disclaimer_confirmed(self, confirmed):
        self._install_manager.setUserDisclaimerConfirmed(confirmed)
        if confirmed:
            self.emit('disclaimer-confirmed')

    def install_local(self, library, file):
        return

    def install_remote(self, library, source, module):
        return
