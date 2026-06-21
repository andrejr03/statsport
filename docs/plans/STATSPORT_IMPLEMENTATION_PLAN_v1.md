# StatSport Implementation Plan v1

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Translate the approved StatSport architecture into a concrete, reviewable implementation
roadmap that delivers a finished, reproducible, explainable football prediction portfolio project.

**Architecture:** StatSport remains a linear, local analytics workflow: documented data acquisition
to processed match data, leakage-safe features, baseline and logistic regression models, evaluation,
explainability artifacts, and final portfolio presentation. The workflow must stay laptop-friendly,
cross-platform, and reproducible on macOS and Windows 11.

**Tech Stack:** Python data science tooling is expected, with exact dependencies and implementation
mechanisms deferred to the implementation phase. No cloud services, deployment targets, APIs, user
systems, or MLOps platforms are part of this plan.

---

## 1. Purpose

This plan defines the first implementation roadmap for StatSport after completion of the architecture
phase. It converts the approved decisions into sequenced milestones while preserving the repository's
core rules: specs first, simplicity, honesty, reproducibility, and finishability within the 40-60 hour
budget.

This is a planning document only. It does not create code, datasets, notebooks, scripts, outputs, or
specification changes.

The approved implementation direction is:

- Dataset: Football-Data.co.uk, Bundesliga, seasons 2020/21-2024/25.
- Prediction target: Home / Draw / Away (1X2), with Home Win vs Not Home Win as fallback.
- Core features: home advantage, recent form, goals scored, goals conceded, and goal difference.
- Optional features: shots on target, league position, and one deterministic Elo-style rating.
- Baseline: home-advantage baseline.
- Selected model: multinomial logistic regression.
- Fallback model: random forest only if logistic regression is not viable.
- Evaluation: train on 2020/21-2023/24, test on 2024/25, with season-blocked walk-forward validation.
- Explainability: standardized coefficient analysis globally and coefficient contribution analysis
  locally.

## 2. Implementation Principles

- **Specs are authoritative.** Implementation must conform to `docs/specs/PROJECT_OVERVIEW.md`,
  `DATA_SPEC.md`, `MODELING_SPEC.md`, `EVALUATION_SPEC.md`, `EXPLAINABILITY_SPEC.md`,
  `REPRODUCIBILITY_SPEC.md`, and `PORTFOLIO_HANDOFF_SPEC.md`.
- **Baseline first.** No selected-model claim is valid until the home-advantage baseline exists and
  is evaluated on the same split and metrics.
- **Leakage prevention is a design constraint.** Features must be computed from information available
  before each match. Chronological order must be preserved in training, validation, and testing.
- **Reproducibility beats convenience.** Acquisition, processing, modelling, evaluation, and
  explanation steps must be documented and repeatable without hidden manual knowledge.
- **Explainability remains native and simple.** Logistic regression coefficient-based explanations are
  the default. Heavier explainability tooling is not part of the default path.
- **Finishability controls optional work.** Optional features are included only after the core
  pipeline is complete and validated.
- **Generated data and outputs stay out of git.** Raw data, processed data, external data, large
  outputs, and regenerable artifacts must remain uncommitted.
- **Cross-platform work is required.** Paths and commands should be suitable for macOS and Windows 11,
  with platform-specific instructions documented when unavoidable.

## 3. Success Definition

StatSport succeeds when a reviewer can understand and reproduce the complete workflow:

- Acquire the selected Bundesliga data from Football-Data.co.uk using documented steps.
- Regenerate processed match data and leakage-safe features.
- Train and evaluate the home-advantage baseline and multinomial logistic regression model.
- Compare both models honestly using Accuracy, Balanced Accuracy, Log Loss, Macro-F1, and Confusion
  Matrix, with optional Brier Score and calibration assessment only if time permits.
- Read global and local explanation artifacts that make the model's behaviour understandable.
- Read a portfolio-ready README and supporting documentation that explain motivation, methodology,
  results, limitations, and reproduction steps.

Success is not defined by maximum predictive accuracy. A weak or marginal improvement over the
baseline is acceptable if it is evaluated honestly and explained clearly.

## 4. Repository Areas Affected

The implementation phase is expected to affect these areas after this plan is reviewed:

| Area | Expected responsibility |
|------|-------------------------|
| `docs/` | Reproducibility notes, data provenance, methodology, limitations, and final portfolio narrative. |
| `data/raw/` | Local raw CSVs acquired from Football-Data.co.uk; not committed. |
| `data/processed/` | Regenerable cleaned/model-ready data; not committed. |
| `src/` | Data acquisition helpers, processing logic, feature engineering, modelling, evaluation, and explainability logic. |
| `notebooks/` | Optional exploratory or presentation notebooks if they support the portfolio narrative without becoming hidden workflow state. |
| `outputs/` | Regenerable figures, tables, reports, and explanation artifacts; large or generated contents not committed. |
| `README.md` | Final reviewer-facing project entry point. |
| Dependency/environment files | Minimal reproducible environment definition, if not already present. |

This plan itself creates no implementation files. Exact file names, interfaces, and commands should be
chosen during implementation in the smallest structure that satisfies the specs.

## 5. Implementation Sequence

The project should be implemented in this order, with explicit review gates between milestones:

1. **Milestone 1 - Dataset Acquisition**
2. **Review Gate 1 - Data provenance and scope approval**
3. **Milestone 2 - Data Processing Pipeline**
4. **Review Gate 2 - Processed data and leakage-risk review**
5. **Milestone 3 - Feature Engineering Pipeline**
6. **Review Gate 3 - Feature provenance and temporal integrity review**
7. **Milestone 4 - Baseline Model**
8. **Review Gate 4 - Baseline evaluation review**
9. **Milestone 5 - Selected Model**
10. **Review Gate 5 - Model comparison and fallback decision**
11. **Milestone 6 - Evaluation Pipeline**
12. **Review Gate 6 - Evaluation report review**
13. **Milestone 7 - Explainability Artifacts**
14. **Review Gate 7 - Explanation quality review**
15. **Milestone 8 - Portfolio Finalization**
16. **Review Gate 8 - Portfolio handoff review**

No milestone should start until the prior milestone's exit criteria and review gate are satisfied,
unless the owner explicitly accepts the risk.

## 6. Milestone Breakdown

### Milestone 1 - Dataset Acquisition

**Goal**

Document and execute a reproducible process for obtaining Football-Data.co.uk Bundesliga CSVs for
seasons 2020/21, 2021/22, 2022/23, 2023/24, and 2024/25.

**Inputs**

- `docs/specs/DATA_SPEC.md`
- Football-Data.co.uk Bundesliga CSV source URLs for the approved seasons.
- Repository `.gitignore` rules for `data/raw/`, `data/processed/`, `data/external/`, and `outputs/`.

**Outputs**

- Local raw CSVs under `data/raw/`, not committed.
- Human-readable provenance documentation covering source, license or terms, scope, URLs, acquisition
  date, and any manual acquisition steps.
- A clear note that the data is static, historical, Bundesliga-only, and limited to 2020/21-2024/25.

**Validation requirements**

- Confirm all five seasons are present locally.
- Confirm row counts are plausible for Bundesliga seasons.
- Confirm expected outcome columns exist, including the full-time result needed for 1X2.
- Confirm no raw data is staged or committed.
- Confirm source, license or terms, scope, URLs, and acquisition date are documented.

**Exit criteria**

- A reviewer can reacquire the same raw data from documented steps.
- No raw, processed, or external data is added to version control.
- Dataset scope matches the approved architecture exactly.

### Milestone 2 - Data Processing Pipeline

**Goal**

Create a repeatable process that converts raw season CSVs into a clean, consistent match-level dataset
ready for feature engineering.

**Inputs**

- Local raw Bundesliga CSVs from Milestone 1.
- Data provenance documentation.
- `docs/specs/DATA_SPEC.md`
- `docs/specs/REPRODUCIBILITY_SPEC.md`

**Outputs**

- Regenerable processed match data under `data/processed/`, not committed.
- Documented processing rules for column selection, season labeling, date parsing, team names,
  outcome labels, missingness handling, and ordering.
- A processing summary suitable for inclusion in later README or methodology documentation.

**Validation requirements**

- Confirm each match has a season, date, home team, away team, full-time goals, and 1X2 target label.
- Confirm the processed dataset preserves chronological ordering within each season.
- Confirm missingness is measured and documented rather than silently ignored.
- Confirm transformations are deterministic and rerunnable.
- Confirm processed data is not committed.

**Exit criteria**

- A reviewer can regenerate the processed dataset from raw files and documented steps.
- The processed data supports the approved target and train/test split.
- Data-quality limitations are documented clearly enough to support honest reporting.

### Milestone 3 - Feature Engineering Pipeline

**Goal**

Generate leakage-safe pre-match features for each fixture, starting with the approved core feature set
and adding optional features only if time and clarity allow.

**Inputs**

- Processed match data from Milestone 2.
- `docs/specs/MODELING_SPEC.md`
- `docs/specs/EVALUATION_SPEC.md`
- Approved feature strategy.

**Outputs**

- Regenerable feature dataset under `data/processed/`, not committed.
- Core pre-match features for home advantage, recent form, goals scored, goals conceded, and goal
  difference.
- Optional features only if they stay simple and documented: shots on target, league position, or one
  deterministic Elo-style rating.
- Feature documentation describing definitions, source columns, window choices, and leakage controls.

**Validation requirements**

- Confirm every feature uses only matches before the fixture being predicted.
- Confirm no target or post-match statistic from the same fixture leaks into features.
- Confirm the same feature definitions are used for baseline, selected model, validation, and test.
- Confirm optional features are either implemented with documentation or explicitly deferred.
- Confirm feature values are deterministic when regenerated.

**Exit criteria**

- The feature dataset supports train 2020/21-2023/24 and test 2024/25.
- Core features are complete and interpretable.
- Leakage checks are documented before any model training begins.

### Milestone 4 - Baseline Model

**Goal**

Implement and evaluate the mandatory home-advantage baseline as the reference point for all modelling
claims.

**Inputs**

- Feature dataset from Milestone 3.
- Approved 1X2 target.
- Approved train/test and validation strategy.
- `docs/specs/MODELING_SPEC.md`
- `docs/specs/EVALUATION_SPEC.md`

**Outputs**

- A deterministic home-advantage baseline.
- Baseline predictions and probabilities for validation folds and the 2024/25 test season.
- Baseline metric results for Accuracy, Balanced Accuracy, Log Loss, Macro-F1, and Confusion Matrix.
- Plain-language baseline interpretation.

**Validation requirements**

- Confirm baseline uses no selected-model features beyond allowed historical/home-advantage priors.
- Confirm baseline and future selected model will be evaluated on identical splits.
- Confirm probability outputs are valid for Log Loss.
- Confirm draw-class behaviour is visible in confusion matrix and class-level summaries.

**Exit criteria**

- Baseline results exist before selected-model claims.
- The baseline is simple, transparent, reproducible, and documented.
- The project has a valid reference point for judging logistic regression.

### Milestone 5 - Selected Model

**Goal**

Train and evaluate multinomial logistic regression as the selected interpretable model, using the same
data and procedure as the baseline.

**Inputs**

- Feature dataset from Milestone 3.
- Baseline outputs from Milestone 4.
- Approved train/test split and walk-forward validation.
- `docs/specs/MODELING_SPEC.md`
- `docs/specs/EXPLAINABILITY_SPEC.md`

**Outputs**

- Trained multinomial logistic regression model from the approved training seasons.
- Validation-fold predictions and 2024/25 test predictions.
- Documented preprocessing choices, including scaling or standardization if used.
- Controlled randomness or deterministic configuration where applicable.
- Initial comparison against the baseline.

**Validation requirements**

- Confirm preprocessing is fit only on training data within each split or fold.
- Confirm validation and test data do not influence model fitting.
- Confirm the model produces probabilities for all 1X2 classes.
- Confirm coefficients are available for global and local explanation.
- Confirm random forest fallback is used only if logistic regression is not viable or cannot be
  interpreted credibly.

**Exit criteria**

- Logistic regression has been trained and evaluated on the same basis as the baseline.
- Any improvement or weakness relative to the baseline is visible and not overstated.
- Coefficients and preprocessing artifacts are suitable for Milestone 7 explainability.

### Milestone 6 - Evaluation Pipeline

**Goal**

Produce the final honest model comparison using the approved train/test split, walk-forward
validation, and core metrics.

**Inputs**

- Baseline predictions and probabilities.
- Logistic regression predictions and probabilities.
- Approved evaluation strategy.
- `docs/specs/EVALUATION_SPEC.md`

**Outputs**

- Walk-forward validation results:
  - Train 2020/21 -> validate 2021/22.
  - Train 2020/21-2021/22 -> validate 2022/23.
  - Train 2020/21-2022/23 -> validate 2023/24.
- Final 2024/25 test results for baseline and logistic regression.
- Core metric tables for Accuracy, Balanced Accuracy, Log Loss, Macro-F1, and Confusion Matrix.
- Optional Brier Score and calibration assessment only if time permits.
- Evaluation narrative covering uncertainty, draw-class difficulty, and limitations.

**Validation requirements**

- Confirm baseline and selected model are compared on the same rows and folds.
- Confirm chronological order is respected throughout.
- Confirm no metric shopping occurs; all approved core metrics are reported.
- Confirm weak or null results are reported honestly.
- Confirm results are traceable to the data, model, and split procedure.

**Exit criteria**

- The project can make a defensible baseline-versus-model statement.
- Evaluation is complete enough for a portfolio reviewer to trust the claims.
- Any limitations are documented before final portfolio writing begins.

### Milestone 7 - Explainability Artifacts

**Goal**

Create reader-facing global and local explanations using native logistic regression interpretability.

**Inputs**

- Final logistic regression model and preprocessing artifacts.
- Feature definitions and standardized feature values.
- Evaluation outputs from Milestone 6.
- `docs/specs/EXPLAINABILITY_SPEC.md`

**Outputs**

- Global feature influence table or figure using standardized coefficient analysis.
- Model behaviour summary explaining how the model tends to predict home, draw, and away outcomes.
- Three prediction explanation cards.
- Feature context tables for the selected example predictions.
- Limitations and uncertainty note tied to evaluation results.

**Validation requirements**

- Confirm global explanations are class-specific and use standardized coefficients.
- Confirm local explanations trace prediction probabilities to coefficient contributions.
- Confirm examples include honest cases, not only flattering correct predictions.
- Confirm explanations use plain language suitable for non-expert reviewers.
- Confirm explanations are regenerable and traceable to the evaluated model.

**Exit criteria**

- A reader can answer why the model made representative predictions.
- Global and local explanations are consistent with each other and with evaluation results.
- Limitations and uncertainty are visible, not buried.

### Milestone 8 - Portfolio Finalization

**Goal**

Turn the implemented workflow into a finished portfolio artifact that is clear, honest, reproducible,
and ready for review.

**Inputs**

- Completed data, feature, model, evaluation, and explainability workflows.
- Final evaluation and explanation artifacts.
- `docs/specs/PORTFOLIO_HANDOFF_SPEC.md`
- `docs/specs/REPRODUCIBILITY_SPEC.md`

**Outputs**

- Clear README covering motivation, problem, data, methodology, baseline, selected model, results,
  explainability, limitations, reproducibility, and repository navigation.
- Documentation updates covering acquisition, processing, modelling, evaluation, explanation, and
  known limitations.
- Regenerable portfolio artifacts, figures, and tables.
- Final reproducibility instructions for macOS and Windows 11 where needed.

**Validation requirements**

- Confirm README claims match actual results and do not overstate performance.
- Confirm reproduction steps are sufficient for a technically literate reviewer.
- Confirm generated artifacts are either committed only when appropriate or documented as
  regenerable outputs.
- Confirm no raw/processed/external data, large outputs, or secrets are committed.
- Confirm all completion criteria in `PORTFOLIO_HANDOFF_SPEC.md` are satisfied or explicitly
  explained.

**Exit criteria**

- The repository is understandable in minutes and reproducible with documented steps.
- The project presents an honest baseline-versus-logistic-regression result.
- The portfolio artifact is finished enough to stop polishing and ship.

## 7. Validation Gates

### Review Gate 1 - Data Provenance and Scope Approval

Occurs after Milestone 1.

- Confirm the data source, league, seasons, URLs, license or terms, and acquisition date are recorded.
- Confirm no data files were committed.
- Confirm the scope is exactly Football-Data.co.uk Bundesliga 2020/21-2024/25.
- Decision: proceed to processing, or fix acquisition/provenance gaps.

### Review Gate 2 - Processed Data and Leakage-Risk Review

Occurs after Milestone 2.

- Confirm processed rows represent valid matches and preserve season/date order.
- Confirm 1X2 target labels are correct and fallback labels can be derived if needed.
- Confirm missingness and data-quality issues are documented.
- Decision: proceed to features, or fix processing/data-quality issues.

### Review Gate 3 - Feature Provenance and Temporal Integrity Review

Occurs after Milestone 3.

- Confirm each feature is pre-match and leakage-safe.
- Confirm core features are complete before optional features are considered.
- Confirm optional features have not expanded scope beyond the budget.
- Decision: proceed to baseline, defer optional features, or fix leakage risks.

### Review Gate 4 - Baseline Evaluation Review

Occurs after Milestone 4.

- Confirm the home-advantage baseline is implemented before selected-model claims.
- Confirm baseline metrics use the approved split and core metrics.
- Confirm probability outputs are valid for Log Loss.
- Decision: proceed to logistic regression, or correct the baseline.

### Review Gate 5 - Model Comparison and Fallback Decision

Occurs after Milestone 5.

- Confirm logistic regression is evaluated on the same folds and test season as the baseline.
- Confirm preprocessing is fitted only on training data.
- Confirm coefficients support planned explanations.
- Decision: continue with logistic regression, or document a justified switch to the random forest
  fallback.

### Review Gate 6 - Evaluation Report Review

Occurs after Milestone 6.

- Confirm all core metrics are reported.
- Confirm confusion matrices and class-level results expose draw-class performance.
- Confirm the final interpretation is proportionate to the evidence.
- Decision: proceed to explainability, or revise evaluation/reporting.

### Review Gate 7 - Explanation Quality Review

Occurs after Milestone 7.

- Confirm global and local explanations are reader-facing and traceable.
- Confirm explanation cards include uncertainty and limitations.
- Confirm no explanation depends on undocumented manual reasoning.
- Decision: proceed to portfolio finalization, or refine explanation artifacts.

### Review Gate 8 - Portfolio Handoff Review

Occurs after Milestone 8.

- Confirm completion criteria are met.
- Confirm README and docs align with specs and actual results.
- Confirm reproduction steps work on a typical laptop and note macOS/Windows 11 considerations.
- Decision: mark StatSport complete, or fix remaining reproducibility/presentation gaps.

## 8. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Data source changes or access issues | Reproduction becomes harder. | Record URLs, acquisition date, source terms, and exact scope. |
| Licensing ambiguity | Public portfolio use becomes uncertain. | Review and document Football-Data.co.uk terms before relying on data. |
| Data leakage in rolling features | Evaluation becomes over-optimistic. | Review feature provenance before modelling; compute features only from prior matches. |
| Draw-class weakness | Aggregate results may look misleading. | Report Balanced Accuracy, Macro-F1, confusion matrix, and draw-class limitations. |
| Optional feature creep | Project exceeds the 40-60 hour budget. | Complete core pipeline first; defer optional features unless clearly budget-safe. |
| Logistic regression underperforms | Portfolio narrative may feel weak. | Report honestly; compare to baseline; use fallback only if justified and documented. |
| Explainability becomes too technical | Reviewers may not understand the result. | Use plain-language coefficient and contribution explanations. |
| Reproducibility gaps | Reviewer cannot recreate results. | Document every required step and keep generated data out of version control. |
| Over-polishing presentation | Other portfolio projects lose time. | Stop when completion criteria are met. |

## 9. Out-of-Scope Items

The implementation must explicitly exclude:

- Live prediction services.
- Betting functionality.
- SaaS features.
- APIs.
- Dashboards.
- User accounts.
- MLOps infrastructure.
- Cloud deployment.
- Real-time or streaming data feeds.
- Paid data sources or subscription feeds.
- Deep-learning-first approaches, large neural networks, foundation models, or LLM-based modelling.
- Large multi-league expansion beyond the approved Bundesliga scope.
- Exhaustive hyperparameter searches, model zoos, AutoML, or leaderboard chasing.
- SHAP or LIME by default for logistic regression explanations.

These items may be mentioned as future work only when doing so supports honest scope communication.
They must not be implemented as part of StatSport v1.

## 10. Completion Criteria

The implementation should be considered complete when all of the following are true:

- [ ] Baseline implemented.
- [ ] Logistic regression implemented.
- [ ] Evaluation complete.
- [ ] Explainability artifacts complete.
- [ ] Portfolio artifacts complete.
- [ ] Repository reproducible.

Expanded completion checks:

- [ ] Dataset acquisition is documented for Football-Data.co.uk Bundesliga 2020/21-2024/25.
- [ ] Processed data and features are regenerable from documented steps.
- [ ] Core feature set is complete and leakage-safe.
- [ ] Train/test split is train 2020/21-2023/24 and test 2024/25.
- [ ] Season-blocked walk-forward validation is complete.
- [ ] Accuracy, Balanced Accuracy, Log Loss, Macro-F1, and Confusion Matrix are reported for baseline
      and logistic regression.
- [ ] Results are framed against the baseline and stated honestly, including weak or null findings.
- [ ] Global standardized coefficient analysis is complete.
- [ ] Local coefficient contribution explanations are complete for three prediction cards.
- [ ] Limitations and uncertainty are documented clearly.
- [ ] README and supporting documentation are consistent with the specs and actual results.
- [ ] Raw data, processed data, external data, large generated outputs, and secrets are not committed.
- [ ] Reproduction steps are sufficient for a technically literate reviewer on a typical laptop.
- [ ] The project remains within the approved scope, budget, and non-goals.

The next natural step after this document is review of
`docs/plans/STATSPORT_IMPLEMENTATION_PLAN_v1.md`.
