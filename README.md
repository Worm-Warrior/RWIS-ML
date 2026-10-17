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

## Build training data

Using the `ds3010` Conda environment, materialize the combined and time-based CSV splits:

```bash
/home/harry/anaconda3/envs/ds3010/bin/python scripts/build_training_table.py --format csv
```

This writes `rwis_all.csv`, `train.csv`, `val.csv`, `test.csv`, and `build_manifest.json` into `dataset/clean/`. The default split is 2015-2022 for training, 2023-2024 for validation, and 2025 for testing.

## Build full-information feature-engineering data

To create equivalent time-based splits that retain every raw sensor and observation column, run:

```bash
python wrangle_data.py --dataset-dir dataset --output-dir dataset/testing_features --keep-all-columns
python scripts/build_training_table.py --clean-dir dataset/testing_features --out-dir dataset/testing_features --format csv
```

This writes the full-information `train.csv`, `val.csv`, and `test.csv` files to `dataset/testing_features/`. The files include the raw fields such as `tfs1`, `tfs2`, `tfs3`, `subf`, `pcpn`, `vsby`, and `feel`, alongside the cleaned `label` and derived time columns. The split years remain 2015-2022 for training, 2023-2024 for validation, and 2025 for testing.

## Train the logistic-regression baseline

Run the classifier using the generated split files:

```bash
python scripts/model.py
```

The model uses the numeric sensor features `tmpf`, `dwpf`, `drct`, `sknt`, `gust`, `relh`, and `tfs0`. It imputes missing values, standardizes features, and uses class-balanced multinomial logistic regression. Outputs are written to `model_output/`: `metrics.json`, `test_predictions.csv`, and `logistic_regression.joblib`.

For a bounded smoke test, use `--max-train-rows` and `--max-eval-rows`, for example:

```bash
python scripts/model.py --max-train-rows 10000 --max-eval-rows 3000 --output-dir /tmp/rwis-model-smoke
```

## Notes

- We keep the original `tfs0_text` label alongside the coarse `label` column for traceability.
- We intentionally do not use `tfs1`, `tfs2`, `tfs3`, `subf`, `feel`, or `vsby` in the baseline pipeline.
- The current version is designed for the full-year task and is still intended to be expanded with realtime 2026 evaluation as the semester continues.
