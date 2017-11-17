
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2
from gettext import gettext as _

class PassageView(Gtk.Grid):

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.props.expand = True

        stylesheet = """
            :root {
                font-family: 'Open Sans', 'sans-serif';
                color: #333;

              --h0: 4.5rem;
              --h1: 3rem;
              --h2: 2.25rem;
              --h3: 1.5rem;
              --h4: 1.125rem;
              --h5: .75rem;

              --lh: calc(4/3);
              --mx: 32em;

              --m1: calc(2/3 * 1em);
              --m2: calc(4/3 * 1em);
              --m3: calc(8/3 * 1em);
              --m4: calc(16/3 * 1em);
              --x1: .5rem;
              --x2: 1rem;
              --x3: 2rem;
              --x4: 4rem;
              --x5: 8rem;
              --x6: 16rem;
            }
            .main {
                max-width: var(--mx);
                word-wrap: break-word;
                margin: var(--m2) auto;
                padding: 0 var(--x2) var(--x4) var(--x2);
                line-height: var(--lh);
            }
            span.verse-num {
                color: #999;
                font-size: var(--h5);
                font-weight: bold;
                padding-right: .15em;
                padding-left: .25em;
                vertical-align: text-top;
            }
            .wordsOfJesus { color: red; }
            .indent1 { margin-left: var(--x1); }
            .indent2 { margin-left: var(--x2); }
            .indent3 { margin-left: var(--x3); }
            .indent4 { margin-left: var(--x4); }
        """
        user_style = WebKit2.UserStyleSheet(stylesheet,
            WebKit2.UserContentInjectedFrames.ALL_FRAMES,
            WebKit2.UserStyleLevel.USER,
            None,
            None)

        content_manager = WebKit2.UserContentManager()
        content_manager.add_style_sheet(user_style)
        self.webview = WebKit2.WebView.new_with_user_content_manager(content_manager)
        self.webview.props.expand = True

        self.webview.connect('context-menu', self._on_context_menu)

        self.add(self.webview)
        self.show_all()

    def load_html(self, html):
        self.webview.load_html(html)

    def _on_context_menu(self, web_view, context_menu, event, hit_test_result):
        items = context_menu.get_items()
        for item in items:
            action = item.get_stock_action()
            if (action == WebKit2.ContextMenuAction.RELOAD)\
            or (action == WebKit2.ContextMenuAction.GO_BACK)\
            or (action == WebKit2.ContextMenuAction.GO_FORWARD)\
            or (action == WebKit2.ContextMenuAction.STOP):
                context_menu.remove(item)