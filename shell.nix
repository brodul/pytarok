{ buildType ? "dev" }:
let
  pkgs = import <nixpkgs> {
    config = { allowUnfree = true; };
    overlays = [];
  };

  dependencies = with pkgs; [
    python310
    poetry

    libffi  # pytest
  ] ++ builtins.getAttr buildType {
    dev = [
      niv
      pre-commit
    ];
    prod = [];
  };
in

pkgs.mkShell {
  name = "dev-shell";
  buildInputs = dependencies;
  shellHook = ''
  '';
}
