from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_TRAIN_YEARS = list(range(2015, 2023))  # 2015-2022
DEFAULT_VAL_YEARS = [2023, 2024]
DEFAULT_TEST_YEARS = [2025]


def read_cleaned_files(clean_dir: Path) -> pd.DataFrame:
    files = sorted(clean_dir.glob("rwis_*_clean.csv"))
    if not files:
        raise FileNotFoundError(f"No cleaned yearly CSVs found in {clean_dir}")

    dfs = []
    for f in files:
        df = pd.read_csv(f, parse_dates=["obtime"], low_memory=False)
        dfs.append(df)
    all_df = pd.concat(dfs, ignore_index=True)
    return all_df


def split_by_year(df: pd.DataFrame, train_years, val_years, test_years):
    df = df.copy()
    if "obtime_year" not in df.columns:
        df["obtime_year"] = df["obtime"].dt.year

    train_df = df[df["obtime_year"].isin(train_years)].reset_index(drop=True)
    val_df = df[df["obtime_year"].isin(val_years)].reset_index(drop=True)
    test_df = df[df["obtime_year"].isin(test_years)].reset_index(drop=True)

    return train_df, val_df, test_df


def main():
    parser = argparse.ArgumentParser(description="Build combined training dataset and time-based splits from per-year cleaned CSVs.")
    parser.add_argument("--clean-dir", type=Path, default=Path("dataset/clean"), help="Directory with per-year cleaned CSVs")
    parser.add_argument("--out-dir", type=Path, default=Path("dataset/clean"), help="Output directory for combined and split files")
    parser.add_argument("--format", choices=["parquet", "csv"], default="parquet", help="Output file format for combined and split datasets")
    parser.add_argument("--train-years", nargs="*", type=int, default=DEFAULT_TRAIN_YEARS)
    parser.add_argument("--val-years", nargs="*", type=int, default=DEFAULT_VAL_YEARS)
    parser.add_argument("--test-years", nargs="*", type=int, default=DEFAULT_TEST_YEARS)
    args = parser.parse_args()

    clean_dir = args.clean_dir
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Reading cleaned files from", clean_dir)
    df = read_cleaned_files(clean_dir)

    # Ensure obtime is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["obtime"]):
        df["obtime"] = pd.to_datetime(df["obtime"], utc=True)

    # Basic dedupe (station, obtime)
    before = len(df)
    df = df.drop_duplicates(subset=["station", "obtime"]).reset_index(drop=True)
    after = len(df)
    print(f"Dropped {before-after} duplicate station/obtime rows")

    # Ensure time parts exist
    if "obtime_year" not in df.columns:
        df["obtime_year"] = df["obtime"].dt.year
    if "obtime_month" not in df.columns:
        df["obtime_month"] = df["obtime"].dt.month
    if "obtime_day" not in df.columns:
        df["obtime_day"] = df["obtime"].dt.day
    if "obtime_hour" not in df.columns:
        df["obtime_hour"] = df["obtime"].dt.hour
    if "obtime_minute" not in df.columns:
        df["obtime_minute"] = df["obtime"].dt.minute

    combined_path = out_dir / ("rwis_all." + ("parquet" if args.format == "parquet" else "csv"))
    if args.format == "parquet":
        try:
            df.to_parquet(combined_path, index=False)
        except Exception as e:
            print("Parquet write failed, falling back to CSV:", e)
            combined_path = out_dir / "rwis_all.csv"
            df.to_csv(combined_path, index=False)
    else:
        df.to_csv(combined_path, index=False)

    print("Wrote combined dataset to", combined_path)

    train_df, val_df, test_df = split_by_year(df, args.train_years, args.val_years, args.test_years)

    def write_split(name, split_df):
        path = out_dir / f"{name}.{ 'parquet' if args.format=='parquet' else 'csv' }"
        if args.format == "parquet":
            try:
                split_df.to_parquet(path, index=False)
            except Exception:
                split_df.to_csv(path.with_suffix('.csv'), index=False)
                return
        else:
            split_df.to_csv(path, index=False)
        print(f"Wrote {name} ({len(split_df)} rows) to {path}")

    write_split("train", train_df)
    write_split("val", val_df)
    write_split("test", test_df)

    # Save a small manifest
    manifest = {
        "combined_path": str(combined_path),
        "train_years": args.train_years,
        "val_years": args.val_years,
        "test_years": args.test_years,
        "n_total": len(df),
        "n_train": len(train_df),
        "n_val": len(val_df),
        "n_test": len(test_df),
    }
    pd.DataFrame([manifest]).to_json(out_dir / "build_manifest.json", orient="records", lines=False)
    print("Wrote manifest to", out_dir / "build_manifest.json")


if __name__ == "__main__":
    main()
