{
  description = "RWIS road condition ML project";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      py = pkgs.python312.withPackages (ps: with ps; [
        numpy
        pandas
        scipy
        scikit-learn
        xgboost
        matplotlib
        seaborn
        requests      # pulling data from IEM
        pyarrow       # parquet for caching the 2015-2025 pulls
        jupyterlab
        ipykernel
        pytest
      ]);
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ py pkgs.ruff pkgs.pyright ];
      };
    };
}
