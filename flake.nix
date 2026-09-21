{
  description = "RWIS road condition ML project";

inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
          (final: prev: {
            pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
              (pyFinal: pyPrev: {
                # timing-based test fails in the build sandbox
                backrefs = pyPrev.backrefs.overridePythonAttrs (_: {
                  doCheck = false;
                });
              })
            ];
          })
        ];
      };
      py = pkgs.python3.withPackages (ps: with ps; [
        numpy
        pandas
        scikit-learn
        matplotlib
        seaborn
        requests
        torch
      ]);
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ py pkgs.ruff pkgs.pyright ];
      };
    };
}
