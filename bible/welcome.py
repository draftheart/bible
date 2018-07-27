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

from gi.repository import Granite

import gi
gi.require_version('Granite', '1.0')

class Welcome(Granite.WidgetsWelcome):
    def __init__(self):
        Granite.WidgetsWelcome.__init__(self,
                                        title='No Bibles Found',
                                        subtitle='Add Bibles to your library.')

        self.append('applications-internet',
                    'Download Bibles',
                    'Download free Bibles from the online library')

        self.show_all()
