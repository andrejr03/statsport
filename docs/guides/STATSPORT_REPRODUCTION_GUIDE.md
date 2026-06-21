# StatSport Reproduction Guide

**Purpose:** recreate the StatSport data, model, evaluation, and explainability outputs from the
repository and public Football-Data.co.uk CSV files.

This guide is written for a technically literate reviewer on macOS or Windows 11. It uses local
scripts only. No cloud service, GPU, paid infrastructure, Streamlit app, dashboard, API, notebook, or
MLOps platform is required.

## 1. Required Software

Install:

- Git
- Python 3.10 or newer
- A terminal:
  - macOS: Terminal, iTerm, or VS Code terminal
  - Windows 11: PowerShell, Git Bash, or VS Code terminal

Python packages needed for the full workflow:

- `numpy`
- `scikit-learn`

The remaining workflow uses the Python standard library.

## 2. macOS Setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install numpy scikit-learn
```

Confirm Python is available:

```bash
python3 --version
```

## 3. Windows 11 Setup

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy scikit-learn
```

If PowerShell blocks activation, allow local script activation for the current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then rerun:

```powershell
.\.venv\Scripts\Activate.ps1
```

Confirm Python is available:

```powershell
python --version
```

## 4. Acquire Raw Data

Create the raw-data directory if needed:

```bash
mkdir -p data/raw
```

On Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force data/raw
```

Download the five approved Football-Data.co.uk Bundesliga CSVs.

macOS or Git Bash:

```bash
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2020-2021.csv https://www.football-data.co.uk/mmz4281/2021/D1.csv
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2021-2022.csv https://www.football-data.co.uk/mmz4281/2122/D1.csv
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2022-2023.csv https://www.football-data.co.uk/mmz4281/2223/D1.csv
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2023-2024.csv https://www.football-data.co.uk/mmz4281/2324/D1.csv
curl -fL --retry 3 --retry-delay 2 -o data/raw/football-data-co-uk_bundesliga_2024-2025.csv https://www.football-data.co.uk/mmz4281/2425/D1.csv
```

Windows PowerShell:

```powershell
Invoke-WebRequest -Uri https://www.football-data.co.uk/mmz4281/2021/D1.csv -OutFile data/raw/football-data-co-uk_bundesliga_2020-2021.csv
Invoke-WebRequest -Uri https://www.football-data.co.uk/mmz4281/2122/D1.csv -OutFile data/raw/football-data-co-uk_bundesliga_2021-2022.csv
Invoke-WebRequest -Uri https://www.football-data.co.uk/mmz4281/2223/D1.csv -OutFile data/raw/football-data-co-uk_bundesliga_2022-2023.csv
Invoke-WebRequest -Uri https://www.football-data.co.uk/mmz4281/2324/D1.csv -OutFile data/raw/football-data-co-uk_bundesliga_2023-2024.csv
Invoke-WebRequest -Uri https://www.football-data.co.uk/mmz4281/2425/D1.csv -OutFile data/raw/football-data-co-uk_bundesliga_2024-2025.csv
```

Expected raw files:

```text
data/raw/football-data-co-uk_bundesliga_2020-2021.csv
data/raw/football-data-co-uk_bundesliga_2021-2022.csv
data/raw/football-data-co-uk_bundesliga_2022-2023.csv
data/raw/football-data-co-uk_bundesliga_2023-2024.csv
data/raw/football-data-co-uk_bundesliga_2024-2025.csv
```

Each season should contain 306 Bundesliga matches.

## 5. Build Processed Dataset

macOS or Git Bash:

```bash
python3 scripts/process_bundesliga_raw_data.py
```

Windows PowerShell:

```powershell
python scripts/process_bundesliga_raw_data.py
```

Expected output:

```text
data/processed/bundesliga_2020_2025_matches_processed.csv
```

Expected row count:

```text
1530 rows
```

## 6. Build Feature Dataset

macOS or Git Bash:

```bash
python3 scripts/build_bundesliga_features.py
```

Windows PowerShell:

```powershell
python scripts/build_bundesliga_features.py
```

Expected output:

```text
data/processed/bundesliga_2020_2025_features.csv
```

Expected row count:

```text
1530 rows
```

Feature generation uses a five-match rolling window and only prior matches for each team's current
fixture features.

## 7. Run Baseline Model

macOS or Git Bash:

```bash
python3 scripts/evaluate_baseline_model.py
```

Windows PowerShell:

```powershell
python scripts/evaluate_baseline_model.py
```

Expected outputs:

```text
outputs/reports/baseline_test_metrics.csv
outputs/reports/baseline_walk_forward_metrics.csv
outputs/reports/baseline_test_confusion_matrix.csv
```

## 8. Run Logistic Regression

macOS or Git Bash:

```bash
python3 scripts/evaluate_logistic_regression_model.py
```

Windows PowerShell:

```powershell
python scripts/evaluate_logistic_regression_model.py
```

Expected outputs:

```text
outputs/reports/logistic_regression_test_metrics.csv
outputs/reports/logistic_regression_walk_forward_metrics.csv
outputs/reports/logistic_regression_test_confusion_matrix.csv
outputs/reports/logistic_regression_coefficients.csv
```

The selected model trains on 2020/21-2023/24 and tests on 2024/25. Walk-forward validation uses the
approved expanding season blocks.

## 9. Generate Evaluation Outputs

macOS or Git Bash:

```bash
python3 scripts/build_model_comparison_reports.py
```

Windows PowerShell:

```powershell
python scripts/build_model_comparison_reports.py
```

Expected outputs:

```text
outputs/reports/model_comparison_test_metrics.csv
outputs/reports/model_comparison_walk_forward_metrics.csv
outputs/reports/model_comparison_summary.md
```

Expected 2024/25 test comparison:

| Metric | Baseline | Logistic Regression | Delta |
|--------|---------:|--------------------:|------:|
| Accuracy | 0.385620915033 | 0.450980392157 | +0.065359477124 |
| Balanced Accuracy | 0.333333333333 | 0.395709268591 | +0.062375935258 |
| Log Loss | 1.094260218009 | 1.063246819064 | -0.031013398945 |
| Macro-F1 | 0.185534591195 | 0.320700358138 | +0.135165766943 |

Lower Log Loss is better. Higher values are better for the other listed metrics.

## 10. Generate Explainability Outputs

macOS or Git Bash:

```bash
python3 scripts/build_explainability_artifacts.py
```

Windows PowerShell:

```powershell
python scripts/build_explainability_artifacts.py
```

Expected outputs:

```text
outputs/reports/global_feature_influence.csv
outputs/reports/global_feature_influence.md
outputs/reports/model_behaviour_summary.md
outputs/reports/prediction_explanation_card_1.md
outputs/reports/prediction_explanation_card_2.md
outputs/reports/prediction_explanation_card_3.md
outputs/reports/limitations_and_uncertainty.md
```

The explainability step does not retrain Logistic Regression. It reads the exported coefficients and
reconstructs training-only standardization statistics from the approved training rows for local
coefficient contribution analysis.

## 11. Run Validation Tests

macOS or Git Bash:

```bash
python3 -m unittest tests/test_data_processing.py tests/test_feature_engineering.py tests/test_baseline.py tests/test_selected_model.py tests/test_evaluation.py tests/test_explainability.py -v
python3 -m compileall src scripts tests
```

Windows PowerShell:

```powershell
python -m unittest tests/test_data_processing.py tests/test_feature_engineering.py tests/test_baseline.py tests/test_selected_model.py tests/test_evaluation.py tests/test_explainability.py -v
python -m compileall src scripts tests
```

Expected test result at finalization:

```text
Ran 39 tests

OK
```

## 12. Version-Control Expectations

These generated or local files must remain ignored by git:

```text
data/raw/*
data/processed/*
data/external/*
outputs/figures/*
outputs/reports/*
outputs/exports/*
```

The repository commits the code, tests, specifications, evidence, guides, and reviews needed to
recreate the workflow. It does not commit raw data, processed data, generated reports, large model
artifacts, or secrets.

Check ignored outputs:

```bash
git status --short
git check-ignore -v data/raw/football-data-co-uk_bundesliga_2020-2021.csv
git check-ignore -v data/processed/bundesliga_2020_2025_features.csv
git check-ignore -v outputs/reports/model_comparison_summary.md
```

## 13. Troubleshooting

If `ModuleNotFoundError: No module named 'sklearn'` appears, install the required package in the
active environment:

```bash
python3 -m pip install scikit-learn
```

On Windows, use:

```powershell
python -m pip install scikit-learn
```

If a script reports missing raw files, rerun the acquisition commands in section 4 and confirm the
filenames exactly match the expected names.

If generated metrics differ, confirm that the raw files are the same Football-Data.co.uk season CSVs
listed in the acquisition evidence and that scripts were run from the repository root.
