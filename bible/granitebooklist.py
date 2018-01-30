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

from Sword import VerseKey
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')

from gi.repository import Gtk
from gi.repository import Granite

class GraniteBookList(Granite.WidgetsSourceList):

    def __init__(self):
        Granite.WidgetsSourceList.__init__(self)
        self.old_testament = Granite.WidgetsSourceListExpandableItem()
        self.old_testament.props.name = "Old Testament"
        self.new_testament = Granite.WidgetsSourceListExpandableItem()
        self.new_testament.props.name = "New Testament"
        self.root = Granite.WidgetsSourceListExpandableItem()

        self.root.add(self.old_testament)
        self.root.add(self.new_testament)
        self.set_root(self.root)

        self._populate_list()
        self.show_all()

    def _populate_list(self):
        vk = VerseKey()

        for b in range(0, vk.bookCount(1)):
            b += 1
            vk.setBook(b)
            book = Granite.WidgetsSourceListItem()
            book.props.name = vk.getBookName()
            self.old_testament.add(book)

        b = 1
        vk.setTestament(2)
        while b <= vk.bookCount(2):
            b += 1
            vk.setBook(b)
            book = Granite.WidgetsSourceListItem()
            book.props.name = vk.getBookName()
            self.new_testament.add(book)

    def set_selected(self, testament, book):
        path_string = '{}:{}'.format(testament-1, book-1)