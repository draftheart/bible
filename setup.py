
#!/usr/bin/python

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