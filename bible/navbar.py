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

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from gettext import gettext as _

class NavBar(Gtk.Revealer):

    def __init__(self):
        self.css = b"""
            .bible-navbar GtkToolbar {
                border: none;
                border-radius: 4px;
                background-color: #333;
                background-image: none;
            }
            .bible-navbar GtkLabel {
                color: #fff;
            }
            .bible-navbar GtkImage {
                color: alpha (#fff, 0.8);
            }
            .bible-navbar GtkToolButton {
                color: #fff;
                background-color: transparent;
            }
        """

        Gtk.Revealer.__init__(self,
            margin=12,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.END)
        self.setup_widgets()
        self.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.show_all()

    def setup_widgets(self):
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(self.css)

        context = self.get_style_context()
        screen = self.get_screen()
        context.add_class('bible-navbar')
        context.add_provider_for_screen(screen, self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.first_button = Gtk.ToolButton()
        self.first_button.set_icon_name('go-first-symbolic')

        self.prev_button = Gtk.ToolButton()
        self.prev_button.set_icon_name('go-previous-symbolic')

        self.label = Gtk.Label.new_with_mnemonic('0/0')
        self.toolbar_label = Gtk.ToolItem()
        self.toolbar_label.add(self.label)

        self.next_button = Gtk.ToolButton()
        self.next_button.set_icon_name('go-next-symbolic')

        self.last_button = Gtk.ToolButton()
        self.last_button.set_icon_name('go-last-symbolic')

        self.toolbar = Gtk.Toolbar()
        self.toolbar.set_icon_size(Gtk.IconSize.SMALL_TOOLBAR)

        self.toolbar.insert(self.first_button, -1)
        self.toolbar.insert(self.prev_button, -1)
        self.toolbar.insert(self.toolbar_label, -1)
        self.toolbar.insert(self.next_button, -1)
        self.toolbar.insert(self.last_button, -1)

        self.add(self.toolbar)

    def show_navbar(self):
        if not self.props.child_revealed:
            self.set_reveal_child(True)

    def hide_navbar(self):
        if self.props.child_revealed:
            self.set_reveal_child(False)
