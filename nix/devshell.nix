{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pygobject3 # Python GTK bindings
    python3Packages.gst-python
    python3Packages.pygobject-stubs
    gtk4
    gobject-introspection
    meson
    ninja
    pkg-config
    libadwaita
  ];
}
