pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'hyprsettings'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'pages/appearance.blp',
    'pages/network.blp',
    'widgets/wallpaper_item.blp',
    'widgets/sidebar_item.blp',
    'widgets/sidebar_box.blp',
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

install_subdir('pages', install_dir: moduledir)
install_subdir('widgets', install_dir: moduledir)

hyprsettings_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'pages/__init__.py',
  'pages/appearance.py',
  'pages/network.py',
  'widgets/__init__.py',
  'widgets/wallpaper_item.py',
  'widgets/sidebar_item.py',
  'widgets/sidebar_box.py',
  'utils.py',
]

install_data(hyprsettings_sources, install_dir: moduledir)
