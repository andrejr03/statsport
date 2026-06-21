# StatSport Baseline Model Evidence v1

**Milestone:** Milestone 4 - Baseline Model  
**Evidence date:** 2026-06-20  
**Input dataset:** `data/processed/bundesliga_2020_2025_features.csv`  
**Output directory:** `outputs/reports/`  
**Baseline:** Home-advantage baseline  
**Prediction target:** Home / Draw / Away (`H`, `D`, `A`)

## Purpose

This document records evidence that the mandatory home-advantage baseline was implemented and
evaluated before any Logistic Regression work begins.

This milestone does not train Logistic Regression, train Random Forest, create selected-model
predictions, create explainability artifacts, create notebooks, modify specs, or modify `README.md`.

## Implementation Files

| File | Purpose |
|------|---------|
| `src/statsport/baseline.py` | Reusable baseline logic, approved split definitions, walk-forward folds, probability derivation, metrics, and confusion matrix calculation. |
| `scripts/evaluate_baseline_model.py` | Command-line entry point that reads the feature dataset and writes baseline report CSVs. |
| `tests/test_baseline.py` | Focused tests for constant predictions, probability validity, training-only probabilities, class order, metric correctness, and split definitions. |

## Baseline Definition

The home-advantage baseline always predicts:

```text
H
```

This makes the baseline intentionally simple and transparent. It is an honest reference point for
future selected-model claims, not an attempt to maximize performance.

## Class Ordering

All class probabilities and confusion matrices use this stable order:

```text
H, D, A
```

The order is defined as `CLASS_ORDER = ("H", "D", "A")` in `src/statsport/baseline.py`.

## Probability Methodology

The baseline probability model uses empirical class frequencies from the relevant training rows only.
No validation or test rows are used to derive probabilities.

For the final test evaluation:

- Training rows: seasons `2020/21`, `2021/22`, `2022/23`, `2023/24`
- Evaluation rows: season `2024/25`

For each walk-forward fold, probabilities are derived from that fold's expanding training block only.
The probabilities are written in `H, D, A` order and validated to sum to `1`.

No smoothing is applied. The approved Bundesliga splits contain all three classes in every training
block used here.

## Train/Test Split

| Split | Seasons | Rows |
|-------|---------|------|
| Train | `2020/21`, `2021/22`, `2022/23`, `2023/24` | 1224 |
| Test | `2024/25` | 306 |

This is the approved chronological hold-out split and is defined in reusable code so future Logistic
Regression evaluation can share the same split definitions.

## Walk-Forward Folds

| Fold | Training seasons | Validation season | Validation rows |
|------|------------------|-------------------|-----------------|
| `walk_forward_1` | `2020/21` | `2021/22` | 306 |
| `walk_forward_2` | `2020/21`, `2021/22` | `2022/23` | 306 |
| `walk_forward_3` | `2020/21`, `2021/22`, `2022/23` | `2023/24` | 306 |

The held-out `2024/25` season is not used by any validation fold.

## Generated Outputs

| Output | Purpose |
|--------|---------|
| `outputs/reports/baseline_test_metrics.csv` | Baseline metrics and training-derived probabilities for the 2024/25 test season. |
| `outputs/reports/baseline_walk_forward_metrics.csv` | Baseline metrics and fold-specific probabilities for approved walk-forward validation folds. |
| `outputs/reports/baseline_test_confusion_matrix.csv` | Actual-by-predicted confusion matrix for the 2024/25 test season. |

These outputs are generated locally and remain ignored by git through the repository `.gitignore`
rules for `outputs/reports/*`.

## Baseline Test Metrics

| Split | Train seasons | Evaluation season | Rows | P(H) | P(D) | P(A) | Accuracy | Balanced Accuracy | Log Loss | Macro-F1 |
|-------|---------------|-------------------|------|------|------|------|----------|-------------------|----------|----------|
| `test` | `2020/21`; `2021/22`; `2022/23`; `2023/24` | `2024/25` | 306 | 0.450163398693 | 0.253267973856 | 0.296568627451 | 0.385620915033 | 0.333333333333 | 1.094260218009 | 0.185534591195 |

## Walk-Forward Metrics

| Fold | Train seasons | Validation season | Rows | P(H) | P(D) | P(A) | Accuracy | Balanced Accuracy | Log Loss | Macro-F1 |
|------|---------------|-------------------|------|------|------|------|----------|-------------------|----------|----------|
| `walk_forward_1` | `2020/21` | `2021/22` | 306 | 0.421568627451 | 0.264705882353 | 0.313725490196 | 0.467320261438 | 0.333333333333 | 1.061691966832 | 0.212323682257 |
| `walk_forward_2` | `2020/21`; `2021/22` | `2022/23` | 306 | 0.444444444444 | 0.251633986928 | 0.303921568627 | 0.473856209150 | 0.333333333333 | 1.057167057894 | 0.214338507021 |
| `walk_forward_3` | `2020/21`; `2021/22`; `2022/23` | `2023/24` | 306 | 0.454248366013 | 0.249455337691 | 0.296296296296 | 0.437908496732 | 0.333333333333 | 1.074834566954 | 0.203030303030 |

## Test Confusion Matrix

Rows are actual classes and columns are predicted classes.

| Actual | Predicted H | Predicted D | Predicted A |
|--------|-------------|-------------|-------------|
| H | 118 | 0 | 0 |
| D | 77 | 0 | 0 |
| A | 111 | 0 | 0 |

The draw and away classes are visible: this baseline never predicts either class, so their recall is
zero. That is expected for this intentionally simple reference model.

## Validation Results

Automated tests:

```text
python3 -m unittest tests/test_data_processing.py tests/test_feature_engineering.py tests/test_baseline.py -v
```

Result:

```text
Ran 18 tests

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
| Baseline predictions generated | Passed |
| Baseline prediction is always `H` | Passed |
| Baseline probabilities generated | Passed |
| Probabilities sum to `1` | Passed |
| Probabilities use stable `H, D, A` ordering | Passed |
| Probabilities derived only from training rows | Passed |
| Test metrics generated | Passed |
| Walk-forward metrics generated | Passed |
| Test confusion matrix generated | Passed |
| Chronological train/test split matches approved definition | Passed |
| Walk-forward folds match approved definition | Passed |
| Baseline and future Logistic Regression share reusable split definitions | Passed |
| Generated output files are ignored by git | Passed |
| Logistic Regression was not trained | Passed |
| Random Forest was not trained | Passed |

## Version-Control Check

`git check-ignore -v` confirms the generated baseline outputs are ignored:

```text
.gitignore:114:outputs/reports/* outputs/reports/baseline_test_metrics.csv
.gitignore:114:outputs/reports/* outputs/reports/baseline_walk_forward_metrics.csv
.gitignore:114:outputs/reports/* outputs/reports/baseline_test_confusion_matrix.csv
```

The regenerated local raw, processed, and feature CSVs are also ignored by `.gitignore`.

## Milestone 4 Boundary Confirmation

- Baseline predictions were created.
- Baseline probabilities were created.
- Baseline test metrics were created.
- Baseline walk-forward metrics were created.
- Baseline test confusion matrix was created.
- No Logistic Regression model was trained.
- No Random Forest model was trained.
- No selected-model predictions were created.
- No explainability artifacts were created.
- No notebooks were created.
- Existing specs were not modified.
- `README.md` was not modified.
- Milestone 5 was not started.
