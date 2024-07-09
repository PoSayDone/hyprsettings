{
  blueprint-compiler,
  desktop-file-utils,
  gobject-introspection,
  lib,
  libadwaita,
  meson,
  ninja,
  python3Packages,
  stdenv,
  wrapGAppsHook4,
  nix-update-script,
}:
stdenv.mkDerivation (finalAttrs: {
  pname = "hyprsettings";
  version = "0.0.1";

  src = ../.;

  pythonPath = with python3Packages; [
    pygobject3
  ];

  buildInputs = [
    libadwaita
    (python3Packages.python.withPackages (_: finalAttrs.pythonPath))
  ];

  nativeBuildInputs = [
    blueprint-compiler
    desktop-file-utils
    gobject-introspection
    meson
    ninja
    python3Packages.wrapPython
    wrapGAppsHook4
  ];

  dontWrapGApps = true;

  postFixup = ''
    makeWrapperArgs+=("''${gappsWrapperArgs[@]}")
    wrapPythonPrograms "$out/bin" "$out" "$pythonPath"
  '';

  passthru = {
    updateScript = nix-update-script {};
  };

  meta = with lib; {
    description = "Settings for hyprland";
    mainProgram = "hyprsettings";
    license = licenses.gpl3Plus;
  };
})
