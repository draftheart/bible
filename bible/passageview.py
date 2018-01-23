
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
                font-size: 100%;
            }
            .main {
                min-width: 32rem;
                max-width: 100rem;
                word-wrap: break-word;
                line-height: 1.5rem;
                margin: 0 auto 4rem auto;
                padding: 0 1rem 0 1rem;
                columns: 3 28rem;
            }
            span.verse-num {
                color: #999;
                font-size: .75rem;
                font-weight: bold;
                padding-right: .15rem;
                padding-left: .25rem;
                vertical-align: text-top;
            }
            h1 { font-size: 2rem }
            h2 {
                font-size: 1.5rem;
                column-span: all;
            }
            h3 {
                font-size: 1.125rem;
                font-weight: lighter;
            }
            h4 { font-size: 1rem }
            h5 { font-size: .875rem }
            h6 { font-size: .75rem }
            .mx-auto { margin-left: auto; margin-right: auto; }
            .divineName { font-variant: small-caps; }
            .wordsOfJesus { color: #7a0000 }
            .indent1 { margin-left: .5rem }
            .indent2 { margin-left: 1rem }
            .indent3 { margin-left: 2rem }
            .indent4 { margin-left: 4rem }
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