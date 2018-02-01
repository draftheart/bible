#!/usr/bin/python

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

inst_path = '/usr/share/com.github.dahenson.bible/bible'

install_data = [('/usr/share/applications', ['data/com.github.dahenson.bible.desktop']),
                ('/usr/share/metainfo', ['data/com.github.dahenson.bible.appdata.xml']),
                #('/usr/share/icons/hicolor/128x128/apps',['data/com.github.dahenson.bible.svg']),
                ('/usr/share/glib-2.0/schemas', ['data/com.github.dahenson.bible.gschema.xml']),
                ('/usr/local/lib/python2.7/dist-packages', ['dist-packages/Sword.py']),
                ('/usr/local/lib/python2.7/dist-packages', ['dist-packages/_Sword.so']),
                (inst_path,['bible/__init__.py']),
                (inst_path,['bible/application.py']),
                (inst_path,['bible/booklist.py']),
                (inst_path,['bible/library.py']),
                (inst_path,['bible/modulelist.py']),
                (inst_path,['bible/navbar.py']),
                (inst_path,['bible/passageview.py']),
                (inst_path,['bible/window.py'])]

setup(name='Bible',
      version='1.0.0',
      author='Dane Henson',
      description='The Bible Reader for elementary OS',
      url='https://github.com/dahenson/bible',
      license='GNU GPL3',
      scripts=['com.github.dahenson.bible'],
      packages=['bible'],
      data_files=install_data)

print('Compiling gsettings schemas...')
os.system('glib-compile-schemas /usr/share/glib-2.0/schemas')
