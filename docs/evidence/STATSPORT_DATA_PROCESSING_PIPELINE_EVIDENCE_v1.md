# StatSport Data Processing Pipeline Evidence v1

**Milestone:** Milestone 2 - Data Processing Pipeline  
**Evidence date:** 2026-06-20  
**Source:** Football-Data.co.uk  
**League:** Bundesliga, Germany top division (`D1`)  
**Seasons:** 2020/21, 2021/22, 2022/23, 2023/24, 2024/25  
**Prediction target:** Home / Draw / Away (`H`, `D`, `A`)  
**Fallback target:** Home Win vs Not Home Win (`1`, `0`)

## Purpose

This document records evidence that the Milestone 2 data processing pipeline converts the approved
raw Bundesliga CSV files into a clean, consistent, match-level processed dataset ready for later
feature engineering.

This milestone does not perform feature engineering, rolling aggregation, model training, model
evaluation, notebook work, or visualization.

## Implementation Files

| File | Purpose |
|------|---------|
| `src/statsport/data_processing.py` | Reusable processing functions, validation helpers, target mapping, chronological sorting, and summary helpers. |
| `scripts/process_bundesliga_raw_data.py` | Simple command-line entry point that reads the approved raw files and writes the processed dataset. |
| `tests/test_data_processing.py` | Focused standard-library tests for validation, target mapping, ordering, row preservation, and raw-file immutability. |

## Input Files

| Season | Input path | Rows read |
|--------|------------|-----------|
| 2020/21 | `data/raw/football-data-co-uk_bundesliga_2020-2021.csv` | 306 |
| 2021/22 | `data/raw/football-data-co-uk_bundesliga_2021-2022.csv` | 306 |
| 2022/23 | `data/raw/football-data-co-uk_bundesliga_2022-2023.csv` | 306 |
| 2023/24 | `data/raw/football-data-co-uk_bundesliga_2023-2024.csv` | 306 |
| 2024/25 | `data/raw/football-data-co-uk_bundesliga_2024-2025.csv` | 306 |

All five approved raw files were read from `data/raw/`.

## Output File

```text
data/processed/bundesliga_2020_2025_matches_processed.csv
```

The processed file exists locally and is ignored by git through the repository `.gitignore` rules for
`data/processed/*`.

## Processing Procedure

Run from the repository root:

```bash
python3 scripts/process_bundesliga_raw_data.py
```

The script:

- reads exactly the five approved raw Football-Data.co.uk Bundesliga CSV files;
- validates required raw columns: `Div`, `Date`, `Time`, `HomeTeam`, `AwayTeam`, `FTHG`, `FTAG`,
  `FTR`;
- parses match dates into ISO `YYYY-MM-DD` format;
- normalizes kickoff time to `HH:MM`;
- normalizes home and away team names by trimming whitespace;
- renames full-time goals to explicit processed columns;
- maps `FTR` directly to the approved 1X2 target;
- maps `FTR == H` to fallback value `1` and `FTR in {D, A}` to fallback value `0`;
- sorts rows chronologically by approved season order, match date, kickoff time, and original row
  order within each raw file;
- writes only the processed match-level columns listed below.

## Columns Produced

| Column | Meaning |
|--------|---------|
| `season` | Approved season label, e.g. `2020/21`. |
| `source_file` | Raw CSV file name used for traceability. |
| `division` | Football-Data.co.uk division code, expected as `D1`. |
| `match_date` | Parsed match date in ISO format. |
| `kickoff_time` | Kickoff time normalized to `HH:MM`. |
| `home_team` | Home team name. |
| `away_team` | Away team name. |
| `full_time_home_goals` | Full-time home-team goals from `FTHG`. |
| `full_time_away_goals` | Full-time away-team goals from `FTAG`. |
| `target_1x2` | Approved target from `FTR`: `H`, `D`, or `A`. |
| `target_home_win` | Fallback binary target: `1` for home win, `0` otherwise. |

No feature columns are produced in this milestone.

## Processed Row Count

| Scope | Row count |
|-------|-----------|
| Total processed rows | 1530 |
| 2020/21 | 306 |
| 2021/22 | 306 |
| 2022/23 | 306 |
| 2023/24 | 306 |
| 2024/25 | 306 |

The total row count equals the five approved Bundesliga seasons at 306 matches per season.

## Target Label Distribution

| Target | Meaning | Count |
|--------|---------|-------|
| `H` | Home win | 669 |
| `D` | Draw | 387 |
| `A` | Away win | 474 |

## Fallback Label Distribution

| Fallback label | Meaning | Count |
|----------------|---------|-------|
| `1` | Home win | 669 |
| `0` | Not home win | 861 |

The fallback label is deterministic from `target_1x2`: `1` if and only if `target_1x2 == H`;
otherwise `0`.

## Missingness Summary

| Column | Missing values |
|--------|----------------|
| `season` | 0 |
| `source_file` | 0 |
| `division` | 0 |
| `match_date` | 0 |
| `kickoff_time` | 0 |
| `home_team` | 0 |
| `away_team` | 0 |
| `full_time_home_goals` | 0 |
| `full_time_away_goals` | 0 |
| `target_1x2` | 0 |
| `target_home_win` | 0 |

No missing values were found in the processed columns.

## Validation Checks

Automated tests:

```text
python3 -m unittest tests/test_data_processing.py -v
```

Result:

```text
Ran 5 tests in 0.017s

OK
```

Additional validation checks:

| Check | Result |
|-------|--------|
| All five approved raw files read | Passed |
| Processed dataset exists locally | Passed |
| Processed dataset has 1530 rows | Passed |
| Each approved season contributes 306 rows | Passed |
| Required processed columns exist | Passed |
| `target_1x2` contains only `A`, `D`, `H` | Passed |
| `target_home_win` contains only `0`, `1` | Passed |
| Fallback label is deterministic from `target_1x2` | Passed |
| Rows are ordered chronologically by season/date/time | Passed |
| Raw file checksums unchanged after processing | Passed |
| Raw file modification timestamps unchanged after processing | Passed |
| Processed CSV is ignored by git | Passed |
| Raw CSVs are ignored by git | Passed |

## Raw File Immutability Evidence

The following SHA-256 hashes were observed before and after processing; they remained unchanged.

| Raw file | SHA-256 |
|----------|---------|
| `data/raw/football-data-co-uk_bundesliga_2020-2021.csv` | `48ec5d53d2452b6ebdbc07bd78a836d6a4686f99fc020439ee3292e685315e61` |
| `data/raw/football-data-co-uk_bundesliga_2021-2022.csv` | `034d0e1296e944dddf25e3c91b85ef5bd1ad25661b89d73878f5c73bfea4b9fc` |
| `data/raw/football-data-co-uk_bundesliga_2022-2023.csv` | `b716517b25033ce8e0243e967aa961876425a4c41e97c8aa8fa59f2aca061341` |
| `data/raw/football-data-co-uk_bundesliga_2023-2024.csv` | `1de8bc12a133dbbf71bc6ffda62082642f087f61b1b7c15ae9f2d320876fb07e` |
| `data/raw/football-data-co-uk_bundesliga_2024-2025.csv` | `a295c58033cfe6393cbbc28f7db85671839b960c5f1153fd3678e20ad2adb92e` |

Raw file modification timestamps also remained unchanged before and after processing.

## Version-Control Check

`git status --ignored --short data/raw data/processed` shows the raw and processed CSV files as
ignored:

```text
!! data/processed/bundesliga_2020_2025_matches_processed.csv
!! data/raw/football-data-co-uk_bundesliga_2020-2021.csv
!! data/raw/football-data-co-uk_bundesliga_2021-2022.csv
!! data/raw/football-data-co-uk_bundesliga_2022-2023.csv
!! data/raw/football-data-co-uk_bundesliga_2023-2024.csv
!! data/raw/football-data-co-uk_bundesliga_2024-2025.csv
```

No raw or processed CSV appears in normal `git status --short`.

## Milestone 2 Boundary Confirmation

- No feature engineering was performed.
- No rolling features were created.
- No models were trained.
- No model evaluation was performed.
- No notebooks were created.
- No visualizations were created.
- Existing specs were not modified.
- `README.md` was not modified.

