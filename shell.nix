{ buildType ? "dev" }:
let
  pkgs = import <nixpkgs> {
    config = { allowUnfree = true; };
    overlays = [];
  };

  dependencies = with pkgs; [
    stdenv
    git
    python310
    python311
    python312
    poetry
    # python310.pkgs.setuptools
    python310.pkgs.tox

    libffi  # pytest
    graphviz
  ] ++ builtins.getAttr buildType {
    dev = [
      niv
    ];
    prod = [];
  };
in

pkgs.mkShell {
  name = "python-env";
  buildInputs = dependencies;
    # Required for building C extensions
  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";

  shellHook = ''
    # rm -rf .nix-shell
    # mkdir .nix-shell
    # ln -sf ${pkgs.python310} .nix-shell/python
    export SOURCE_DATE_EPOCH=315532800
  '';
}
