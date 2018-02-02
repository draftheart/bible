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

from gi.repository import Gtk, Pango

class BookList(Gtk.TreeView):

    def __init__(self, library):
        Gtk.TreeView.__init__(self,
                              reorderable=False,
                              headers_visible=False,
                              enable_search=False,
                              enable_grid_lines=Gtk.TreeViewGridLines.NONE,
                              activate_on_single_click=True,
                              halign=Gtk.Align.FILL,
                              valign=Gtk.Align.FILL)

        self.library = library

        self.get_style_context().add_class('source-list')

        self._book_store = Gtk.TreeStore(int, int, int, str, str, str)

        item_column = Gtk.TreeViewColumn()
        item_column.props.expand = True
        self.insert_column(item_column, -1)

        book_cell = Gtk.CellRendererText()
        book_cell.props.ellipsize = Pango.EllipsizeMode.END
        item_column.pack_end(book_cell, False)
        item_column.set_cell_data_func(book_cell, self._book_cell_data_func)

        icon_cell = Gtk.CellRendererPixbuf()
        icon_cell.props.xpad = 2
        item_column.pack_end(icon_cell, False)
        item_column.set_cell_data_func(icon_cell, self._icon_cell_data_func)

        self.set_model (self._book_store)
        self._populate_list()
        self.library.connect('reference-changed', self._on_reference_changed)

        self.show_all()

    def _book_cell_data_func(self, layout, renderer, model, iter, data):
        renderer.props.text = model[iter][5]
        renderer.props.xpad = 6

        if (model[iter][3] == 'testament'):
            renderer.props.weight = Pango.Weight.BOLD
        else:
            renderer.props.weight = Pango.Weight.NORMAL

    def _icon_cell_data_func(self, layout, renderer, model, iter, data):
        renderer.props.visible = True

        if (model[iter][3] == 'book'):
            renderer.props.icon_name = 'library-audiobook'
        elif model[iter][3] == 'chapter':
            renderer.props.icon_name = 'document'
        else:
            renderer.props.icon_name = None
            renderer.props.visible = False

    def _populate_list(self):
        vk = VerseKey()

        testament_iter = self._book_store.append(None, [1, 0, 0, 'testament', '', 'Old Testament'])
        for b in range(1, vk.bookCount(1) + 1):
            vk.setBook(b)
            book_iter = self._book_store.append(testament_iter, [1, b, 0, 'book', 'library-audiobook', vk.getBookName()])
            for c in range(1, vk.getChapterMax() + 1):
                self._book_store.append(book_iter, [1, b, c, 'chapter', 'document', 'Chapter {}'.format(c)])

        vk.setTestament(2)
        testament_iter = self._book_store.append(None, [2, 0, 0, 'testament', '', 'New Testament'])
        for b in range(1, vk.bookCount(2) + 1):
            vk.setBook(b)
            book_iter = self._book_store.append(testament_iter, [2, b, 0, 'book', 'library-audiobook', vk.getBookName()])
            for c in range(1, vk.getChapterMax() + 1):
                self._book_store.append(book_iter, [2, b, c, 'chapter', 'document', 'Chapter {}'.format(c)])

    def do_row_activated(self, path, column):
        model, treeiter = self.get_selection().get_selected()
        if (treeiter is not None):
            if (model[treeiter][1] != 0) and (model[treeiter][2] != 0):
                self.library.set_reference(model[treeiter][0],
                                           model[treeiter][1],
                                           model[treeiter][2],
                                           1)
            if (model[treeiter][1] == 0) or (model[treeiter][2] == 0):
                if self.row_expanded(path):
                    self.collapse_row(path)
                else:
                    self.expand_row(path, False)

    def _on_reference_changed(self, library):
        self.set_selected(library.get_testament(),
                          library.get_book(),
                          library.get_chapter())

    def set_selected(self, testament, book, chapter):
        path_string = '{}:{}:{}'.format(testament-1, book-1, chapter-1)
        path = Gtk.TreePath.new_from_string(path_string)
        self.expand_to_path(path)
        self.set_cursor(path, None, False)
