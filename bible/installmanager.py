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
        'module_installed': (GObject.SIGNAL_RUN_FIRST, None, ())
        'sources_refreshed': (GObject.SIGNAL_RUN_FIRST, None, ())
        'disclaimer_confirmed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        GObject.GObject.__init__(self)
        self.install_manager = InstallMgr()

    def refresh_source_list(self):
        r =  self.install_manager.refreshRemoteSourceConfiguration()
        if (r != 0):
            return False
        self.emit('sources-refreshed')
        return True

    def get_source_list(self):
        return self.install_manager.sources

    def get_user_disclaimer_confirmed(self):
        return self.install_manager.isUserDisclaimerConfirmed()

    def set_user_disclaimer_confirmed(self, confirmed):
        self.install_manager.setUserDisclaimerConfirmed()
        if confirmed:
            self.emit('disclaimer_confirmed')
