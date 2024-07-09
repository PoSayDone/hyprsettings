pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'hyprsettings'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'wallpaper_item.blp',
    'sidebar_item.blp',
    'sidebar_box.blp',
    'window.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('hyprsettings',
  'hyprsettings.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'hyprsettings.in',
  output: 'hyprsettings',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

hyprsettings_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'wallpaper_item.py',
  'sidebar_item.py',
  'sidebar_box.py',
  'utils.py',
]

install_data(hyprsettings_sources, install_dir: moduledir)
