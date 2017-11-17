
from Sword import VerseKey
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class BookList(Gtk.TreeView):

    def __init__(self):
        Gtk.TreeView.__init__(self,
                              reorderable=False,
                              headers_visible=False,
                              activate_on_single_click=True)

        self._book_store = Gtk.TreeStore(int, int, str)

        book_renderer = Gtk.CellRendererText()
        book_column = Gtk.TreeViewColumn("Book", book_renderer, text=2)
        self.append_column(book_column)

        self.set_model (self._book_store)

        self._populate_list()

        self.expand_all()
        self.show_all()

    def _populate_list(self):
        vk = VerseKey()

        testament_iter = self._book_store.append(None, [1, 0, "Old Testament"])
        for b in range(0, vk.bookCount(1)):
            b += 1
            vk.setBook(b)
            self._book_store.append(testament_iter, [1, b, vk.getBookName()])

        b = 1
        vk.setTestament(2)
        testament_iter = self._book_store.append(None, [2, 0, "New Testament"])
        while b <= vk.bookCount(2):
            self._book_store.append(testament_iter, [2, b, vk.getBookName()])
            b += 1
            vk.setBook(b)

    def set_selected(self, testament, book):
        path_string = '{}:{}'.format(testament-1, book-1)
        path = Gtk.TreePath.new_from_string(path_string)
        self.expand_to_path(path)
        self.set_cursor(path, None, False)