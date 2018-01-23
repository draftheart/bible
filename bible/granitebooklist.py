
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