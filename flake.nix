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
            djangorestframework
            django-guardian
            django-cors-headers
            pyyaml
            uritemplate
            markdown
          '';
        };
      in {
        devShells.backend = pkgs.mkShellNoCC {
          packages = [pythonEnv pkgs.sqlite];
          shellHook = ''
            export PYTHONPATH="${pythonEnv}/bin/python"
          '';
        };
        devShells.frontEnd = pkgs.mkShellNoCC {
          packages = with pkgs; [
            nodejs-19_x
            nodePackages.pnpm
          ];
          shellHook = ''
            export PYTHONPATH="${pythonEnv}/bin/python"
          '';
        };
        devShells.default = pkgs.mkShellNoCC {
          packages = with pkgs; [
            nodejs-19_x
            nodePackages.pnpm
            pythonEnv
            pkgs.sqlite
          ];
          shellHook = ''
            export PYTHONPATH="${pythonEnv}/bin/python"
          '';
        };
      }
    );
}