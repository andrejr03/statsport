# StatSport Fresh Clone Run Validation v1

**Validation date:** 2026-06-21  
**Repository tested:** `https://github.com/andrejr03/statsport.git`  
**Fresh clone path:** `/Users/agentisstudio/Documents/statsport-fresh-clone-validation`  
**Commit tested:** `ff26dd741d9ee5725aee13faa19d156f07d2f968`  
**Runtime target:** fresh clone only; no files copied from `/Users/agentisstudio/Documents/statsport-ai`

## Purpose

This validation checks whether an external GitHub visitor can clone the public repository, install
dependencies, download the approved raw data, regenerate required artifacts, run tests, launch the
Streamlit Showcase UI, and open it in a browser using the README instructions.

## Setup Commands Run

```bash
rm -rf /Users/agentisstudio/Documents/statsport-fresh-clone-validation
git clone https://github.com/andrejr03/statsport.git /Users/agentisstudio/Documents/statsport-fresh-clone-validation
cd /Users/agentisstudio/Documents/statsport-fresh-clone-validation
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

**Result:** passed. Dependencies installed from `requirements.txt`.

## Data Download Result

Command:

```bash
.venv/bin/python scripts/download_bundesliga_raw_data.py
```

**Result:** passed. The script downloaded all five approved Football-Data.co.uk Bundesliga CSVs:

- `data/raw/football-data-co-uk_bundesliga_2020-2021.csv`
- `data/raw/football-data-co-uk_bundesliga_2021-2022.csv`
- `data/raw/football-data-co-uk_bundesliga_2022-2023.csv`
- `data/raw/football-data-co-uk_bundesliga_2023-2024.csv`
- `data/raw/football-data-co-uk_bundesliga_2024-2025.csv`

## Artifact Regeneration Result

Commands:

```bash
.venv/bin/python scripts/process_bundesliga_raw_data.py
.venv/bin/python scripts/build_bundesliga_features.py
.venv/bin/python scripts/evaluate_baseline_model.py
.venv/bin/python scripts/evaluate_logistic_regression_model.py
.venv/bin/python scripts/build_model_comparison_reports.py
.venv/bin/python scripts/build_explainability_artifacts.py
```

**Result:** passed. The fresh clone regenerated processed data, baseline outputs, Logistic
Regression outputs, comparison reports, and explainability artifacts.

Key outputs observed:

- Processed rows: `1530`
- Feature rows: `1530`
- Baseline test accuracy: `0.38562091503267976`
- Logistic Regression test accuracy: `0.45098039215686275`
- Explanation cards generated: `3`

## Test Result

Command:

```bash
.venv/bin/python -m unittest tests/test_data_processing.py tests/test_feature_engineering.py tests/test_baseline.py tests/test_selected_model.py tests/test_evaluation.py tests/test_explainability.py -v
```

**Result:** passed.

```text
Ran 39 tests in 0.024s

OK
```

## Streamlit Launch Result

Command:

```bash
.venv/bin/streamlit run streamlit_app.py --server.headless true --server.port 8502 --server.address 127.0.0.1
```

**Result:** passed. Streamlit served the app at:

```text
http://127.0.0.1:8502
```

No Streamlit traceback appeared in the server output during validation.

## Playwright Browser Validation Result

Browser validation used the Playwright CLI wrapper from a clean browser session against the fresh
clone Streamlit server.

Commands:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
"$PWCLI" open http://127.0.0.1:8502
"$PWCLI" snapshot
"$PWCLI" click e166
"$PWCLI" snapshot
mkdir -p output/playwright
"$PWCLI" screenshot --filename output/playwright/fresh-clone-showcase-validation.png
```

Observed browser results:

- App loaded successfully.
- No missing-artifact error was shown.
- No Streamlit traceback/error page was shown.
- Prediction Center rendered.
- Probabilities rendered for Home, Draw, and Away outcomes.
- The staged `Reveal actual result` button existed.
- Before reveal, the result area showed `Result hidden`.
- After reveal, the result area showed `Actual Result` and `Incorrect · Draw (0-0)`.
- 2027 showcase framing appeared in the hero and Prediction Center.
- No 2024/2025 date appeared in the hero or Prediction Center area; historical 2024/25 references
  remained visible only in later evidence/track-record sections.

## Screenshot

Screenshot captured in the fresh clone:

```text
/Users/agentisstudio/Documents/statsport-fresh-clone-validation/output/playwright/fresh-clone-showcase-validation.png
```

## Friction Found

- The public run path depends on live internet access to GitHub, PyPI, and Football-Data.co.uk.
- Streamlit printed its standard optional Watchdog performance suggestion on launch; this did not
  block the app.

No repository blocker was found.

## Final Verdict

FRESH CLONE PASS WITH NOTES
