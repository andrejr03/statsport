# StatSport Dataset Inventory v1

**Milestone:** Milestone 1 - Dataset Acquisition  
**Inventory date:** 2026-06-20  
**Source:** Football-Data.co.uk  
**League:** Bundesliga, Germany top division (`D1`)  
**Storage location:** `data/raw/`

## Inventory

| Season | File name | Row count | Key columns present | Acquisition status |
|--------|-----------|-----------|---------------------|--------------------|
| 2020/21 | `football-data-co-uk_bundesliga_2020-2021.csv` | 306 | `Div`, `Date`, `Time`, `HomeTeam`, `AwayTeam`, `FTHG`, `FTAG`, `FTR`, `HS`, `AS`, `HST`, `AST` | Acquired |
| 2021/22 | `football-data-co-uk_bundesliga_2021-2022.csv` | 306 | `Div`, `Date`, `Time`, `HomeTeam`, `AwayTeam`, `FTHG`, `FTAG`, `FTR`, `HS`, `AS`, `HST`, `AST` | Acquired |
| 2022/23 | `football-data-co-uk_bundesliga_2022-2023.csv` | 306 | `Div`, `Date`, `Time`, `HomeTeam`, `AwayTeam`, `FTHG`, `FTAG`, `FTR`, `HS`, `AS`, `HST`, `AST` | Acquired |
| 2023/24 | `football-data-co-uk_bundesliga_2023-2024.csv` | 306 | `Div`, `Date`, `Time`, `HomeTeam`, `AwayTeam`, `FTHG`, `FTAG`, `FTR`, `HS`, `AS`, `HST`, `AST` | Acquired |
| 2024/25 | `football-data-co-uk_bundesliga_2024-2025.csv` | 306 | `Div`, `Date`, `Time`, `HomeTeam`, `AwayTeam`, `FTHG`, `FTAG`, `FTR`, `HS`, `AS`, `HST`, `AST` | Acquired |

## Inventory Notes

- Row counts count non-empty CSV data rows, excluding the header.
- `FTR` is present in every file and supports the approved Home / Draw / Away prediction target.
- `HST` and `AST` are present in every file and may support the approved optional shots-on-target
  feature group in a later milestone.
- This inventory does not define cleaning rules, feature rules, train/test splits, or model inputs.
- No processed data, feature dataset, notebook, script, model, or output artifact was created as part
  of this inventory.

## Local Files Expected

```text
data/raw/football-data-co-uk_bundesliga_2020-2021.csv
data/raw/football-data-co-uk_bundesliga_2021-2022.csv
data/raw/football-data-co-uk_bundesliga_2022-2023.csv
data/raw/football-data-co-uk_bundesliga_2023-2024.csv
data/raw/football-data-co-uk_bundesliga_2024-2025.csv
```

