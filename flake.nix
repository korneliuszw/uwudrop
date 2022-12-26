{
  description = "A Backend for uwudrop - an anonymous fast, file sharing";
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-22.11;
    flake-utils = {
      url = github:numtide/flake-utils;
    };
    mach-nix.url = github:davhau/mach-nix;
  };
  outputs =
   { self, nixpkgs, flake-utils, mach-nix, ...}@inputs:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        mach = mach-nix.lib.${system};
        pythonEnv = mach.mkPython {
          python = "python310";
          requirements = ''
            django
          '';
        };
      in {
        devShells.default = pkgs.mkShellNoCC {
          packages = [pythonEnv];
          shellHook = ''
            export PYTHONPATH="${pythonEnv}/bin/python"
          '';
        };
      }
    );
}