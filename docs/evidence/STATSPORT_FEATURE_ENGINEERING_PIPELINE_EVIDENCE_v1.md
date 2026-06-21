# StatSport Feature Engineering Pipeline Evidence v1

**Milestone:** Milestone 3 - Feature Engineering Pipeline  
**Evidence date:** 2026-06-20  
**Input dataset:** `data/processed/bundesliga_2020_2025_matches_processed.csv`  
**Output dataset:** `data/processed/bundesliga_2020_2025_features.csv`  
**Feature scope:** Approved core features only  
**Rolling window:** 5 prior team matches

## Purpose

This document records evidence that the Milestone 3 feature engineering pipeline creates
leakage-safe, match-level core features for the approved StatSport Bundesliga dataset.

This milestone does not train models, evaluate models, create baseline predictions, create logistic
regression or random forest models, create explainability artifacts, implement optional features,
create notebooks, modify specs, or modify `README.md`.

## Implementation Files

| File | Purpose |
|------|---------|
| `src/statsport/feature_engineering.py` | Reusable feature generation logic, rolling calculations, leakage controls, summary helpers, and optional-feature checks. |
| `scripts/build_bundesliga_features.py` | Command-line entry point that reads the Milestone 2 processed dataset and writes the core feature dataset. |
| `tests/test_feature_engineering.py` | Focused standard-library tests for rolling calculations, no future leakage, row preservation, feature presence, determinism, and chronological correctness. |

## Feature Definitions

All rolling features are computed from each team's prior matches only. For a fixture between a home
team and an away team, the pipeline reads both teams' histories before updating either history with
the current fixture result.

When a team has no prior matches in the available dataset, its rolling averages are set to `0.000000`.
This keeps the feature dataset complete and deterministic while making early-season lack of history
explicit through the documented definition.

| Feature column | Definition |
|----------------|------------|
| `home_advantage` | Deterministic fixture indicator. Because each row is represented from the home team's perspective, this is always `1`. |
| `home_recent_form_points_avg` | Home team's average league points over its last 5 prior matches. |
| `away_recent_form_points_avg` | Away team's average league points over its last 5 prior matches. |
| `recent_form_points_diff` | `home_recent_form_points_avg - away_recent_form_points_avg`. |
| `home_goals_scored_avg` | Home team's average goals scored over its last 5 prior matches. |
| `away_goals_scored_avg` | Away team's average goals scored over its last 5 prior matches. |
| `goals_scored_diff` | `home_goals_scored_avg - away_goals_scored_avg`. |
| `home_goals_conceded_avg` | Home team's average goals conceded over its last 5 prior matches. |
| `away_goals_conceded_avg` | Away team's average goals conceded over its last 5 prior matches. |
| `goals_conceded_diff` | `home_goals_conceded_avg - away_goals_conceded_avg`. |
| `home_goal_difference_avg` | Home team's average goal difference over its last 5 prior matches. |
| `away_goal_difference_avg` | Away team's average goal difference over its last 5 prior matches. |
| `goal_difference_diff` | `home_goal_difference_avg - away_goal_difference_avg`. |

## Rolling Window Definition

The rolling window is fixed at 5 prior matches per team.

- "Prior" means matches already processed earlier in chronological order.
- The current fixture is not included in its own features.
- Histories carry across the approved dataset chronology, including season boundaries, because those
  matches are still historical information available before later fixtures.
- If a team has fewer than 5 prior matches, the average uses all available prior matches.
- If a team has zero prior matches, the average is `0.000000`.

This definition is implemented by `ROLLING_WINDOW_MATCHES = 5` in
`src/statsport/feature_engineering.py`.

## Leakage Controls

The pipeline prevents future and target leakage through these controls:

- The input processed rows are sorted by season, match date, kickoff time, and source order.
- Feature values for both teams are calculated before the current match is appended to either team's
  history.
- Rolling values use goals, goal difference, and points from prior fixtures only.
- The full-time goals and target label for the current fixture are retained as labels/context, but
  they are not used to compute the current fixture's feature values.
- Optional feature groups are not implemented.
- No modelling, training, evaluation, or prediction generation occurs in this milestone.

## Output Dataset

```text
data/processed/bundesliga_2020_2025_features.csv
```

The output dataset exists locally and is ignored by git through the repository `.gitignore` rules for
`data/processed/*`.

## Row Counts and Season Coverage

| Scope | Row count |
|-------|-----------|
| Total feature rows | 1530 |
| 2020/21 | 306 |
| 2021/22 | 306 |
| 2022/23 | 306 |
| 2023/24 | 306 |
| 2024/25 | 306 |

All five approved seasons are covered, and the feature row count matches the Milestone 2 processed
dataset row count.

## Feature Columns Produced

```text
home_advantage
home_recent_form_points_avg
away_recent_form_points_avg
recent_form_points_diff
home_goals_scored_avg
away_goals_scored_avg
goals_scored_diff
home_goals_conceded_avg
away_goals_conceded_avg
goals_conceded_diff
home_goal_difference_avg
away_goal_difference_avg
goal_difference_diff
```

## Optional Features Not Implemented

The following approved optional feature groups were deliberately not implemented in this milestone:

- Shots on target.
- League position.
- Elo-style rating.

Validation found no output columns containing optional-feature markers: `shots_on_target`,
`league_position`, or `elo`.

## Feature Missingness Summary

| Feature column | Missing values |
|----------------|----------------|
| `home_advantage` | 0 |
| `home_recent_form_points_avg` | 0 |
| `away_recent_form_points_avg` | 0 |
| `recent_form_points_diff` | 0 |
| `home_goals_scored_avg` | 0 |
| `away_goals_scored_avg` | 0 |
| `goals_scored_diff` | 0 |
| `home_goals_conceded_avg` | 0 |
| `away_goals_conceded_avg` | 0 |
| `goals_conceded_diff` | 0 |
| `home_goal_difference_avg` | 0 |
| `away_goal_difference_avg` | 0 |
| `goal_difference_diff` | 0 |

No missing values were found in the generated core feature columns.

## Target Distribution Retained for Later Modelling

| Target | Count |
|--------|-------|
| `H` | 669 |
| `D` | 387 |
| `A` | 474 |

The target columns are retained for later supervised modelling milestones, but target labels are not
used to compute the current fixture's features.

## Validation Results

Automated tests:

```text
python3 -m unittest tests/test_data_processing.py tests/test_feature_engineering.py -v
```

Result:

```text
Ran 11 tests in 0.007s

OK
```

Compile check:

```text
python3 -m compileall src scripts tests
```

Result: passed.

Additional validation checks:

| Check | Result |
|-------|--------|
| Output dataset exists | Passed |
| Output dataset has 1530 rows | Passed |
| All five approved seasons covered | Passed |
| Each season contributes 306 rows | Passed |
| Core feature columns exist | Passed |
| Optional feature columns absent | Passed |
| Feature generation deterministic | Passed |
| Rows are chronologically ordered | Passed |
| `target_1x2` contains only `A`, `D`, `H` | Passed |
| `target_home_win` contains only `0`, `1` | Passed |
| Fallback label remains deterministic from `target_1x2` | Passed |
| Raw file checksums unchanged | Passed |
| Milestone 2 processed file checksum unchanged | Passed |
| Feature dataset ignored by git | Passed |

## Immutability Evidence

Raw files remained unchanged. The Milestone 2 processed input file also remained unchanged.

| File | SHA-256 after Milestone 3 |
|------|---------------------------|
| `data/raw/football-data-co-uk_bundesliga_2020-2021.csv` | `48ec5d53d2452b6ebdbc07bd78a836d6a4686f99fc020439ee3292e685315e61` |
| `data/raw/football-data-co-uk_bundesliga_2021-2022.csv` | `034d0e1296e944dddf25e3c91b85ef5bd1ad25661b89d73878f5c73bfea4b9fc` |
| `data/raw/football-data-co-uk_bundesliga_2022-2023.csv` | `b716517b25033ce8e0243e967aa961876425a4c41e97c8aa8fa59f2aca061341` |
| `data/raw/football-data-co-uk_bundesliga_2023-2024.csv` | `1de8bc12a133dbbf71bc6ffda62082642f087f61b1b7c15ae9f2d320876fb07e` |
| `data/raw/football-data-co-uk_bundesliga_2024-2025.csv` | `a295c58033cfe6393cbbc28f7db85671839b960c5f1153fd3678e20ad2adb92e` |
| `data/processed/bundesliga_2020_2025_matches_processed.csv` | `7a470fb448e2105b5f2b87006ed7b7ab7160ca25b8449814df41f8c0022935cb` |

Generated feature dataset hash:

```text
7aa57a6f477dd6e12db0aa1b609a1db4b1b331c919c45cbca3c0c047b77bdc8e  data/processed/bundesliga_2020_2025_features.csv
```

## Version-Control Check

`git status --ignored --short data/raw data/processed` shows raw, processed, and feature CSV files as
ignored:

```text
!! data/processed/bundesliga_2020_2025_features.csv
!! data/processed/bundesliga_2020_2025_matches_processed.csv
!! data/raw/football-data-co-uk_bundesliga_2020-2021.csv
!! data/raw/football-data-co-uk_bundesliga_2021-2022.csv
!! data/raw/football-data-co-uk_bundesliga_2022-2023.csv
!! data/raw/football-data-co-uk_bundesliga_2023-2024.csv
!! data/raw/football-data-co-uk_bundesliga_2024-2025.csv
```

No raw or processed CSV appears in normal `git status --short`.

## Milestone 3 Boundary Confirmation

- No optional features were implemented.
- No baseline predictions were created.
- No logistic regression model was created.
- No random forest model was created.
- No model training was performed.
- No model evaluation was performed.
- No explainability artifacts were created.
- No notebooks were created.
- Existing specs were not modified.
- `README.md` was not modified.

