# RWIS Road Condition Prediction

This project predicts road surface condition using Iowa DOT RWIS sensor data from the Iowa Environmental Mesonet.

## Project scope

- Raw data lives in `dataset/`
- We use the `tfs0` sensor as the main label/feature pair
- We keep a three-class target:
  - `Dry`
  - `Wet`
  - `Ice/Snow`
- We split by time rather than randomly, so adjacent observations from the same station do not leak across train/validation/test sets
- We continue to collect newer data during the semester to test on recent unseen observations

## Raw dataset

The raw files are downloaded as full-calendar-year text files in `dataset/`:

- `dataset/rwis_data_2015.txt`
- `dataset/rwis_data_2016.txt`
- ...
- `dataset/rwis_data_2025.txt`

The project uses the full-year window, not just Aug-Dec.

## Canonical cleaning pipeline

The main script is `wrangle_data.py`.

It is the source of truth for the cleaning workflow and should be the script used to generate each cleaned yearly CSV. It does the following:

1. Reads each annual raw RWIS file
2. Restricts to the relevant columns only
3. Removes duplicate station/time rows
4. Parses `obtime` as UTC timestamps
5. Replaces numeric `-99` sentinel values with `NaN`
6. Normalizes label spelling variants such as `Chemical Wet` -> `Chemically Wet`
7. Removes invalid labels such as `Other`, `Error`, `No Report`, and `-99`
8. Maps the original condition labels into the three coarse classes:
   - `Dry`
   - `Wet`
   - `Ice/Snow`
9. Saves a cleaned per-year CSV in `dataset/clean/`
10. Writes diagnostics such as yearly summaries and station-level "Other" rates

## Output files

The cleaned files are saved into the shared `dataset/clean/` directory, using this naming convention:

- `dataset/clean/rwis_2015_clean.csv`
- `dataset/clean/rwis_2016_clean.csv`
- ...
- `dataset/clean/rwis_2025_clean.csv`

Other generated outputs include:

- `dataset/clean/rwis_yearly_summary.csv`
- `dataset/clean/rwis_yearly_class_counts.csv`
- `dataset/clean/other_by_station.csv`

## Run the cleaning pipeline

From the project root:

```bash
python wrangle_data.py
```

Optional arguments:

```bash
python wrangle_data.py --dataset-dir dataset --output-dir dataset/clean
```

## Columns kept for modeling

The cleaned dataset keeps these columns:

- `station`
- `obtime`
- `longitude`
- `latitude`
- `tmpf`
- `dwpf`
- `drct`
- `sknt`
- `gust`
- `relh`
- `tfs0`
- `tfs0_text`
- `label`
- `obtime_year`
- `obtime_month`
- `obtime_day`
- `obtime_hour`
- `obtime_minute`

These time columns are stored separately so the modeling window and feature engineering can be adjusted later without re-reading the raw files.

## Notes

- We keep the original `tfs0_text` label alongside the coarse `label` column for traceability.
- We intentionally do not use `tfs1`, `tfs2`, `tfs3`, `subf`, `feel`, or `vsby` in the baseline pipeline.
- The current version is designed for the full-year task and is still intended to be expanded with realtime 2026 evaluation as the semester continues.
