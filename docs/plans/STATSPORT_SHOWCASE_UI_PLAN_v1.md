# StatSport Showcase UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task if the owner approves this post-v1 enhancement. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create an optional Streamlit showcase layer that presents the completed StatSport v1 project as a premium, memorable portfolio demonstration.

**Architecture:** Build a local, read-only presentation app over the already-generated StatSport outputs. The UI must not create new modelling work, retrain models, change project claims, or redefine v1 completion.

**Tech Stack:** Streamlit, Python standard library, generated CSV/Markdown outputs under `outputs/reports/`, processed local CSVs under `data/processed/`, and the existing showcase image under `assets/`.

---

## 1. Purpose

The StatSport Showcase UI is an optional post-v1 presentation layer for the already complete StatSport repository. Its purpose is to make the finished project easier to understand, remember, and discuss during admissions review, internship screening, GitHub browsing, and technical portfolio review.

This plan does not reopen StatSport v1 scope. StatSport v1 is complete without this UI. The showcase should sit on top of completed outputs and communicate the existing work more vividly, not add a new product surface or new ML capability.

The UI must preserve the repository constitution:

- It is not a SaaS product.
- It is not a betting platform.
- It is not a live prediction service.
- It is not a dashboard product.
- It is not a model experimentation interface.
- It is a portfolio demonstration layer over completed, reproducible outputs.

## 2. Showcase Objectives

The showcase should:

- Present the project story in a guided sequence: Problem -> Dataset -> Features -> Baseline -> Selected Model -> Results -> Explainability -> Limitations -> Reproducibility.
- Make the baseline-versus-Logistic-Regression comparison visually clear.
- Surface the most important honest result: Logistic Regression improves aggregate metrics, but draw prediction remains weak.
- Make coefficient-based explainability understandable to non-expert reviewers.
- Use the existing showcase image as visual inspiration without becoming a marketing landing page.
- Keep the implementation lightweight enough that it does not undermine the completed v1 repository.
- Provide a memorable first impression while remaining technically honest and traceable.

The showcase should not replace the README, specs, evidence files, or reproduction guide. It should act as a visual front door for reviewers who benefit from an interactive walkthrough.

## 3. Target Audience

Primary audiences:

- University admissions reviewers who want to understand the project quickly.
- Internship recruiters who skim for evidence of practical data and ML competence.
- GitHub visitors who may not read every evidence document.
- Technical portfolio reviewers who want to inspect methodology, results, and limitations.

Reader assumptions:

- They may understand programming or data science at a high level.
- They may not know football modelling, multiclass metrics, or coefficient interpretation.
- They have limited time and need the project story to be clear in minutes.
- They value honesty, scope control, and reproducibility more than inflated claims.

## 4. Design Principles

The showcase should follow these design principles:

- **Portfolio-first:** Every screen should help a reviewer understand competence, judgment, and completion.
- **Evidence-backed:** Every displayed metric or claim should trace to an existing generated artifact or documented source.
- **Narrative over controls:** The app should guide the reader through the project rather than ask them to discover meaning through filters.
- **Dark, premium, restrained:** Use the provided image's dark football-analytics mood, but keep readability and credibility ahead of visual drama.
- **Honest by design:** Limitations should appear in the main story, not as a hidden footnote.
- **No product affordances:** Avoid account, live prediction, upload, API, deployment, betting, odds, or "try a match" flows.
- **Local and reproducible:** The app should run after the documented v1 reproduction steps regenerate local artifacts.
- **Small maintenance surface:** Prefer a single app file plus simple helper functions if implementation is approved.

## 5. Information Architecture

### Showcase Scope Decision

The UI should be **hybrid**.

Definition: one Streamlit app entry point with a single narrative page, sidebar navigation, and focused in-section tabs or expanders where they reduce clutter.

Why not pure single-page:

- A pure scroll-only page would become long and tiring because the project includes dataset scope, model comparison, multiple metrics, confusion matrices, global explanations, local explanation cards, limitations, and reproduction guidance.
- Reviewers need quick jumps to Results, Explainability, and Reproducibility.

Why not full multi-page:

- Multi-page Streamlit would imply a heavier app structure and can feel like a product dashboard.
- The project story is linear and portfolio-oriented; splitting it into separate pages would weaken the guided narrative.
- More pages increase maintenance cost and the risk of inconsistent copy.

Hybrid is the best fit because it preserves the story while letting reviewers jump to specific evidence.

### Final UI Structure

Use the following final structure:

1. Hero and project status
2. Problem and project overview
3. Dataset scope and feature pipeline
4. Baseline versus selected model
5. Evaluation results
6. Walk-forward validation
7. Confusion matrix and draw-class limitation
8. Global feature influence
9. Prediction explanation cards
10. Limitations and uncertainty
11. Reproducibility and repository structure
12. About the project

### Candidate Section Evaluation

| Candidate section | Decision | Placement / rationale |
|---|---|---|
| Hero | Include | First viewport. Establish project name, completion, scope, and visual identity. |
| Project Overview | Include | Explain what StatSport is and is not. |
| Dataset Scope | Include | Required to ground the modelling claims in Bundesliga 2020/21-2024/25. |
| Baseline vs Logistic Regression | Include | Central ML judgment signal. |
| Evaluation Results | Include | Show test-season metrics clearly against the baseline. |
| Walk-Forward Validation | Include | Show evaluation rigor without overcomplicating the story. |
| Confusion Matrix | Include | Necessary for class-level honesty. |
| Draw-Class Limitation | Include prominently | Main honest limitation; should be visible near the confusion matrix. |
| Global Feature Influence | Include | Core global explainability artifact. |
| Prediction Explanation Cards | Include | Core local explainability artifact. |
| Reproducibility | Include | Major portfolio signal and spec requirement. |
| Repository Structure | Include | Helps GitHub and technical reviewers navigate the project. |
| Limitations | Include | Must be in the main narrative, not hidden. |
| About The Project | Include compactly | Footer-level context: university portfolio, bounded scope, no product claim. |

## 6. Page Architecture

### 6.1 Hero And Project Status

Purpose: create a memorable first impression without implying product scope.

Content:

- Title: `StatSport`
- Subtitle: `Explainable football match prediction from historical Bundesliga data`
- Status chip: `Complete portfolio project`
- Scope chips: `Bundesliga 2020/21-2024/25`, `Home / Draw / Away`, `Baseline vs Logistic Regression`, `Reproducible locally`
- Background or side visual based on `assets/STATSPORT_AI_POWERED_FOOTBALL_ANALYTICS_AND_PREDICTION_SHOWCASE.png`
- Compact boundary note: `Portfolio showcase only. No live predictions, betting, accounts, APIs, or deployment.`

### 6.2 Problem And Project Overview

Purpose: explain the project in plain language.

Content:

- What problem is being addressed.
- Why the problem is bounded.
- What the completed workflow demonstrates: data acquisition, processing, features, baseline, selected model, evaluation, explainability, and reproducibility.
- What the project deliberately does not do.

### 6.3 Dataset Scope And Feature Pipeline

Purpose: show that the data foundation is real, bounded, and leakage-aware.

Content:

- Dataset source: Football-Data.co.uk.
- League: Bundesliga.
- Seasons: 2020/21 through 2024/25.
- Total matches: 1530.
- Train/test split: train 2020/21-2023/24, test 2024/25.
- Core feature families:
  - home advantage;
  - recent form points;
  - goals scored;
  - goals conceded;
  - goal difference;
  - home-minus-away differences.
- Leakage note: rolling features use prior matches only.

Presentation:

- Use compact metric tiles for seasons, total rows, train rows, and test rows.
- Use a simple left-to-right pipeline: Raw Bundesliga CSVs -> processed matches -> rolling features -> models -> evaluation and explanations.

### 6.4 Baseline Versus Selected Model

Purpose: show the baseline-first modelling discipline.

Content:

- Baseline: home-advantage baseline.
- Selected model: multinomial Logistic Regression.
- Explain why Logistic Regression fits the project: interpretable, deterministic, classical, sufficient improvement, native coefficients.
- Mention Random Forest only as a fallback that was not implemented because Logistic Regression was viable.

Presentation:

- Two side-by-side model cards.
- Each card should show role, input type, interpretability level, and portfolio reason.
- Avoid making the selected model look like a production predictor.

### 6.5 Evaluation Results

Purpose: communicate measured improvement clearly and honestly.

Content from `outputs/reports/model_comparison_test_metrics.csv`:

- Accuracy: baseline 0.385620915033, Logistic Regression 0.450980392157, delta +0.065359477124.
- Balanced Accuracy: baseline 0.333333333333, Logistic Regression 0.395709268591, delta +0.062375935258.
- Log Loss: baseline 1.094260218009, Logistic Regression 1.063246819064, delta -0.031013398945.
- Macro-F1: baseline 0.185534591195, Logistic Regression 0.320700358138, delta +0.135165766943.

Presentation:

- Use four metric comparison cards.
- Each card should show baseline, selected model, delta, and whether higher or lower is better.
- Use restrained positive color for improvement and a neutral note that the improvement is useful but modest.

### 6.6 Walk-Forward Validation

Purpose: show the evaluation was not a one-off lucky split.

Content from `outputs/reports/model_comparison_walk_forward_metrics.csv`:

- Fold 1: train 2020/21, validate 2021/22.
- Fold 2: train 2020/21-2021/22, validate 2022/23.
- Fold 3: train 2020/21-2022/23, validate 2023/24.
- Show that Logistic Regression improved over the baseline across the approved core metrics in all three folds.

Presentation:

- Use a compact line or grouped bar chart for metric deltas by fold.
- Keep the chart focused on deltas, not raw metric overload.
- Include a one-sentence interpretation: the selected model improved consistently, but not enough to erase class-specific limitations.

### 6.7 Confusion Matrix And Draw-Class Limitation

Purpose: make the main limitation impossible to miss.

Content from `outputs/reports/logistic_regression_test_confusion_matrix.csv`:

| Actual | Predicted H | Predicted D | Predicted A |
|---|---:|---:|---:|
| H | 105 | 0 | 13 |
| D | 59 | 0 | 18 |
| A | 77 | 1 | 33 |

Required interpretation:

- The selected model correctly predicted 0 of 77 actual draws.
- It made only 1 draw prediction in the test season.
- This is a valid result, not a defect to hide.
- Aggregate improvement and draw-class weakness can both be true.

Presentation:

- Use a heatmap-style confusion matrix.
- Add a nearby limitation card titled `Draws remain hard`.
- Do not use celebratory language around the model.

### 6.8 Global Feature Influence

Purpose: show how the Logistic Regression model behaves overall.

Content from `outputs/reports/global_feature_influence.csv`:

- Top Home feature: `goals_scored_diff`, coefficient 0.108201929510.
- Top Draw feature: `home_recent_form_points_avg`, coefficient 0.204890671918.
- Top Away feature: `away_goals_scored_avg`, coefficient 0.146336245615.
- Class-specific top-ranked feature lists.
- Plain-language coefficient interpretation.

Presentation:

- Use class tabs: Home, Draw, Away.
- Within each tab, show a ranked horizontal bar chart by absolute coefficient.
- Use color or direction markers for positive versus negative coefficients.
- Always label coefficients as associations in this model, not causal effects.

### 6.9 Prediction Explanation Cards

Purpose: show local explainability for individual predictions.

Content from:

- `outputs/reports/prediction_explanation_card_1.md`
- `outputs/reports/prediction_explanation_card_2.md`
- `outputs/reports/prediction_explanation_card_3.md`

Required card types:

- Strong correct prediction: Bayern Munich vs Heidenheim, 2024-12-07, actual H, predicted H.
- Difficult draw case: Heidenheim vs Bochum, 2025-05-02, actual D, predicted H.
- Incorrect low-confidence case: RB Leipzig vs Werder Bremen, 2025-01-12, actual H, predicted A.

Presentation:

- Use three cards with consistent structure:
  - category;
  - match context;
  - predicted probabilities;
  - top contributing features;
  - feature-difference context;
  - confidence discussion.
- The cards should include both successful and unsuccessful examples to avoid cherry-picking.
- Probability bars should use Home, Draw, Away colors consistently.

### 6.10 Limitations And Uncertainty

Purpose: preserve the honest portfolio narrative.

Content from `outputs/reports/limitations_and_uncertainty.md`:

- Draw-class weakness.
- Non-causality warning.
- Bundesliga-only scope.
- Small-data limitations.
- Modest baseline improvement.

Presentation:

- Use a plain limitations section with concise cards.
- Avoid hiding this in an expander by default.
- Make it visually calm and credible.

### 6.11 Reproducibility And Repository Structure

Purpose: show that the project can be recreated and reviewed.

Content:

- Link or reference `docs/guides/STATSPORT_REPRODUCTION_GUIDE.md`.
- Summarize the reproduction commands at a high level.
- Show expected output groups:
  - processed data;
  - baseline outputs;
  - Logistic Regression outputs;
  - model comparison outputs;
  - explainability outputs;
  - tests.
- Show repository map:
  - `src/statsport/`;
  - `scripts/`;
  - `tests/`;
  - `docs/specs/`;
  - `docs/evidence/`;
  - `docs/guides/`;
  - `docs/reviews/`;
  - `data/`;
  - `outputs/`.

Presentation:

- Use a compact repository map, not a full file browser.
- Include a clear note that raw data, processed data, and generated outputs are local and ignored by git.

### 6.12 About The Project

Purpose: close the story with portfolio context.

Content:

- StatSport is one of three summer portfolio repositories.
- It demonstrates a completed, bounded, explainable ML workflow.
- v1 completion remains independent of the showcase UI.
- The UI is optional enhancement, not required for portfolio correctness.

## 7. Data Sources

The showcase should consume existing regenerated outputs only. It should not create new data or modelling artifacts.

### Required Runtime Sources

Use these exact sources:

| Source | Use in UI |
|---|---|
| `assets/STATSPORT_AI_POWERED_FOOTBALL_ANALYTICS_AND_PREDICTION_SHOWCASE.png` | Hero visual inspiration and optional image asset. |
| `data/processed/bundesliga_2020_2025_matches_processed.csv` | Dataset scope counts, seasons, match totals, and train/test row checks if generated locally. |
| `data/processed/bundesliga_2020_2025_features.csv` | Feature-count and feature-family checks if generated locally. |
| `outputs/reports/model_comparison_test_metrics.csv` | Main test-season metric comparison cards. |
| `outputs/reports/model_comparison_walk_forward_metrics.csv` | Walk-forward validation visualization. |
| `outputs/reports/logistic_regression_test_confusion_matrix.csv` | Selected-model confusion matrix. |
| `outputs/reports/baseline_test_confusion_matrix.csv` | Baseline confusion matrix if a side-by-side comparison is desired. |
| `outputs/reports/global_feature_influence.csv` | Feature influence charts and ranked feature tables. |
| `outputs/reports/model_behaviour_summary.md` | Plain-language model behavior copy. |
| `outputs/reports/prediction_explanation_card_1.md` | Strong correct prediction card. |
| `outputs/reports/prediction_explanation_card_2.md` | Difficult draw case card. |
| `outputs/reports/prediction_explanation_card_3.md` | Incorrect low-confidence card. |
| `outputs/reports/limitations_and_uncertainty.md` | Limitations section. |

### Reference-Only Sources

These should be linked or summarized, not parsed as primary UI data:

- `README.md`
- `docs/guides/STATSPORT_REPRODUCTION_GUIDE.md`
- `docs/reviews/STATSPORT_COMPLETION_REVIEW_v1.md`
- `docs/evidence/STATSPORT_PORTFOLIO_FINALIZATION_EVIDENCE_v1.md`
- `docs/specs/`

### Do Not Consume

The showcase should not consume:

- raw Football-Data.co.uk files directly;
- bookmaker odds fields;
- live data;
- external APIs;
- databases;
- user-uploaded data;
- newly trained models;
- uncommitted manual screenshots as evidence;
- any source outside the documented v1 workflow.

### Missing Artifact Behavior

Because `data/` and `outputs/` contents are ignored by git, a fresh clone may not have these files until the reproduction workflow runs. The app, if implemented, should fail gracefully with a clear message:

```text
Showcase artifacts not found. Run the reproduction workflow in docs/guides/STATSPORT_REPRODUCTION_GUIDE.md, then restart the showcase.
```

It should not silently substitute fake numbers.

## 8. Visual Design Direction

### Dark Mode Direction

Use dark mode as the default and only theme. The provided showcase image supports a premium, night-match analytics feel. The UI should use:

- deep charcoal or near-black page background;
- off-white primary text;
- muted gray secondary text;
- restrained accent colors for Home, Draw, Away, and metric improvement;
- no neon overload;
- no casino, betting, or odds-board styling.

### Visual Hierarchy

Recommended hierarchy:

- Hero title: largest type, reserved only for `StatSport`.
- Section headings: clear and compact.
- Metric values: prominent but not oversized.
- Explanatory prose: short paragraphs near the visualization they explain.
- Warnings and limitations: visually distinct but calm.

### Typography Hierarchy

Use Streamlit-compatible typography and CSS only if necessary:

- Page title: strong, high-contrast, 40-52px equivalent.
- Section heading: 24-32px equivalent.
- Card title: 16-20px equivalent.
- Body copy: 15-17px equivalent.
- Metric labels: 12-14px equivalent, uppercase only sparingly.

Avoid decorative fonts. The UI should feel analytical and premium, not sporty in a novelty way.

### Cards

Use cards for repeated units only:

- metric comparison cards;
- model role cards;
- limitation cards;
- prediction explanation cards.

Do not nest cards inside cards. Keep border radius modest, around 6-8px. Use subtle borders over heavy shadows.

### Metric Presentation

Metric cards should show:

- metric name;
- baseline value;
- Logistic Regression value;
- delta;
- better direction;
- one-line interpretation.

Use improvement color carefully. For Log Loss, negative delta is good; do not assume all positive deltas are better.

### Feature Ranking Presentation

Feature influence should use:

- class tabs for Home, Draw, Away;
- horizontal bars sorted by absolute coefficient;
- visible sign/direction labels;
- plain-language feature names when available from `global_feature_influence.csv`;
- a persistent note that coefficients are associations, not causal claims.

### Prediction-Card Presentation

Prediction cards should use:

- consistent Home / Draw / Away probability bars;
- match context at the top;
- actual versus predicted outcome chips;
- top feature contributions as a small table or compact bar list;
- confidence discussion in plain language;
- explicit category labels: strong correct, difficult draw, incorrect low-confidence.

The visual design should make the incorrect and difficult examples look intentional, not embarrassing or hidden.

## 9. Interaction Model

The interaction model should be limited and reviewer-friendly.

Recommended interactions:

- Sidebar table of contents for jumping between major story sections.
- Tabs for Home, Draw, and Away feature influence.
- Tabs or segmented controls for the three prediction explanation cards.
- Optional metric selector in the walk-forward chart, limited to approved metrics.
- Expanders only for secondary implementation details, such as reproduction commands.

Avoid:

- match prediction forms;
- editable inputs that imply live prediction;
- uploads;
- accounts;
- filters over raw match data;
- interactive betting-style probability exploration;
- anything that looks like a reusable analytics product.

Default state should tell the whole story without requiring interaction. Interactions should clarify, not hide the narrative.

## 10. Technical Architecture

### Streamlit Appropriateness

Streamlit is appropriate for this optional showcase if implementation remains local, read-only, and small.

Reasons Streamlit fits:

- It is fast to build for a Python data project.
- It can read CSV and Markdown outputs directly.
- It supports simple metric cards, charts, tabs, and layout without frontend infrastructure.
- It is easy for reviewers to run locally after reproduction.
- It aligns with the repository's Python workflow.

Conditions for using Streamlit:

- The UI must not become required for v1 completion.
- The UI must not add data acquisition, training, serving, or deployment responsibilities.
- The UI must consume generated outputs rather than recomputing results.
- Dependencies must remain modest and documented if implementation is approved.
- The app should run locally on macOS and Windows 11.

### Alternatives Evaluated

| Alternative | Fit | Trade-off |
|---|---|---|
| README only | Already complete | Lowest maintenance, but less memorable and less interactive. |
| Static HTML page | Good visual control | More frontend work; less natural for CSV/Markdown data binding. |
| Quarto report | Strong narrative report | Less app-like; may add unfamiliar tooling. |
| Jupyter notebook | Familiar for data science | Weaker portfolio first impression; notebooks were deliberately not required for v1. |
| Plotly Dash | Powerful | More product-like and heavier than needed. |
| Streamlit | Best optional fit | Quick, local, Python-native, but must be constrained to avoid dashboard/product creep. |

### Complexity Trade-Offs

The showcase adds value only if it stays small. A reasonable implementation should be no more than:

- one Streamlit app file;
- one small helper module if parsing Markdown becomes messy;
- optional lightweight CSS file;
- no database;
- no API;
- no deployment configuration;
- no model execution;
- no training code;
- no generated data committed.

If the showcase requires significant app architecture, custom frontend work, hosting, authentication, or new data pipelines, it should be stopped.

### Maintenance Cost

Expected maintenance cost is low if the app reads stable generated artifacts. Main maintenance risks:

- output filenames or schemas change;
- Markdown card formats change;
- Streamlit dependency changes;
- CSS customization becomes brittle.

Mitigation:

- Treat output schemas as simple read contracts.
- Keep parsing minimal.
- Prefer CSV sources for charts and Markdown sources for reader-facing copy.
- Include graceful missing-artifact messages.
- Avoid visual flourishes that depend on fragile custom CSS.

### Portfolio Value

Portfolio value is moderate to high if the UI is polished and bounded:

- Admissions reviewers get a fast project walkthrough.
- Recruiters see communication skill quickly.
- Technical reviewers can inspect results and limitations without hunting through files.
- The project becomes more memorable while preserving honesty.

Portfolio value becomes negative if the UI suggests StatSport is an unfinished product, betting system, or live prediction service.

## 11. Portfolio Storytelling Flow

The UI should follow this exact story:

```text
Problem
|
Dataset
|
Features
|
Baseline
|
Selected Model
|
Results
|
Explainability
|
Limitations
|
Reproducibility
```

Narrative beats:

1. **Problem:** Predicting football outcomes is recognizable but uncertain, making it a good test of honest ML practice.
2. **Dataset:** The project uses a bounded Bundesliga dataset from Football-Data.co.uk, five completed seasons, 1530 matches.
3. **Features:** Features are pre-match rolling summaries, designed to avoid leakage and remain interpretable.
4. **Baseline:** A simple home-advantage baseline is required before any selected-model claim.
5. **Selected Model:** Multinomial Logistic Regression is chosen because it is deterministic, classical, and explainable.
6. **Results:** Logistic Regression improves over the baseline across approved metrics, but the improvement is modest.
7. **Explainability:** Coefficients and prediction cards show how the model reaches decisions.
8. **Limitations:** Draw prediction remains weak, and coefficients are not causal claims.
9. **Reproducibility:** The full workflow can be regenerated locally from documented steps.

The UI should not start with "try a prediction." It should start with "here is the completed project and what it demonstrates."

## 12. Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| Product creep | A polished app can imply SaaS/dashboard scope. | Label it clearly as an optional portfolio showcase. Avoid product affordances. |
| Betting misinterpretation | Football prediction can be mistaken for odds or gambling. | Never show odds, stake language, betting terms, or live prediction controls. |
| Overclaiming | A premium UI could make modest results look stronger than they are. | Keep draw-class weakness and modest improvement in the main story. |
| Reproducibility drift | App may depend on local ignored files. | Show missing-artifact guidance and point to the reproduction guide. |
| Schema fragility | CSV or Markdown structure may change. | Keep parsers small and tied to named v1 output files. |
| Maintenance overhead | UI polish can consume time after v1 completion. | Limit to a small local app; stop before deployment, accounts, or APIs. |
| Spec tension | v1 specs excluded shipping a frontend app. | Treat the showcase as post-v1 optional enhancement, not v1 completion work. Do not modify specs silently. |

## 13. Out-of-Scope

The showcase must not include:

- live predictions;
- user accounts;
- APIs;
- databases;
- cloud deployment;
- SaaS functionality;
- betting functionality;
- odds or bookmaker data;
- model retraining;
- new ML work;
- new metrics beyond approved outputs;
- new data acquisition;
- external live data feeds;
- authentication;
- payment flows;
- admin panels;
- production monitoring;
- MLOps infrastructure;
- dashboard-product positioning.

It should also not modify:

- existing specs;
- README;
- evidence files;
- reproduction guide;
- model scripts;
- evaluation scripts;
- generated v1 claims.

## 14. Success Criteria

The showcase is successful if:

- It can be run locally after the documented reproduction workflow regenerates artifacts.
- It clearly communicates that StatSport v1 is already complete.
- It follows the full story from problem through reproducibility.
- It shows baseline and Logistic Regression results with correct values from existing outputs.
- It highlights draw-class weakness clearly.
- It presents global and local explainability in plain language.
- It avoids live prediction, betting, SaaS, dashboard, API, and deployment framing.
- It uses the provided visual inspiration while remaining readable and credible.
- It adds portfolio value without creating significant maintenance burden.
- A reviewer can understand the project's purpose, method, result, limitation, and reproducibility path within a few minutes.

The showcase is not successful if:

- It implies StatSport is a product.
- It hides limitations.
- It requires cloud services or deployment to be useful.
- It recalculates or changes modelling results.
- It expands project scope beyond a small presentation layer.

## 15. Recommended Implementation Sequence

This sequence is only for a future approved implementation. Do not implement it as part of this planning task.

### Task 1: Confirm Showcase Boundary

**Files:**

- Read: `AGENTS.md`
- Read: `docs/specs/PROJECT_OVERVIEW.md`
- Read: `docs/specs/PORTFOLIO_HANDOFF_SPEC.md`
- Read: `docs/reviews/STATSPORT_COMPLETION_REVIEW_v1.md`
- Do not modify specs.

- [ ] Confirm the UI is post-v1 and optional.
- [ ] Confirm no product, betting, live prediction, dashboard, API, or deployment scope is being added.
- [ ] Confirm generated `data/` and `outputs/` files are local and ignored by git.

Acceptance criteria:

- The implementation notes state that v1 remains complete without the showcase.
- No spec changes are made.

### Task 2: Add Minimal Streamlit Entry Point

**Files:**

- Create only if implementation is approved: a small Streamlit entry point under an agreed location.
- Modify dependency documentation only if the owner approves dependency changes.

- [ ] Add a local Streamlit app shell with dark theme support.
- [ ] Add missing-artifact detection for all required runtime sources.
- [ ] Display a clear reproduction-guide message if artifacts are missing.

Acceptance criteria:

- Running the app without generated outputs does not crash.
- Running the app with generated outputs loads the story shell.

### Task 3: Build The Narrative Sections

**Files:**

- Use required runtime sources listed in section 7.

- [ ] Implement Hero and project status.
- [ ] Implement Problem and overview.
- [ ] Implement Dataset and feature pipeline.
- [ ] Implement Baseline versus selected model.
- [ ] Implement Evaluation and walk-forward sections.
- [ ] Implement Confusion matrix and draw limitation.
- [ ] Implement Global feature influence.
- [ ] Implement Prediction explanation cards.
- [ ] Implement Limitations.
- [ ] Implement Reproducibility and repository structure.

Acceptance criteria:

- The app tells the story in the required order.
- All displayed numbers match existing generated outputs.
- Limitations are visible without extra interaction.

### Task 4: Apply Visual Polish Conservatively

**Files:**

- Use: `assets/STATSPORT_AI_POWERED_FOOTBALL_ANALYTICS_AND_PREDICTION_SHOWCASE.png`
- Add styling only if it remains small and maintainable.

- [ ] Apply dark visual direction.
- [ ] Use consistent Home / Draw / Away colors.
- [ ] Make metric cards readable at desktop and laptop widths.
- [ ] Keep cards flat, compact, and non-product-like.

Acceptance criteria:

- The UI feels premium and readable.
- The design does not resemble a betting interface or SaaS dashboard.

### Task 5: Validate Locally

**Files:**

- Use existing scripts and generated outputs only.

- [ ] Run the documented reproduction workflow if outputs are missing.
- [ ] Start the Streamlit app locally.
- [ ] Check every section for incorrect values, missing files, or overstated claims.
- [ ] Check macOS and Windows 11 instructions if dependency documentation changes.

Acceptance criteria:

- The app starts locally.
- All required sections render.
- No new data, model, API, database, account, deployment, or training workflow exists.
- Repository status shows only the intentionally approved UI files.

## Final Recommendation

RECOMMENDED
