# StatSport Evaluation Pipeline Evidence v1

**Milestone:** Milestone 6 - Evaluation Pipeline  
**Evidence date:** 2026-06-20  
**Input reports:** `outputs/reports/` baseline and Logistic Regression reports  
**Output directory:** `outputs/reports/`  
**Models compared:** Home-advantage baseline vs. multinomial Logistic Regression  
**Prediction target:** Home / Draw / Away (`H`, `D`, `A`)

## Purpose

This document records evidence that the final baseline-versus-selected-model evaluation pipeline was
implemented using the approved chronological test split, season-blocked walk-forward validation, and
approved core metrics.

This milestone consolidates existing Milestone 4 and Milestone 5 outputs. It does not retrain models,
modify model implementations, implement Random Forest, create explainability artifacts, create
notebooks, create dashboards, modify specs, modify `README.md`, or start Milestone 7.

## Implementation Files

| File | Purpose |
|------|---------|
| `src/statsport/evaluation.py` | Reusable report loading, split/fold validation, metric delta calculation, confusion-matrix draw summary, and summary markdown generation. |
| `scripts/build_model_comparison_reports.py` | Command-line entry point that reads existing baseline and Logistic Regression reports and writes consolidated comparison outputs. |
| `tests/test_evaluation.py` | Focused tests for metric deltas, Log Loss direction, split/fold validation, missing files, summary structure, and deterministic output generation. |

## Input Report Files

| Input | Purpose |
|-------|---------|
| `outputs/reports/baseline_test_metrics.csv` | Baseline 2024/25 test metrics. |
| `outputs/reports/baseline_walk_forward_metrics.csv` | Baseline walk-forward validation metrics. |
| `outputs/reports/baseline_test_confusion_matrix.csv` | Baseline 2024/25 confusion matrix. |
| `outputs/reports/logistic_regression_test_metrics.csv` | Logistic Regression 2024/25 test metrics. |
| `outputs/reports/logistic_regression_walk_forward_metrics.csv` | Logistic Regression walk-forward validation metrics. |
| `outputs/reports/logistic_regression_test_confusion_matrix.csv` | Logistic Regression 2024/25 confusion matrix. |
| `outputs/reports/logistic_regression_coefficients.csv` | Logistic Regression coefficient output from Milestone 5; retained as an input artifact but not interpreted here. |

## Generated Outputs

| Output | Purpose |
|--------|---------|
| `outputs/reports/model_comparison_test_metrics.csv` | Consolidated baseline-vs-Logistic-Regression test comparison with metric deltas. |
| `outputs/reports/model_comparison_walk_forward_metrics.csv` | Consolidated walk-forward comparison with metric deltas by fold. |
| `outputs/reports/model_comparison_summary.md` | Concise portfolio/report-ready evaluation summary. |

These outputs are generated locally and remain ignored by git through the repository `.gitignore`
rules for `outputs/reports/*`.

## Metric Delta Methodology

Metric deltas are calculated as:

```text
Logistic Regression metric - baseline metric
```

For Accuracy, Balanced Accuracy, and Macro-F1, higher values are better, so positive deltas indicate
improvement.

For Log Loss, lower values are better, so negative deltas indicate improvement.

## Test Comparison Metrics

| Split | Rows | Baseline Accuracy | Logistic Accuracy | Accuracy Delta | Baseline Balanced Accuracy | Logistic Balanced Accuracy | Balanced Accuracy Delta | Baseline Log Loss | Logistic Log Loss | Log Loss Delta | Baseline Macro-F1 | Logistic Macro-F1 | Macro-F1 Delta |
|-------|------|-------------------|-------------------|----------------|----------------------------|----------------------------|-------------------------|-------------------|-------------------|----------------|-------------------|-------------------|----------------|
| `test` | 306 | 0.385620915033 | 0.450980392157 | +0.065359477124 | 0.333333333333 | 0.395709268591 | +0.062375935258 | 1.094260218009 | 1.063246819064 | -0.031013398945 | 0.185534591195 | 0.320700358138 | +0.135165766943 |

The 2024/25 test comparison shows Logistic Regression improving over the baseline on all approved
core metrics. This is a modest but consistent improvement and should be reported proportionately.

## Walk-Forward Comparison Metrics

| Fold | Validation season | Rows | Accuracy Delta | Balanced Accuracy Delta | Log Loss Delta | Macro-F1 Delta |
|------|-------------------|------|----------------|-------------------------|----------------|----------------|
| `walk_forward_1` | `2021/22` | 306 | +0.019607843137 | +0.074226990666 | -0.008263535057 | +0.159073919584 |
| `walk_forward_2` | `2022/23` | 306 | +0.016339869281 | +0.059944756304 | -0.017382430243 | +0.134576581057 |
| `walk_forward_3` | `2023/24` | 306 | +0.094771241830 | +0.120784626589 | -0.076016514481 | +0.193036627091 |

The walk-forward comparison also favors Logistic Regression on all approved core metrics in all three
folds. This supports the selected-model choice while remaining within the approved evaluation scope.

## Interpretation of Improvement

Logistic Regression beats the home-advantage baseline on:

- Accuracy.
- Balanced Accuracy.
- Log Loss, where lower is better.
- Macro-F1.

The improvement is useful but not grounds for overclaiming. Football match outcomes remain noisy,
and the evaluation still shows class-level weakness, especially for draws.

## Draw-Class Limitation

The 2024/25 confusion matrices show the draw-class limitation clearly:

| Model | Actual draws | Correct draw predictions | Total draw predictions |
|-------|--------------|--------------------------|------------------------|
| Baseline | 77 | 0 | 0 |
| Logistic Regression | 77 | 0 | 1 |

The selected model improves aggregate metrics, but it still fails to correctly predict any actual
draws in the held-out test season. This limitation must remain visible in later portfolio narrative
and explainability work.

## Approved Core Metrics Included

All approved core metrics are included:

- Accuracy.
- Balanced Accuracy.
- Log Loss.
- Macro-F1.
- Confusion Matrix.

Optional Brier Score and calibration assessment were not implemented in this milestone. They were not
required to complete the approved core evaluation, and adding them now would expand scope beyond the
necessary final baseline-versus-selected-model comparison.

## Validation Results

Automated tests:

```text
python3 -m unittest tests/test_data_processing.py tests/test_feature_engineering.py tests/test_baseline.py tests/test_selected_model.py tests/test_evaluation.py -v
```

Result:

```text
Ran 33 tests

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
| Consolidated test comparison exists | Passed |
| Consolidated walk-forward comparison exists | Passed |
| Summary markdown exists | Passed |
| All approved core metrics included | Passed |
| Baseline and Logistic Regression test rows match | Passed |
| Baseline and Logistic Regression walk-forward folds match | Passed |
| Metric deltas calculated correctly | Passed |
| Lower Log Loss handled as improvement | Passed |
| Draw-class limitation noted honestly | Passed |
| Optional Brier/calibration not implemented | Passed |
| Generated output files are ignored by git | Passed |
| No model retraining occurred in this milestone | Passed |
| No explainability artifacts were created | Passed |

## Version-Control Check

`git check-ignore -v` confirms the generated evaluation outputs are ignored:

```text
.gitignore:114:outputs/reports/* outputs/reports/model_comparison_test_metrics.csv
.gitignore:114:outputs/reports/* outputs/reports/model_comparison_walk_forward_metrics.csv
.gitignore:114:outputs/reports/* outputs/reports/model_comparison_summary.md
```

## Milestone 6 Boundary Confirmation

- Existing baseline and Logistic Regression reports were consolidated.
- No baseline model code was modified.
- No selected-model code was modified.
- No models were retrained.
- Random Forest was not implemented.
- No explainability artifacts were created.
- No notebooks were created.
- No Streamlit, UI, or dashboard was created.
- Existing specs were not modified.
- `README.md` was not modified.
- Milestone 7 was not started.
