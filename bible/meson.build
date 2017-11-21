conf = configuration_data()
conf.set('PACKAGE_URL', 'https://github.com/dahenson/bible')
conf.set('DATADIR', datadir)
conf.set('LOCALEDIR', localedir)
conf.set('LIBEXECDIR', libexecdir)
conf.set('VERSION', meson.project_version())

message('Preparing init file')
configure_file(
    input: 'defs.py.in',
    output: 'defs.py',
    configuration: conf,
    install: true,
    install_dir: bibledir
)

shell_sources = [
  'application.py',
  'booklist.py',
  'library.py',
  'modulelist.py',
  'navbar.py',
  'passageview.py',
  'window.py'
]

install_data(shell_sources, install_dir: bibledir)