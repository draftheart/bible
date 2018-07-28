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

from gi.repository import GObject
from Sword import SWMgr, SWModule, SWBuf, VerseKey, OSISHTMLHREF, MarkupFilterMgr

import os, gi
gi.require_version('Gtk', '3.0')

class Library(GObject.GObject):

    __gsignals__ = {
        'reference_changed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'module_changed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        GObject.GObject.__init__(self)
        self._filter_manager = MarkupFilterMgr(10, 2)
        self.setup_settings_path()
        settings_path = os.path.join(os.path.expanduser('~'), '.sword')
        self._lib = SWMgr(settings_path, True, self._filter_manager)
        self._lib.setGlobalOption('Headings', 'On')

        self._vk = VerseKey()
        self._module = None

        self._make_mod_lists()
        if len(self.bibles) > 0:
            self._module = self._lib.getModuleAt(0)
            self._vk = VerseKey(self._module.getKey())

        self._html_skele = """
        <!DOCTYPE html>
            <head></head>
            <body>
                <div class="main">
                {}
                </div>
            </body>
        </html>
        """

    def setup_settings_path(self):
        mods_path = os.path.join(os.path.expanduser('~'), '.sword', 'mods.d')
        if not os.path.isdir(mods_path):
            os.mkdir(mods_path)

    def get_book(self):
        return ord(self._vk.getBook())

    def get_book_name(self):
        return self._vk.getBookName()

    def get_chapter(self):
        return self._vk.getChapter()

    def get_chapter_max(self):
        return self._vk.getChapterMax()

    def get_entry_attribute(self, level1, level2, level3):
        l1 = SWBuf(level1)
        l2 = SWBuf(level2)
        l3 = SWBuf(level3)

        self._module.renderText()
        m = self._module.getEntryAttributesMap()

        if m.has_key(l1):
            n = m[l1]
            if n.has_key(l2):
                o = n[l2]
                if o.has_key(l3):
                    i = o[l3]
                    return i.c_str()
        return ''

    def get_entry_has_attribute(self, level1):
        l1 = SWBuf(level1)
        m = self._module.getEntryAttributesMap()

        return m.has_key(l1)

    def get_first_valid_passage(self):
        vk = VerseKey()
        if (self._module != None):
            for t in range(1, 3):
                vk.setTestament(t)
                for b in range(1, vk.bookCount(t) + 1):
                    vk.setBook(b)
                    for c in range(1, vk.getChapterMax() + 1):
                        vk.setChapter(c)
                        if self._module.hasEntry(vk):
                            return [t, b, c]
        return [1, 1, 1]

    def get_manager(self):
        return self._lib

    def get_passage_valid(self):
        if (self._module != None):
            return self._module.hasEntry(self._vk)

    def get_testament(self):
        return ord(self._vk.getTestament())

    def has_module(self, module):
        return None != self._lib.getModule(module)

    def has_passage(self, vk):
        if (self._module != None):
            return self._module.hasEntry(vk)
        return False

    def reload_modules(self):
        return self._lib.Load()

    def set_book(self, book):
        self._vk.setBook(book)
        self.emit('reference_changed')

    def set_chapter(self, chapter):
        self._vk.setChapter(chapter)
        self.emit('reference_changed')

    def set_manager(self, manager):
        self._lib = manager

    def set_module(self, module):
        self._module = self._lib.getModule(module)
        if (self._module != None):
            self._module.renderText()
        self.emit('module_changed')

    def set_reference(self, testament, book, chapter, verse):
        self._vk.setTestament(testament)
        self._vk.setBook(book)
        self._vk.setChapter(chapter)
        self._vk.setVerse(verse)
        self.emit('reference_changed')

    def set_testament(self, testament):
        self._vk.setTestament(testament)
        self.emit('reference_changed')

    def set_verse(self, verse):
        self._vk.setVerse(verse)
        self.emit('reference_changed')

    def increment_chapter(self):
        self._vk.setChapter(self._vk.getChapter()+1)
        self.emit('reference_changed')

    def decrement_chapter(self):
        self._vk.setChapter(self._vk.getChapter()-1)
        self.emit('reference_changed')

    def render_chapter(self):
        buf = '<h2>{} {}</h2>'.format(self.get_book_name(), self.get_chapter())

        if self._module != None:
            for v in range(1, self._vk.getVerseMax()):
                self._vk.setVerse(v)
                self._module.setKey(self._vk)
                verse_text = self._module.renderText().c_str()

                heading = self.get_entry_attribute('Heading', 'Preverse', '0')
                heading = self._module.renderText(heading).c_str()

                text = '{}<span class="verse-num">{}</span> {} '\
                    .format(heading, v, verse_text)
                buf = buf + text
            return self._html_skele.format(buf)

        return ""

    def strip_chapter(self):
        buf = ''

        if self._module != None:
            for v in range(1, self._vk.getVerseMax()):
                self._vk.setVerse(v)
                self._module.setKey(self._vk)
                text = "{} {} {}".format(self._vk.getVerse(),
                                         self._module.stripText(),
                                         "<br />"
                )
                buf = buf + text

        return buf

    def _make_mod_lists(self):
        self.bibles = []
        mods = self._lib.getModules()

        i = 0
        for mod in mods:
            module = self._lib.getModule(mod.c_str())
            if (module.getType() == self._lib.MODTYPE_BIBLES):
                self.bibles.append([i, mod.c_str(), module.getDescription()])
