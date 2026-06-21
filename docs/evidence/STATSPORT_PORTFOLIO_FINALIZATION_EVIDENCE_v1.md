# StatSport Portfolio Finalization Evidence v1

**Milestone:** Milestone 8 - Portfolio Finalization  
**Evidence date:** 2026-06-21  
**Final status:** COMPLETE  
**Scope:** Documentation, presentation, reproducibility, and portfolio packaging

## Purpose

This document records evidence that StatSport was finalized as a portfolio-ready repository for
public project review, technical discussion, and GitHub browsing.

This milestone does not retrain models, implement Random Forest, create Streamlit, create dashboards,
create APIs, create notebooks, modify specs, or start post-project enhancements.

## Final Repository State

StatSport now contains:

- documented Football-Data.co.uk Bundesliga data acquisition;
- deterministic data processing;
- leakage-safe feature engineering;
- mandatory home-advantage baseline;
- multinomial Logistic Regression selected model;
- final baseline-versus-selected-model evaluation;
- coefficient-based global and local explainability artifacts;
- final README;
- macOS and Windows 11 reproduction guide;
- completion review with final status `COMPLETE`.

Generated data and reports remain local and ignored by git.

## Implementation Summary

| Layer | Status | Key files |
|-------|--------|-----------|
| Data acquisition | Complete | `docs/evidence/STATSPORT_DATASET_ACQUISITION_EVIDENCE_v1.md` |
| Data processing | Complete | `src/statsport/data_processing.py`, `scripts/process_bundesliga_raw_data.py` |
| Feature engineering | Complete | `src/statsport/feature_engineering.py`, `scripts/build_bundesliga_features.py` |
| Baseline model | Complete | `src/statsport/baseline.py`, `scripts/evaluate_baseline_model.py` |
| Selected model | Complete | `src/statsport/selected_model.py`, `scripts/evaluate_logistic_regression_model.py` |
| Evaluation | Complete | `src/statsport/evaluation.py`, `scripts/build_model_comparison_reports.py` |
| Explainability | Complete | `src/statsport/explainability.py`, `scripts/build_explainability_artifacts.py` |
| Portfolio finalization | Complete | `README.md`, `docs/guides/STATSPORT_REPRODUCTION_GUIDE.md`, `docs/reviews/STATSPORT_COMPLETION_REVIEW_v1.md` |

## Model Summary

The completed modelling workflow compares:

| Model | Role | Status |
|-------|------|--------|
| Home-advantage baseline | Mandatory reference | Complete |
| Multinomial Logistic Regression | Selected model | Complete |
| Random Forest | Fallback only | Not implemented because Logistic Regression was viable |

The prediction target is Home / Draw / Away (`H`, `D`, `A`).

## Evaluation Summary

The approved split is:

| Split | Seasons | Rows |
|-------|---------|-----:|
| Train | 2020/21-2023/24 | 1224 |
| Test | 2024/25 | 306 |

2024/25 test-season comparison:

| Metric | Baseline | Logistic Regression | Delta |
|--------|---------:|--------------------:|------:|
| Accuracy | 0.385620915033 | 0.450980392157 | +0.065359477124 |
| Balanced Accuracy | 0.333333333333 | 0.395709268591 | +0.062375935258 |
| Log Loss | 1.094260218009 | 1.063246819064 | -0.031013398945 |
| Macro-F1 | 0.185534591195 | 0.320700358138 | +0.135165766943 |

Logistic Regression improved over the baseline on all approved core test metrics. Lower Log Loss is
better; higher values are better for the other listed metrics.

The result is useful but modest. The held-out confusion matrix shows that draw prediction remains a
major limitation: Logistic Regression correctly predicted 0 of 77 actual draws in the 2024/25 test
season.

## Explainability Summary

The explainability workflow uses native Logistic Regression interpretation:

- global standardized coefficient rankings;
- model behaviour summary;
- local coefficient contribution analysis;
- feature-difference explanations;
- probability explanations;
- three deterministic prediction explanation cards.

Generated explainability outputs:

```text
outputs/reports/global_feature_influence.csv
outputs/reports/global_feature_influence.md
outputs/reports/model_behaviour_summary.md
outputs/reports/prediction_explanation_card_1.md
outputs/reports/prediction_explanation_card_2.md
outputs/reports/prediction_explanation_card_3.md
outputs/reports/limitations_and_uncertainty.md
```

## Limitations

Final documentation now states:

- Draw-class weakness.
- Modest improvement over baseline.
- Bundesliga-only scope.
- Small held-out test season.
- Coefficients and contributions are not causal claims.
- Generated data and outputs are reproducible local artifacts, not committed deliverables.

## Reproducibility Status

`docs/guides/STATSPORT_REPRODUCTION_GUIDE.md` documents how to:

1. Acquire raw Football-Data.co.uk Bundesliga data.
2. Build the processed match dataset.
3. Build the feature dataset.
4. Run the home-advantage baseline.
5. Run multinomial Logistic Regression.
6. Generate consolidated evaluation outputs.
7. Generate explainability outputs.
8. Run validation tests.

The guide includes both macOS and Windows 11 instructions, required software, Python package notes,
and expected output files.

## Completion Criteria Review

| Criterion | Status |
|-----------|--------|
| Completed implementation reflected in README | Passed |
| Actual model results reported | Passed |
| Actual evaluation metrics reported | Passed |
| Actual limitations reported | Passed |
| Explainability approach documented | Passed |
| Reproduction guide created | Passed |
| Completion review created | Passed |
| Specs left unchanged | Passed |
| No new modelling work | Passed |
| No Streamlit/dashboard/API/notebook created | Passed |
| No Random Forest implementation | Passed |

## Repository Audit

| Audit item | Result |
|------------|--------|
| Raw data ignored | Passed |
| Processed data ignored | Passed |
| Generated outputs ignored | Passed |
| No secrets committed | Passed |
| No notebooks required | Passed |
| No Streamlit | Passed |
| No dashboard | Passed |
| No API | Passed |
| No Random Forest implementation | Passed |
| No scope creep | Passed |

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

Documentation checks:

| Check | Result |
|-------|--------|
| All milestone evidence files exist | Passed |
| Reproduction guide exists | Passed |
| Completion review exists | Passed |
| README references actual results | Passed |
| Reproduction instructions are coherent and ordered | Passed |
| Completion review status is `COMPLETE` | Passed |

## Final Boundary Confirmation

- Milestone 8 finalized documentation and portfolio packaging only.
- No specs were modified.
- No models were retrained.
- Random Forest was not implemented.
- No Streamlit, dashboard, API, notebook, or showcase UI work was created.
- No post-project enhancements were started.
