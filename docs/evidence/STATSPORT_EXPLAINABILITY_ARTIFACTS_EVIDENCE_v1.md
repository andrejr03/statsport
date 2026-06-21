# StatSport Explainability Artifacts Evidence v1

**Milestone:** Milestone 7 - Explainability Artifacts  
**Evidence date:** 2026-06-21  
**Input dataset:** `data/processed/bundesliga_2020_2025_features.csv`  
**Input reports:** `outputs/reports/logistic_regression_coefficients.csv`, `outputs/reports/model_comparison_summary.md`  
**Output directory:** `outputs/reports/`  
**Selected model:** Multinomial Logistic Regression  
**Prediction target:** Home / Draw / Away (`H`, `D`, `A`)

## Purpose

This document records evidence that the approved explainability artifacts were generated from the
already-trained Logistic Regression coefficient report and the already-generated evaluation outputs.

This milestone does not retrain Logistic Regression, implement Random Forest, create Streamlit,
create a dashboard UI, create notebooks, modify specs, modify `README.md`, or start Milestone 8.

## Implementation Files

| File | Purpose |
|------|---------|
| `src/statsport/explainability.py` | Reusable coefficient-ranking, training-stat reconstruction, probability reconstruction, local contribution, deterministic example-selection, and markdown rendering logic. |
| `scripts/build_explainability_artifacts.py` | Command-line entry point that reads existing coefficients/evaluation outputs and writes explainability reports. |
| `tests/test_explainability.py` | Focused tests for coefficient ranking, stable ordering, deterministic example selection, local explanation generation, probability validity, and reproducible outputs. |

## Explainability Inputs Used

| Input | Purpose |
|-------|---------|
| `outputs/reports/logistic_regression_coefficients.csv` | Standardized class-specific Logistic Regression coefficients exported in Milestone 5. |
| `outputs/reports/model_comparison_summary.md` | Milestone 6 evaluation context for baseline comparison and draw-class limitation. |
| `data/processed/bundesliga_2020_2025_features.csv` | Match context, approved test-season rows, and training-only feature statistics needed to reconstruct standardized feature values. |

No model fitting is performed by the explainability script. Training-season feature means and scales
are recomputed only to recreate the selected model's training-only standardization for contribution
analysis.

## Class Ordering

All explainability artifacts use the project-wide stable class order:

```text
H, D, A
```

Reader-facing labels are Home, Draw, and Away.

## Global Explanation Outputs

| Output | Purpose |
|--------|---------|
| `outputs/reports/global_feature_influence.csv` | Full class-specific standardized coefficient ranking table. |
| `outputs/reports/global_feature_influence.md` | Reader-facing global feature influence explanation. |
| `outputs/reports/model_behaviour_summary.md` | Plain-language summary of what generally drives Home, Draw, and Away predictions. |

Top five standardized coefficient rankings by class:

| Class | Rank | Feature | Standardized coefficient |
|-------|-----:|---------|-------------------------:|
| Home | 1 | `goals_scored_diff` | 0.108201929510 |
| Home | 2 | `home_goals_scored_avg` | 0.097575493893 |
| Home | 3 | `goal_difference_diff` | 0.091528201587 |
| Home | 4 | `home_goal_difference_avg` | 0.079045975025 |
| Home | 5 | `home_recent_form_points_avg` | -0.070275799031 |
| Draw | 1 | `home_recent_form_points_avg` | 0.204890671918 |
| Draw | 2 | `home_goals_scored_avg` | -0.114762902972 |
| Draw | 3 | `recent_form_points_diff` | 0.097349553711 |
| Draw | 4 | `home_goal_difference_avg` | -0.096727945815 |
| Draw | 5 | `away_goals_scored_avg` | -0.092832425150 |
| Away | 1 | `away_goals_scored_avg` | 0.146336245615 |
| Away | 2 | `home_recent_form_points_avg` | -0.134614872887 |
| Away | 3 | `away_goal_difference_avg` | 0.098349300062 |
| Away | 4 | `goals_scored_diff` | -0.094217222427 |
| Away | 5 | `recent_form_points_diff` | -0.059702549783 |

The rankings are class-specific and sorted by absolute coefficient size, with deterministic feature
name tie-breaking.

## Local Explanation Outputs

| Output | Purpose |
|--------|---------|
| `outputs/reports/prediction_explanation_card_1.md` | Strong/correct 2024/25 prediction explanation. |
| `outputs/reports/prediction_explanation_card_2.md` | Difficult draw or draw-adjacent 2024/25 prediction explanation. |
| `outputs/reports/prediction_explanation_card_3.md` | Incorrect or low-confidence 2024/25 prediction explanation. |

Each card includes match context, predicted probabilities, actual outcome, key coefficient
contributions, feature-difference context, and confidence discussion.

## Example-Selection Methodology

Examples are selected deterministically from the approved 2024/25 test season:

1. Strong/correct prediction: highest-confidence row where predicted class equals actual class.
2. Difficult draw or draw-adjacent prediction: prefer actual draws, then highest predicted draw
   probability, then smallest confidence margin, then chronological match key.
3. Incorrect or low-confidence prediction: incorrect row with the lowest confidence, then smallest
   confidence margin, then chronological match key.

Already selected matches are excluded from later categories so exactly three unique examples are
produced.

## Selected Matches

| Card | Category | Match | Date | Actual | Predicted | Confidence |
|------|----------|-------|------|--------|-----------|-----------:|
| 1 | Strong/correct prediction | Bayern Munich vs Heidenheim | 2024-12-07 | H | H | 0.752024588212 |
| 2 | Difficult draw or draw-adjacent prediction | Heidenheim vs Bochum | 2025-05-02 | D | H | 0.435016365882 |
| 3 | Incorrect or low-confidence prediction | RB Leipzig vs Werder Bremen | 2025-01-12 | H | A | 0.346386307771 |

## Limitations Generated

`outputs/reports/limitations_and_uncertainty.md` documents:

- draw-class weakness;
- non-causality warning;
- Bundesliga-only scope;
- small-data limitations;
- baseline comparison context.

## Validation Results

Automated tests:

```text
python3 -m unittest tests/test_data_processing.py tests/test_feature_engineering.py tests/test_baseline.py tests/test_selected_model.py tests/test_evaluation.py tests/test_explainability.py -v
```

Result:

```text
Ran 39 tests

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
| Global feature influence generated | Passed |
| Model behaviour summary generated | Passed |
| Exactly three explanation cards generated | Passed |
| Limitations note generated | Passed |
| Deterministic example selection | Passed |
| Local probabilities sum to 1 in `H`, `D`, `A` order | Passed |
| Consecutive explainability script runs produced identical output hashes | Passed |
| No Logistic Regression retraining occurred in this milestone | Passed |
| Random Forest was not implemented | Passed |
| No Streamlit, dashboard UI, or notebook was created | Passed |
| Generated output files are ignored by git | Passed |

## Version-Control Check

`git check-ignore -v` confirms the generated explainability outputs are ignored:

```text
.gitignore:114:outputs/reports/* outputs/reports/global_feature_influence.csv
.gitignore:114:outputs/reports/* outputs/reports/global_feature_influence.md
.gitignore:114:outputs/reports/* outputs/reports/prediction_explanation_card_1.md
.gitignore:114:outputs/reports/* outputs/reports/prediction_explanation_card_2.md
.gitignore:114:outputs/reports/* outputs/reports/prediction_explanation_card_3.md
.gitignore:114:outputs/reports/* outputs/reports/model_behaviour_summary.md
.gitignore:114:outputs/reports/* outputs/reports/limitations_and_uncertainty.md
```

## Milestone 7 Boundary Confirmation

- Explainability artifacts were generated from existing Logistic Regression coefficients and
  evaluation outputs.
- No new model training occurred.
- Random Forest was not implemented.
- No Streamlit, dashboard UI, or notebook was created.
- Existing specs were not modified.
- `README.md` was not modified.
- Milestone 8 was not started.
