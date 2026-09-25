from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

KEEP_COLUMNS = [
    "station",
    "obtime",
    "longitude",
    "latitude",
    "tmpf",
    "dwpf",
    "drct",
    "sknt",
    "gust",
    "relh",
    "tfs0",
    "tfs0_text",
]

NUMERIC_COLUMNS = ["tmpf", "dwpf", "drct", "sknt", "gust", "relh", "tfs0"]
INVALID_LABELS = {"Other", "Error", "No Report", "-99", "nan", "NaN"}

LABEL_MAP = {
    "Dry": "Dry",
    "Trace Moisture": "Wet",
    "Wet": "Wet",
    "Moist": "Wet",
    "Damp": "Wet",
    "Chemically Wet": "Wet",
    "Chemical Wet": "Wet",
    "Frost": "Ice/Snow",
    "Ice": "Ice/Snow",
    "Ice Watch": "Ice/Snow",
    "Ice Warning": "Ice/Snow",
    "Snow": "Ice/Snow",
    "Snow Watch": "Ice/Snow",
    "Snow Warning": "Ice/Snow",
    "Snow/Ice Watch": "Ice/Snow",
    "Snow/Ice Warning": "Ice/Snow",
}


def normalize_label_series(series: pd.Series) -> pd.Series:
    """Normalize common spelling variants used in the RWIS labels."""
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .replace(
            {
                "Chemical Wet": "Chemically Wet",
                "chemical wet": "Chemically Wet",
                "Chemically wet": "Chemically Wet",
                "chemically wet": "Chemically Wet",
            }
        )
    )


def build_year_clean_dataset(raw_path: Path, output_dir: Path) -> tuple[dict, pd.DataFrame, pd.Series]:
    year = int(raw_path.stem.split("_")[-1])

    raw_df = pd.read_csv(raw_path, usecols=["station", "obtime"], low_memory=False)
    n_raw = len(raw_df)

    df = pd.read_csv(
        raw_path,
        usecols=KEEP_COLUMNS,
        dtype={"tfs0_text": str},
        low_memory=False,
    )

    other_by_station = (
        df["tfs0_text"].eq("Other").groupby(df["station"]).agg(["mean", "sum"]).reset_index()
    )
    other_by_station["year"] = year

    df = df.drop_duplicates(subset=["station", "obtime"]).copy()
    df["obtime"] = pd.to_datetime(df["obtime"], utc=True)
    df[NUMERIC_COLUMNS] = df[NUMERIC_COLUMNS].replace(-99, np.nan)

    df["tfs0_text"] = normalize_label_series(df["tfs0_text"])
    df = df[df["tfs0_text"].notna()].copy()
    df["tfs0_text"] = df["tfs0_text"].replace({label: np.nan for label in INVALID_LABELS})
    df = df[df["tfs0_text"].notna()].copy()

    df["label"] = df["tfs0_text"].map(LABEL_MAP)
    df = df[df["label"].notna()].copy()

    df["station"] = df["station"].astype("string")
    df["tfs0_text"] = df["tfs0_text"].astype("string")
    df["label"] = df["label"].astype("string")

    df["obtime_year"] = df["obtime"].dt.year
    df["obtime_month"] = df["obtime"].dt.month
    df["obtime_day"] = df["obtime"].dt.day
    df["obtime_hour"] = df["obtime"].dt.hour
    df["obtime_minute"] = df["obtime"].dt.minute

    output_path = output_dir / f"rwis_{year}_clean.csv"
    df.to_csv(output_path, index=False)

    class_counts = df["tfs0_text"].value_counts().sort_values(ascending=False)
    summary = {
        "year": year,
        "raw_rows": n_raw,
        "clean_rows": len(df),
        "stations": df["station"].nunique(),
        "first_observation": df["obtime"].min(),
        "last_observation": df["obtime"].max(),
    }

    return summary, other_by_station, class_counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean per-year RWIS data into training-ready CSV files.")
    parser.add_argument("--dataset-dir", type=Path, default=Path("dataset"), help="Directory containing raw RWIS TXT files.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for cleaned CSV outputs; defaults to dataset/clean.")
    args = parser.parse_args()

    dataset_dir = args.dataset_dir
    output_dir = args.output_dir or dataset_dir / "clean"
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_files = sorted(dataset_dir.glob("rwis_data_*.txt"))
    if not raw_files:
        raise FileNotFoundError(f"No raw RWIS files found in {dataset_dir!s}")

    summaries: list[dict] = []
    other_by_station_frames: list[pd.DataFrame] = []
    class_counts_by_year: dict[int, pd.Series] = {}

    for raw_path in raw_files:
        summary, other_by_station, class_counts = build_year_clean_dataset(raw_path, output_dir)
        summaries.append(summary)
        other_by_station_frames.append(other_by_station)
        class_counts_by_year[int(raw_path.stem.split("_")[-1])] = class_counts

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(output_dir / "rwis_yearly_summary.csv", index=False)

    if other_by_station_frames:
        pd.concat(other_by_station_frames, ignore_index=True).to_csv(output_dir / "other_by_station.csv", index=False)

    if class_counts_by_year:
        labels = sorted({label for counts in class_counts_by_year.values() for label in counts.index})
        count_table = pd.DataFrame({"label": labels})
        for year, counts in sorted(class_counts_by_year.items()):
            count_table[str(year)] = count_table["label"].map(counts).fillna(0).astype(int)
        count_table.to_csv(output_dir / "rwis_yearly_class_counts.csv", index=False)

    print(summary_df)
    print("\nCleaned files saved to:", output_dir)


if __name__ == "__main__":
    main()