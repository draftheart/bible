
from Sword import SWMgr, SWModule, SWBuf, VerseKey, OSISHTMLHREF, MarkupFilterMgr

class Library():

    def __init__(self):
        self._filter_manager = MarkupFilterMgr(10, 2)
        self._lib = SWMgr(self._filter_manager)
        self._lib.setGlobalOption('Headings', 'On')

        self._module = self._lib.getModuleAt(0)
        self._vk = VerseKey(self._module.getKey())
        self._make_mod_lists()

        self._html_skele = """
        <!DOCTYPE html>
            <head></head>
            <body>
                <div class="main">
                {}
                </div>
            </body>
        </html
        """

    def _make_mod_lists(self):
        self.bibles = []
        self.commentaries = []

        mods = self._lib.getModules()
        i = 0

        for mod in mods:

            module = self._lib.getModule(mod.c_str())

            if (module.getType() == self._lib.MODTYPE_BIBLES):
                self.bibles.append([i, mod.c_str(), module.getDescription()])

    def set_module(self, module):
        self._module = self._lib.getModule(module)
        self._module.renderText()

    def set_testament(self, testament):
        self._vk.setTestament(testament)

    def get_testament(self):
        return ord(self._vk.getTestament())

    def set_book(self, book):
        self._vk.setBook(book)

    def get_book(self):
        return ord(self._vk.getBook())

    def get_book_name(self):
        return self._vk.getBookName()

    def set_chapter(self, chapter):
        self._vk.setChapter(chapter)

    def get_chapter(self):
        return self._vk.getChapter()

    def get_chapter_max(self):
        return self._vk.getChapterMax()

    def increment_chapter(self):
        self._vk.setChapter(self._vk.getChapter()+1)

    def decrement_chapter(self):
        self._vk.setChapter(self._vk.getChapter()-1)

    def set_verse(self, verse):
        self._vk.setVerse(verse)

    def render_chapter(self):
        buf = '<h1>{} {}</h1>'.format(self.get_book_name(), self.get_chapter())

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

    def strip_chapter(self):
        buf = ''
        for v in range(1, self._vk.getVerseMax()):
            self._vk.setVerse(v)
            self._module.setKey(self._vk)
            text = "{} {} {}".format(self._vk.getVerse(),
                                     self._module.stripText(),
                                     "<br />"
            )
            buf = buf + text

        return buf

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