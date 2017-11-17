gnome = import('gnome')

message('Compiling schemas')
gnome.compile_schemas()
install_data(
  project_id + '.gschema.xml',
  install_dir: 'share/glib-2.0/schemas'
)