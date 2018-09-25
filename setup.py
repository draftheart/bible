#!/usr/bin/python3

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

import glob, os
from distutils.core import setup
from distutils.command.install_data import install_data

inst_path = '/usr/share/com.github.draftheart.bible/bible'

inst_data = [('/usr/share/applications', ['data/com.github.draftheart.bible.desktop']),
                ('/usr/share/metainfo', ['data/com.github.draftheart.bible.appdata.xml']),
                ('/usr/share/icons/hicolor/16x16/apps',['data/icons/16/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/24x24/apps',['data/icons/24/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/32x32/apps',['data/icons/32/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/48x48/apps',['data/icons/48/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/64x64/apps',['data/icons/64/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/128x128/apps',['data/icons/128/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/16x16@2/apps',['data/icons/16/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/24x24@2/apps',['data/icons/24/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/32x32@2/apps',['data/icons/32/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/48x48@2/apps',['data/icons/48/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/64x64@2/apps',['data/icons/64/com.github.draftheart.bible.svg']),
                ('/usr/share/icons/hicolor/128x128@2/apps',['data/icons/128/com.github.draftheart.bible.svg']),
                ('/usr/share/glib-2.0/schemas', ['data/com.github.draftheart.bible.gschema.xml']),
                ('/usr/local/lib/python3.5/dist-packages', ['dist-packages/Sword.py']),
                ('/usr/local/lib/python3.5/dist-packages', ['dist-packages/_Sword.so']),
                (inst_path,['bible/__init__.py']),
                (inst_path,['bible/application.py']),
                (inst_path,['bible/booklist.py']),
                (inst_path,['bible/library.py']),
                (inst_path,['bible/modulelist.py']),
                (inst_path,['bible/navbar.py']),
                (inst_path,['bible/passageview.py']),
                (inst_path,['bible/window.py'])]

class post_install(install_data):
    def run(self):
        install_data.run(self)
        print('Compiling gsettings schemas...')
        os.system('glib-compile-schemas /usr/share/glib-2.0/schemas')

setup(name='Bible',
      version='1.0.0',
      author='Dane Henson',
      description='The Bible Reader for elementary OS',
      url='https://github.com/draftheart/bible',
      license='GNU GPL3',
      scripts=['com.github.draftheart.bible'],
      packages=['bible'],
      data_files=inst_data,
      cmdclass={'install_data': post_install})
