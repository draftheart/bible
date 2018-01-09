project('bible',
    version: '0.1',
    meson_version: '>=0.40.0'
)

gnome = import('gnome')
python = import('python3')
project_id = 'com.github.dahenson.bible'
prefix = get_option('prefix')

message('Looking for dependencies')
python_bin = python.find_python()
if not python_bin.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif

dependency('glib-2.0')
dependency('gtk+-3.0', version:'>=3.14')

message('Getting python install path')
py3_purelib = ''
r = run_command(python_bin.path(), '-c', 'from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix=""))')
if r.returncode() != 0
    py3_purelib = python.sysconfig_path('purelib')
    if not py3_purelib.endswith('site-packages')
        error('Cannot find python install path')
    endif
    pythondir = py3_purelib
else
    pythondir = r.stdout().strip()
endif

bindir = join_paths(prefix, get_option('bindir'))
datadir = join_paths(prefix, get_option('datadir'))
libexecdir = join_paths(prefix, get_option('libexecdir'))
localedir = join_paths(prefix, get_option('localedir'))

pkgdatadir = join_paths(datadir, meson.project_name())

icondir = join_paths(datadir, 'icons', 'hicolor')
schemadir = join_paths(datadir, 'glib-2.0', 'schemas')
bibledir = join_paths(pythondir, 'bible')

install_data('com.github.dahenson.bible', install_dir: bindir)

subdir('bible')
subdir('data')

meson.add_install_script('meson_post_install.py')