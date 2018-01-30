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

install_data = [('share/applications', ['data/com.github.dahenson.bible.desktop']),
                #('share/metainfo', ['data/com.github.dahenson.bible.appdata.xml']),
                #('share/icons/hicolor/128x128/apps',['data/com.github.dahenson.bible.svg']),
                ('share/glib-2.0/schemas', ['data/com.github.dahenson.bible.gschema.xml']),
                ('bin/bible',['bible/__init__.py']),
                ('bin/bible',['bible/application.py']),
                ('bin/bible',['bible/booklist.py']),
                ('bin/bible',['bible/library.py']),
                ('bin/bible',['bible/modulelist.py']),
                ('bin/bible',['bible/navbar.py']),
                ('bin/bible',['bible/passageview.py']),
                ('bin/bible',['bible/window.py'])]

setup(  name='Bible',
        version='0.0.1',
        author='Dane Henson',
        description='The Bible Reader for elementary OS',
        url='https://github.com/dahenson/bible',
        license='GNU GPL3',
        scripts=['com.github.dahenson.bible'],
        packages=['bible'],
data_files=install_data)