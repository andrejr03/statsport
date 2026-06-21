# StatSport Selected Model Evidence v1

**Milestone:** Milestone 5 - Selected Model  
**Evidence date:** 2026-06-20  
**Input dataset:** `data/processed/bundesliga_2020_2025_features.csv`  
**Output directory:** `outputs/reports/`  
**Selected model:** Multinomial Logistic Regression  
**Prediction target:** Home / Draw / Away (`H`, `D`, `A`)

## Purpose

This document records evidence that the approved selected model, multinomial Logistic Regression, was
trained and evaluated using the same split and fold definitions as the Milestone 4 baseline.

This milestone does not implement Random Forest, create explainability artifacts, create a final
evaluation report, create notebooks, create dashboards, modify specs, modify `README.md`, or start
Milestone 6.

## Implementation Files

| File | Purpose |
|------|---------|
| `src/statsport/selected_model.py` | Reusable selected-model logic, approved feature selection, training-only preprocessing, Logistic Regression fitting, predictions, probabilities, metrics, and coefficient export. |
| `scripts/evaluate_logistic_regression_model.py` | Command-line entry point that reads the feature dataset and writes selected-model report CSVs. |
| `tests/test_selected_model.py` | Focused tests for feature selection, preprocessing leakage controls, probability validity, split/fold reuse, coefficient availability, and determinism. |

## Selected Model Definition

The selected model is multinomial Logistic Regression over the approved core feature columns. It uses:

- scikit-learn `LogisticRegression`
- `solver="lbfgs"`
- `max_iter=1000`
- `random_state=42`
- training-only `StandardScaler` preprocessing

No model artifact is committed. The model and outputs are regenerable from the feature dataset and
script.

## Feature Columns Used

Only the approved core Milestone 3 features are used:

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

No optional feature groups are used.

## Preprocessing Method

Numeric feature columns are standardized with `StandardScaler`.

For each split or fold:

- the scaler is fit on that split's training rows only;
- validation and test rows are transformed with the already-fitted scaler;
- target labels, validation rows, and test rows do not influence preprocessing.

This keeps preprocessing aligned with the leakage-avoidance requirements in `EVALUATION_SPEC.md`.

## Class Ordering

StatSport report outputs use this stable class order:

```text
H, D, A
```

scikit-learn may store classes internally in its own sorted order, but the selected-model module maps
all probabilities, confusion matrices, and coefficient output into the project order above.

## Train/Test Split

| Split | Seasons | Rows |
|-------|---------|------|
| Train | `2020/21`, `2021/22`, `2022/23`, `2023/24` | 1224 |
| Test | `2024/25` | 306 |

The selected model reuses the split definitions from `src/statsport/baseline.py`.

## Walk-Forward Folds

| Fold | Training seasons | Validation season | Validation rows |
|------|------------------|-------------------|-----------------|
| `walk_forward_1` | `2020/21` | `2021/22` | 306 |
| `walk_forward_2` | `2020/21`, `2021/22` | `2022/23` | 306 |
| `walk_forward_3` | `2020/21`, `2021/22`, `2022/23` | `2023/24` | 306 |

The selected model reuses the fold definitions from `src/statsport/baseline.py`.

## Generated Outputs

| Output | Purpose |
|--------|---------|
| `outputs/reports/logistic_regression_test_metrics.csv` | Selected-model metrics and mean predicted probabilities for the 2024/25 test season. |
| `outputs/reports/logistic_regression_walk_forward_metrics.csv` | Selected-model metrics and mean predicted probabilities for approved walk-forward validation folds. |
| `outputs/reports/logistic_regression_test_confusion_matrix.csv` | Actual-by-predicted confusion matrix for the 2024/25 test season. |
| `outputs/reports/logistic_regression_coefficients.csv` | Standardized coefficients and intercepts from the final train 2020/21-2023/24 model. |

These outputs are generated locally and remain ignored by git through the repository `.gitignore`
rules for `outputs/reports/*`.

## Test Metrics

| Split | Train seasons | Evaluation season | Rows | Mean P(H) | Mean P(D) | Mean P(A) | Accuracy | Balanced Accuracy | Log Loss | Macro-F1 |
|-------|---------------|-------------------|------|-----------|-----------|-----------|----------|-------------------|----------|----------|
| `test` | `2020/21`; `2021/22`; `2022/23`; `2023/24` | `2024/25` | 306 | 0.457444998445 | 0.253348446447 | 0.289206555108 | 0.450980392157 | 0.395709268591 | 1.063246819064 | 0.320700358138 |

## Walk-Forward Metrics

| Fold | Train seasons | Validation season | Rows | Mean P(H) | Mean P(D) | Mean P(A) | Accuracy | Balanced Accuracy | Log Loss | Macro-F1 |
|------|---------------|-------------------|------|-----------|-----------|-----------|----------|-------------------|----------|----------|
| `walk_forward_1` | `2020/21` | `2021/22` | 306 | 0.421420849240 | 0.268194145545 | 0.310385005215 | 0.486928104575 | 0.407560323999 | 1.053428431775 | 0.371397601841 |
| `walk_forward_2` | `2020/21`; `2021/22` | `2022/23` | 306 | 0.442559294338 | 0.250588616279 | 0.306852089383 | 0.490196078431 | 0.393278089637 | 1.039784627651 | 0.348915088078 |
| `walk_forward_3` | `2020/21`; `2021/22`; `2022/23` | `2023/24` | 306 | 0.453581861432 | 0.244577792174 | 0.301840346393 | 0.532679738562 | 0.454117959922 | 0.998818052473 | 0.396066930121 |

## Test Confusion Matrix

Rows are actual classes and columns are predicted classes.

| Actual | Predicted H | Predicted D | Predicted A |
|--------|-------------|-------------|-------------|
| H | 105 | 0 | 13 |
| D | 59 | 0 | 18 |
| A | 77 | 1 | 33 |

The model predicts all three classes at least once on the test season, but draw prediction remains
very weak. This should remain visible in later evaluation and explanation work.

## Coefficient Output

The coefficient file contains 42 rows:

- 3 classes: `H`, `D`, `A`
- 13 standardized feature coefficients per class
- 1 intercept per class

Example rows from `outputs/reports/logistic_regression_coefficients.csv`:

| Class | Feature | Coefficient |
|-------|---------|-------------|
| H | `goals_scored_diff` | 0.108201929510 |
| H | `goal_difference_diff` | 0.091528201587 |
| D | `home_recent_form_points_avg` | 0.204890671918 |
| A | `away_goals_scored_avg` | 0.146336245615 |

These coefficients are suitable inputs for the later Milestone 7 explainability work, but this
milestone does not interpret them as explanation artifacts.

## Baseline Comparison Summary

Compared on the same 2024/25 test season:

| Metric | Baseline | Logistic Regression | Directional change |
|--------|----------|---------------------|--------------------|
| Accuracy | 0.385620915033 | 0.450980392157 | +0.065359477124 |
| Balanced Accuracy | 0.333333333333 | 0.395709268591 | +0.062375935258 |
| Log Loss | 1.094260218009 | 1.063246819064 | -0.031013398945 |
| Macro-F1 | 0.185534591195 | 0.320700358138 | +0.135165766943 |

This is an initial selected-model comparison, not a final Milestone 6 evaluation report. The results
show improvement over the baseline on the approved test metrics while still exposing weak draw-class
performance.

## Validation Results

Automated tests:

```text
python3 -m unittest tests/test_data_processing.py tests/test_feature_engineering.py tests/test_baseline.py tests/test_selected_model.py -v
```

Result:

```text
Ran 25 tests

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
| Logistic Regression model trained | Passed |
| Probabilities generated for `H`, `D`, `A` | Passed |
| Probability rows sum to `1` | Passed |
| Test metrics generated | Passed |
| Walk-forward metrics generated | Passed |
| Test confusion matrix generated | Passed |
| Coefficient output generated | Passed |
| Preprocessing fitted only on training rows | Passed |
| Selected model uses baseline split definitions | Passed |
| Selected model uses baseline walk-forward fold definitions | Passed |
| Generated output files are ignored by git | Passed |
| Repeated script run produced identical report hashes | Passed |
| Random Forest was not implemented | Passed |
| No explainability artifacts were created | Passed |

## Version-Control Check

`git check-ignore -v` confirms the generated selected-model outputs are ignored:

```text
.gitignore:114:outputs/reports/* outputs/reports/logistic_regression_test_metrics.csv
.gitignore:114:outputs/reports/* outputs/reports/logistic_regression_walk_forward_metrics.csv
.gitignore:114:outputs/reports/* outputs/reports/logistic_regression_test_confusion_matrix.csv
.gitignore:114:outputs/reports/* outputs/reports/logistic_regression_coefficients.csv
```

The local feature CSV remains ignored by `.gitignore`.

## Milestone 5 Boundary Confirmation

- Logistic Regression was trained and evaluated.
- Coefficients were exported for later explainability.
- Random Forest was not implemented because Logistic Regression was viable.
- No explainability artifacts were created.
- No final evaluation report was created.
- No notebooks were created.
- No Streamlit, UI, or dashboard was created.
- Existing specs were not modified.
- `README.md` was not modified.
- Milestone 6 was not started.
