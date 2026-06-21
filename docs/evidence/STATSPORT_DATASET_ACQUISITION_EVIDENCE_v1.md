# StatSport Dataset Acquisition Evidence v1

**Milestone:** Milestone 1 - Dataset Acquisition  
**Acquisition date:** 2026-06-20  
**Approved source:** Football-Data.co.uk  
**Approved league:** Bundesliga, Germany top division (`D1`)  
**Approved seasons:** 2020/21, 2021/22, 2022/23, 2023/24, 2024/25  
**Local storage:** `data/raw/`

## Purpose

This document records the evidence for acquiring the approved StatSport raw dataset. It is limited to
dataset acquisition only. No processed data, feature engineering, modelling, evaluation, or
explainability work was performed for this milestone.

## Source URLs

| Season | Source URL | Local file |
|--------|------------|------------|
| 2020/21 | `https://www.football-data.co.uk/mmz4281/2021/D1.csv` | `data/raw/football-data-co-uk_bundesliga_2020-2021.csv` |
| 2021/22 | `https://www.football-data.co.uk/mmz4281/2122/D1.csv` | `data/raw/football-data-co-uk_bundesliga_2021-2022.csv` |
| 2022/23 | `https://www.football-data.co.uk/mmz4281/2223/D1.csv` | `data/raw/football-data-co-uk_bundesliga_2022-2023.csv` |
| 2023/24 | `https://www.football-data.co.uk/mmz4281/2324/D1.csv` | `data/raw/football-data-co-uk_bundesliga_2023-2024.csv` |
| 2024/25 | `https://www.football-data.co.uk/mmz4281/2425/D1.csv` | `data/raw/football-data-co-uk_bundesliga_2024-2025.csv` |

## Acquisition Procedure

The raw files were downloaded directly from Football-Data.co.uk using the public CSV URLs above and
stored under `data/raw/`.

Re-acquisition commands:

```bash
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2020-2021.csv https://www.football-data.co.uk/mmz4281/2021/D1.csv
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2021-2022.csv https://www.football-data.co.uk/mmz4281/2122/D1.csv
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2022-2023.csv https://www.football-data.co.uk/mmz4281/2223/D1.csv
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2023-2024.csv https://www.football-data.co.uk/mmz4281/2324/D1.csv
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2024-2025.csv https://www.football-data.co.uk/mmz4281/2425/D1.csv
```

These commands are intentionally simple and require no scraping framework, paid account, cloud
service, GPU, or external database.

## Acquisition Results

| Season | Local file | Row count | Result column present | Status |
|--------|------------|-----------|-----------------------|--------|
| 2020/21 | `football-data-co-uk_bundesliga_2020-2021.csv` | 306 | `FTR` present | Acquired |
| 2021/22 | `football-data-co-uk_bundesliga_2021-2022.csv` | 306 | `FTR` present | Acquired |
| 2022/23 | `football-data-co-uk_bundesliga_2022-2023.csv` | 306 | `FTR` present | Acquired |
| 2023/24 | `football-data-co-uk_bundesliga_2023-2024.csv` | 306 | `FTR` present | Acquired |
| 2024/25 | `football-data-co-uk_bundesliga_2024-2025.csv` | 306 | `FTR` present | Acquired |

Each Bundesliga season has 18 teams and 306 league matches, so these row counts are plausible for the
approved scope.

## Provenance Notes

- Football-Data.co.uk publishes historical results and match-statistics data as per-season CSV files.
- `D1` is the Football-Data.co.uk division code used here for the German Bundesliga.
- The full-time result column is `FTR`, with values `H`, `D`, and `A` for home win, draw, and away
  win. This directly supports the approved 1X2 prediction target.
- The files also include match context columns such as `Div`, `Date`, `Time`, `HomeTeam`, `AwayTeam`,
  `FTHG`, and `FTAG`, plus match-statistics columns including `HS`, `AS`, `HST`, and `AST`.
- Raw files are treated as immutable local source data and are not committed to git.
- No processed dataset was created during this milestone.

## Licensing and Usage Notes

Football-Data.co.uk provides the historical CSV files publicly on its website. Its notes page
describes the CSV field meanings, including `FTR` for full-time result. The site also has a
disclaimer and help page explaining that the service is free to users and funded by advertising.

No explicit open-source data license was identified during this acquisition milestone. To stay aligned
with the repository data rules, the raw CSVs are stored locally under `data/raw/` and are not
redistributed through git. The repository records the acquisition process and provenance so another
reviewer can re-fetch the same public files directly from Football-Data.co.uk.

Reference pages checked:

- `https://www.football-data.co.uk/`
- `https://www.football-data.co.uk/notes.txt`
- `https://www.football-data.co.uk/disclaimer.php`
- `https://www.football-data.co.uk/help_footballdata.php`

## Milestone 1 Validation Summary

- All five approved seasons were acquired.
- Files were stored under `data/raw/`.
- Row counts are plausible: 306 rows per season.
- The full-time result column `FTR` exists in every file.
- Raw dataset files remain ignored by git and were not staged.
- No processed data was created.
- No feature engineering was performed.
- No modelling was performed.

