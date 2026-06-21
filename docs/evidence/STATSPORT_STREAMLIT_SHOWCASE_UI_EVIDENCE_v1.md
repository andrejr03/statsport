# StatSport Streamlit Showcase UI Evidence v1

**Milestone:** Optional post-v1 Streamlit Showcase UI  
**Evidence date:** 2026-06-21  
**Status:** COMPLETE  
**Scope:** Local, read-only portfolio presentation layer over completed StatSport v1 outputs

## Purpose

This document records evidence that the optional StatSport Showcase UI was implemented and validated
as a post-v1 portfolio enhancement. StatSport v1 remains complete without this UI.

The showcase does not create a SaaS product, dashboard product, betting application, live prediction
service, model-training interface, API, database, account system, upload flow, deployment layer, or
new ML workflow.

## Architecture

The implementation creates a single Streamlit entry point:

```text
streamlit_app.py
```

The app is read-only and local-only. It reads already-generated StatSport v1 artifacts from
`data/processed/`, `outputs/reports/`, and `assets/`. It does not run the data pipeline, retrain
models, regenerate reports, call external APIs, write new model outputs, or mutate project data.

No helper module was added under `src/statsport/` because the implementation is small enough to keep
in one app file without adding an unnecessary abstraction.

## Sections Implemented

The app implements the approved showcase structure:

| Section | Status |
|---|---|
| Hero | Complete |
| Problem & Project Overview | Complete |
| Dataset Scope & Feature Pipeline | Complete |
| Baseline vs Logistic Regression | Complete |
| Evaluation Results | Complete |
| Walk-Forward Validation | Complete |
| Confusion Matrix & Draw Limitation | Complete |
| Global Feature Influence | Complete |
| Prediction Explanation Cards | Complete |
| Limitations | Complete |
| Reproducibility | Complete |
| About The Project | Complete |

## Data Sources Used

The UI consumes these existing artifacts:

| Source | Use |
|---|---|
| `assets/STATSPORT_AI_POWERED_FOOTBALL_ANALYTICS_AND_PREDICTION_SHOWCASE.png` | Hero visual. |
| `data/processed/bundesliga_2020_2025_matches_processed.csv` | Match count validation. |
| `data/processed/bundesliga_2020_2025_features.csv` | Feature row count validation. |
| `outputs/reports/model_comparison_test_metrics.csv` | Accuracy, Balanced Accuracy, Log Loss, Macro-F1 cards. |
| `outputs/reports/model_comparison_walk_forward_metrics.csv` | Walk-forward validation table and bars. |
| `outputs/reports/logistic_regression_test_confusion_matrix.csv` | Confusion matrix and draw limitation. |
| `outputs/reports/baseline_test_confusion_matrix.csv` | Required artifact gate for baseline comparison context. |
| `outputs/reports/global_feature_influence.csv` | Home, Draw, and Away feature influence tabs. |
| `outputs/reports/model_behaviour_summary.md` | Logistic Regression explanation content. |
| `outputs/reports/prediction_explanation_card_1.md` | Strong correct prediction explanation card. |
| `outputs/reports/prediction_explanation_card_2.md` | Difficult draw case explanation card. |
| `outputs/reports/prediction_explanation_card_3.md` | Incorrect low-confidence explanation card. |
| `outputs/reports/limitations_and_uncertainty.md` | Limitations section. |

Displayed metrics originate from `outputs/reports/model_comparison_test_metrics.csv`; no synthetic
or placeholder results are used.

## Missing-Artifact Behavior

The app checks required artifacts before rendering the showcase. If required generated outputs are
missing, it displays:

```text
Showcase artifacts not found.

Run the reproduction workflow documented in:

docs/guides/STATSPORT_REPRODUCTION_GUIDE.md
```

Validation used a separate Streamlit server with `STATSPORT_SHOWCASE_ROOT` pointed at an empty
temporary directory. The missing-artifact page rendered the required message and did not crash or show
a traceback.

## Theme Selected

The app uses a dark, premium portfolio theme.

Rationale:

- It aligns with the supplied showcase image.
- It gives the project a memorable admissions/recruiter presentation without introducing betting or
product styling.
- It keeps the football analytics aesthetic restrained and readable.

The app hides Streamlit header/menu/toolbar elements and the image fullscreen control where reasonably
possible so screenshots present the StatSport Showcase UI rather than the developer environment.

## Browser Validation

Browser validation was performed with Playwright CLI against a locally launched Streamlit app.

Streamlit command:

```bash
python3 -m streamlit run streamlit_app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false
```

Playwright CLI steps executed:

```bash
playwright-cli open http://127.0.0.1:8501
playwright-cli resize 1440 1200
playwright-cli snapshot
playwright-cli eval "<section and data-integrity checks>"
playwright-cli screenshot --filename output/playwright/statsport-showcase-home.png
playwright-cli screenshot --filename output/playwright/statsport-showcase-results.png
playwright-cli screenshot --filename output/playwright/statsport-showcase-explainability.png
```

Validation checks confirmed:

- Hero rendered.
- Problem & Project Overview rendered.
- Dataset Scope & Feature Pipeline rendered.
- Baseline vs Logistic Regression rendered.
- Evaluation Results rendered.
- Walk-Forward Validation rendered.
- Confusion Matrix rendered.
- Draw-Class Limitation rendered.
- Global Feature Influence rendered.
- Prediction Explanation Cards rendered.
- Limitations rendered.
- Reproducibility rendered.
- About The Project rendered.
- Bundesliga 2020/21-2024/25 scope appeared.
- 1530 total matches appeared.
- Accuracy, Balanced Accuracy, Log Loss, and Macro-F1 comparisons appeared.
- `0 correct draw predictions out of 77 actual draws` appeared.
- Logistic Regression explanation content appeared.
- No missing-artifact error state appeared in the normal app path.
- No horizontal page overflow was detected at the desktop viewport.

## Screenshots Created

Screenshots were created at:

```text
output/playwright/statsport-showcase-home.png
output/playwright/statsport-showcase-results.png
output/playwright/statsport-showcase-explainability.png
```

Screenshots were captured at a desktop viewport after the UI fully rendered. They showed no loading
state, no app error state, no placeholder sections, and no visible horizontal scrolling.

## Visual Defects Found And Corrected

Playwright validation found escaped raw HTML inside the walk-forward and feature-influence sections.
The issue came from indented generated HTML strings being interpreted as Markdown code blocks.

Correction:

- Converted generated walk-forward bar rows to single-line HTML strings.
- Converted generated feature-ranking rows to single-line HTML strings.
- Re-ran Playwright validation and recaptured screenshots after the correction.

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
python3 -m compileall src scripts tests streamlit_app.py
```

Result: passed.

Screenshot files:

```text
output/playwright/statsport-showcase-home.png
output/playwright/statsport-showcase-results.png
output/playwright/statsport-showcase-explainability.png
```

Result: created.

## Limitations

- The showcase depends on generated local artifacts under `data/processed/` and `outputs/reports/`;
  a fresh clone must run the documented reproduction workflow first.
- The UI is intentionally not a production app and should not be deployed or expanded into product
  behavior.
- Streamlit is an additional local runtime dependency for this optional showcase; it is not required
  for StatSport v1 reproduction.
- The UI visualizes existing results only. It does not improve model quality or address draw-class
  weakness.

## Boundary Confirmation

- No model retraining occurred.
- No new ML work occurred.
- No new metrics were invented.
- No generated data was committed by this implementation.
- No API, database, account system, upload flow, deployment workflow, live prediction flow, or betting
  behavior was introduced.
- StatSport v1 remains complete independently of the Showcase UI.
