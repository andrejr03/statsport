# StatSport — Explainability Strategy Analysis

**Research / decision-support document**

> _A structured comparison of realistic explainability approaches — global methods, local methods,
> portfolio artifacts, and fallback options — against the StatSport specifications, to inform but not
> make the final explainability decision._

| | |
|---|---|
| **Status** | Research — for review |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Research artifact (informs `EXPLAINABILITY_SPEC.md`; conforms to all existing specifications) |
| **Parents** | [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) · [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) · [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) · [`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md) · [`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md) · [`PORTFOLIO_HANDOFF_SPEC.md`](../specs/PORTFOLIO_HANDOFF_SPEC.md) · [`AGENTS.md`](../../AGENTS.md) |
| **Related** | [`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md) · [`PREDICTION_TARGET_ANALYSIS.md`](./PREDICTION_TARGET_ANALYSIS.md) · [`FEATURE_ENGINEERING_ANALYSIS.md`](./FEATURE_ENGINEERING_ANALYSIS.md) · [`MODEL_CANDIDATE_ANALYSIS.md`](./MODEL_CANDIDATE_ANALYSIS.md) · [`EVALUATION_STRATEGY_ANALYSIS.md`](./EVALUATION_STRATEGY_ANALYSIS.md) |

> **What this document is:** an explainability-strategy analysis performed *before* the final
> explainability decision. It identifies realistic global and local explanation approaches for the
> approved dataset, target, feature strategy, model, and evaluation strategy; scores each against the
> StatSport specifications; and produces explicit recommendations for a **global explanation
> strategy**, a **local explanation strategy**, **portfolio explainability artifacts**, and a
> **fallback explainability strategy**. **It does not change any specification** — final
> explainability methods, tooling, visualizations, workflow, and presentation format remain decisions
> owned by [`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md) (§14), and the choice is the
> human's to make. This document is **decision-support only**: it modifies no spec, writes no code,
> creates no datasets/notebooks/scripts, and commits to no implementation.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total; one of three summer
> portfolio repositories.
>
> **Governing rule of thumb (from `EXPLAINABILITY_SPEC.md`):** explainability is first-class, but the
> best explanation is the clearest sufficient one. This analysis prioritizes **native
> interpretability, simplicity, reviewer comprehension, and reproducibility** over explainability
> tooling complexity, research-grade XAI, and novel methods.

---

## 1. Context and Scope

The project decisions relevant to explainability are approved:

- **Source / league / seasons:** Football-Data.co.uk · Bundesliga · 2020/21–2024/25.
- **Prediction target:** Home / Draw / Away (1X2), three-class classification of the full-time result.
- **Fallback target:** Home Win vs Not Home Win, binary classification.
- **Core features:** home advantage, recent form, goals scored, goals conceded, goal difference.
- **Optional features:** shots on target, league position, Elo-style rating.
- **Excluded features:** corners, cards, strength-of-schedule features, bookmaker odds, xG,
  possession, player-level features.
- **Baseline:** home-advantage baseline.
- **Selected model:** multinomial logistic regression.
- **Fallback model:** random forest.
- **Evaluation strategy:** chronological hold-out, season-blocked walk-forward validation, approved
  metric set.

The next major decision is the **explainability strategy**: how StatSport explains overall model
behaviour, individual predictions, portfolio-facing artifacts, and fallback behaviour if the selected
model or multiclass target proves too weak.

**Out of scope (by constraint):** modifying any spec, writing code, creating datasets/notebooks/scripts,
or committing to implementation. Selecting the explainability strategy is the next step (§9).

### 1.1 What the approved decisions imply for explainability

- **The selected model is already interpretable.** Multinomial logistic regression has native global
  explanations through coefficients and native local explanations through feature contributions to
  class log-odds. This reduces the need for SHAP, LIME, or other model-agnostic tooling.
- **The feature set is intentionally plain-language.** Home advantage, recent form, goals scored,
  goals conceded, goal difference, shots on target, league position, and Elo-style rating all map to
  football concepts a reviewer can understand.
- **The target is multiclass.** Explanations must address why the model leans toward home, draw, or
  away, and must not let the draw class disappear.
- **The evaluation strategy is temporal and baseline-first.** Explanations should describe the
  evaluated model trained under the approved chronological procedure, and claims should stay consistent
  with baseline-relative results.
- **The portfolio audience is non-specialist.** The artifact should help a reviewer answer "why did
  the model predict this?" without needing XAI background.
- **The project budget is tight.** Explainability should be finished and understandable, not expanded
  into a separate research project.

**Consequence:** the strongest strategy is likely a native logistic-regression explanation package:
standardized global coefficients, odds-ratio/plain-language interpretation where helpful, and local
coefficient contribution examples, supported by a small set of reproducible tables/figures.

---

## 2. Method

### 2.1 Scoring rubric

Each candidate is scored **1 (poor) – 5 (excellent)** on ten criteria. Weights encode the inherited
priority order, the explainability spec's reader-first mandate, and the repository constitution's
finishability constraint. The **Fit Score /100** is the weighted average rescaled:
`Fit = sum(score * weight) / sum(weight) * 20`, with `sum(weight) = 42`.

| # | Criterion | Weight | What a 5 looks like |
|---|-----------|:------:|---------------------|
| 1 | Explainability quality | 5 | Clearly shows model behaviour or prediction reasoning without distortion |
| 2 | Reviewer comprehension | 5 | Understandable to a technically literate non-specialist |
| 3 | Portfolio value | 5 | Demonstrates sound ML judgment and communication |
| 4 | Reproducibility | 5 | Deterministic, traceable, and easy to regenerate |
| 5 | Simplicity | 4 | Minimal moving parts and little extra tooling |
| 6 | Alignment with logistic regression | 4 | Uses or respects the selected model's native structure |
| 7 | Alignment with approved feature set | 4 | Works naturally with the project's interpretable football features |
| 8 | Fit for a 40–60 hour project | 4 | Cheap enough to finish without crowding out evaluation/presentation |
| 9 | Long-term maintainability | 3 | Easy for future André or a reviewer to understand and update |
| 10 | Implementation effort | 3 | Low effort, few dependencies, low failure surface |

> **Note on criterion 10.** The brief lists "implementation effort"; it is scored as **implementation
> ease** (5 = easiest) so higher scores consistently mean better fit.

> **Caveat:** fit scores are structured judgment, not measurement. The ranking and recommendations are
> the point.

### 2.2 Summary rankings

| Candidate | Scope | Fit score |
|-----------|-------|:---------:|
| Standardized coefficient analysis | Global | 95 |
| Coefficient contribution analysis | Local | 93 |
| Logistic regression coefficients | Global | 91 |
| Feature-difference explanation | Local | 90 |
| Global feature ranking | Global | 88 |
| Example-based explanation | Local | 86 |
| Odds-ratio interpretation | Global | 84 |
| Probability decomposition | Local | 80 |
| Permutation feature importance | Global | 78 |
| Partial dependence / ICE-lite | Global | 70 |
| Random Forest feature importance | Global / fallback | 66 |
| SHAP | Local / global | 60 |
| LIME | Local | 54 |

---

## 3. Global Explainability Comparison

### 3.1 Logistic regression coefficients

**Description.** Report the fitted multinomial logistic regression coefficients for each class,
connecting positive/negative coefficient direction to higher or lower class tendency.

**Pros.** Native to the selected model, deterministic, transparent, and dependency-light. Shows the
actual learned model rather than an approximation. Strongly aligned with `MODELING_SPEC.md` and
`EXPLAINABILITY_SPEC.md`.

**Cons.** Raw coefficient magnitudes are hard to compare when features are on different scales. The
multiclass setup can be confusing unless explained carefully.

**Risks.** Reviewers may overread coefficients as causal effects. Unstandardized coefficients can make
small-scale features look artificially large.

**Implementation effort.** **Low** — extract model coefficients and map them to feature names/classes.

**Reviewer suitability.** **Strong** if accompanied by plain-language labels and a short explanation of
direction and scale.

**Portfolio suitability.** **Excellent** — demonstrates that the selected model was chosen partly
because it can be explained directly.

**Fit score: 91 / 100.**

### 3.2 Standardized coefficient analysis

**Description.** Standardize numeric features during modelling or explanation, then rank coefficients
by comparable magnitude for each class and explain direction in plain language.

**Pros.** Keeps the explanation native to logistic regression while making feature influence more
comparable. Helps answer "which features matter most?" without adding model-agnostic tooling. Fits the
approved small, interpretable feature set.

**Cons.** Requires explaining that standardized coefficients are not in the original units. If feature
scaling is not already part of the modelling pipeline, the workflow must document it carefully.

**Risks.** A reviewer may treat standardized magnitude as exact importance rather than approximate
influence. Correlated features such as recent form and goal difference can share signal, so rankings
must be interpreted cautiously.

**Implementation effort.** **Low** — use the same deterministic preprocessing as modelling and report
class-specific standardized coefficients.

**Reviewer suitability.** **Excellent** — a compact ranking with plain-language labels is easy to read.

**Portfolio suitability.** **Excellent** — shows ML maturity without overengineering.

**Fit score: 95 / 100.**

### 3.3 Odds-ratio interpretation

**Description.** Convert selected logistic regression coefficients into odds ratios to explain how a
feature changes the relative odds of one outcome versus another.

**Pros.** Mathematically faithful to logistic regression and useful for a few headline effects, such as
home advantage increasing the tendency toward home win. Can make coefficients more concrete.

**Cons.** Odds ratios are less intuitive than they appear, especially in multinomial classification.
They require careful wording and can distract non-expert readers.

**Risks.** High risk of overclaiming if phrased as causal or exact. Too many odds ratios would make the
presentation technical and less reader-first.

**Implementation effort.** **Low** — exponentiate selected coefficients after confirming the reference
class interpretation.

**Reviewer suitability.** **Moderate to strong** when limited to a few examples; weak if used as the
main explanation.

**Portfolio suitability.** **Strong** as a supporting artifact, not the centerpiece.

**Fit score: 84 / 100.**

### 3.4 Permutation feature importance

**Description.** Measure how much validation or test performance changes when each feature is shuffled,
using the approved evaluation metric(s).

**Pros.** Model-agnostic, intuitive in principle, and tied to predictive performance. Useful as a
sanity check against coefficient-based interpretation.

**Cons.** More computation and more methodological choices: dataset, metric, repeat count, random seed,
and handling correlated features. Can be unstable on a small five-season dataset.

**Risks.** Correlated football features can make importance look lower than expected because related
features substitute for one another. Results may vary unless randomness and repeats are controlled.

**Implementation effort.** **Medium** — requires deterministic shuffling, repeated estimates, and a
clear reporting rule.

**Reviewer suitability.** **Strong** if summarized simply, but less direct than native coefficients.

**Portfolio suitability.** **Moderate to strong** as an optional cross-check; too much emphasis risks
turning explainability into a tooling exercise.

**Fit score: 78 / 100.**

### 3.5 Random Forest feature importance

**Description.** If the fallback random forest is used, report tree-based feature importance, ideally
with permutation importance preferred over impurity-based importance.

**Pros.** Gives a fallback route if logistic regression underperforms and the project needs to explain
a random forest. Familiar and easy to visualize.

**Cons.** It explains the fallback model, not the selected model. Impurity-based importance can be
biased and less stable; random forests are less transparent than logistic regression.

**Risks.** Could weaken the project's explainability narrative if presented as equivalent to native
logistic regression interpretation. May require explaining random forest mechanics.

**Implementation effort.** **Low to medium** — easy to compute, but needs careful interpretation and
fixed random state.

**Reviewer suitability.** **Moderate** — understandable as a ranking, weaker as a behavioural
explanation.

**Portfolio suitability.** **Moderate** for fallback; poor as the primary strategy while logistic
regression remains selected.

**Fit score: 66 / 100.**

### 3.6 Global feature ranking

**Description.** Produce a single reader-facing ranking of feature groups based primarily on
standardized coefficients, optionally checked against permutation importance.

**Pros.** Very reviewer-friendly. Turns model internals into a compact story: which football concepts
matter most overall and for each outcome. Aligns with portfolio handoff needs.

**Cons.** A single ranking can oversimplify class-specific behaviour. It can hide that features may
push toward home, draw, and away differently.

**Risks.** The ranking may be mistaken for causal truth or exact importance. Needs caveats about
correlation and uncertainty.

**Implementation effort.** **Low** — aggregate and label the native coefficient outputs.

**Reviewer suitability.** **Excellent** — likely one of the easiest artifacts for a reviewer to scan.

**Portfolio suitability.** **Excellent** as a README/report figure or table.

**Fit score: 88 / 100.**

### 3.7 Partial dependence / ICE-lite

**Description.** Show how predicted probabilities change as one feature varies while other features
are held fixed or averaged.

**Pros.** Can be visually intuitive for one or two features, such as home advantage or goal difference.
Shows probability movement rather than only coefficient direction.

**Cons.** More artificial than coefficient interpretation, because it changes features in isolation.
With correlated rolling features, unrealistic combinations are possible.

**Risks.** Reviewers may read synthetic curves as observed football patterns. The method adds more
explanation machinery than the project likely needs.

**Implementation effort.** **Medium** — needs controlled grids, prediction calls, and careful captions.

**Reviewer suitability.** **Moderate** — useful visually, but not necessary for the selected model.

**Portfolio suitability.** **Moderate** as optional future polish; not required for a finished project.

**Fit score: 70 / 100.**

---

## 4. Local Explainability Comparison

### 4.1 Coefficient contribution analysis

**Description.** For a selected match, multiply each standardized feature value by its class-specific
coefficient to show which features pushed the prediction toward home, draw, or away.

**Pros.** Native to logistic regression, deterministic, and directly connected to the model's predicted
probabilities. Produces a clear per-prediction explanation without SHAP/LIME. Works well with the
approved feature set because each feature has plain football meaning.

**Cons.** Contributions operate on log-odds, which are not immediately intuitive. The final multiclass
probability still needs a short plain-language bridge.

**Risks.** Overly numerical presentation could lose readers. Contributions should be summarized as
"main factors pushing toward/away from the prediction," not as causal statements.

**Implementation effort.** **Low** — use model coefficients, transformed feature values, and class
labels already available from the modelling pipeline.

**Reviewer suitability.** **Excellent** if displayed as a small ranked table with natural-language
sentence output.

**Portfolio suitability.** **Excellent** — directly answers "why this prediction?".

**Fit score: 93 / 100.**

### 4.2 Probability decomposition

**Description.** Explain how the model moves from baseline-like class probabilities to final predicted
probabilities, using simplified intermediate steps or grouped feature contributions.

**Pros.** Speaks in probabilities, which are easier for readers than log-odds. Connects naturally to
Log Loss, calibration, and uncertainty.

**Cons.** Exact probability decomposition for multinomial logistic regression is not additive in the
same intuitive way as log-odds contributions. Any simplified decomposition needs careful caveats.

**Risks.** A step-by-step probability story can become technically misleading if it implies an order of
feature application that the model does not actually use.

**Implementation effort.** **Medium** — possible with grouped scenarios, but harder to make exact and
simple.

**Reviewer suitability.** **Strong** as a narrative supplement; weaker as the primary local method.

**Portfolio suitability.** **Strong** if limited to concise uncertainty language.

**Fit score: 80 / 100.**

### 4.3 Example-based explanation

**Description.** Select a few representative matches and explain the prediction using the model's top
feature drivers plus the actual outcome and evaluation context.

**Pros.** Very reader-friendly. Makes the project concrete and supports portfolio storytelling. Can
show a correct home prediction, a hard draw, and an error or low-confidence case to demonstrate honest
limitations.

**Cons.** Examples can be cherry-picked unless selection rules are documented. It is not a complete
explanation method by itself.

**Risks.** Picking only successful examples would conflict with the honesty requirement. Examples
should include limitations and at least one difficult/incorrect case.

**Implementation effort.** **Low** — choose examples from the approved test set using documented
criteria.

**Reviewer suitability.** **Excellent** — concrete examples are easier to understand than abstract
model internals.

**Portfolio suitability.** **Excellent** as a report/README artifact, paired with coefficient
contributions.

**Fit score: 86 / 100.**

### 4.4 Feature-difference explanation

**Description.** Explain a match by comparing the two teams on interpretable pre-match feature values:
home advantage, recent form, goals for/against, goal difference, and optional features.

**Pros.** Highly intuitive for football readers. It grounds the model explanation in visible match
context and helps translate coefficients into a plain-language story.

**Cons.** It explains the input context more than the model mechanics. On its own, it may not show how
the model weighted each feature.

**Risks.** Could drift into informal punditry if not tied back to model coefficients and predicted
probabilities.

**Implementation effort.** **Low** — uses already generated feature values and simple differences.

**Reviewer suitability.** **Excellent** — probably the easiest local artifact for non-specialists.

**Portfolio suitability.** **Excellent** when paired with contribution analysis.

**Fit score: 90 / 100.**

### 4.5 SHAP

**Description.** Use SHAP values to attribute prediction output to features globally or locally.

**Pros.** Recognizable XAI method and powerful for complex models. Can produce polished plots.

**Cons.** Logistic regression already has native additive structure, so SHAP is usually unnecessary
here. It adds dependencies, background-data choices, runtime considerations, and conceptual overhead.
For a multiclass model, SHAP outputs can be harder to explain than coefficients.

**Risks.** Tooling complexity can crowd out the project's actual goal: explaining a simple,
interpretable model clearly. SHAP may impress superficially while reducing reviewer comprehension.

**Implementation effort.** **Medium to high** — dependency management, explainer choice, background
sample, multiclass output handling, and plotting decisions.

**Reviewer suitability.** **Mixed** — familiar to ML reviewers, often opaque to non-specialists.

**Portfolio suitability.** **Moderate** — useful for complex models, but likely unnecessary and
misaligned with the project's simplicity mandate.

**Fit score: 60 / 100.**

### 4.6 LIME

**Description.** Use LIME to approximate the model locally around a prediction and report feature
weights for that local surrogate model.

**Pros.** Designed for local explanations and can explain many model types. Useful when the underlying
model is opaque.

**Cons.** Logistic regression is already transparent, so a local surrogate is redundant. LIME adds
sampling randomness, kernel/neighbourhood settings, and another model that may be less faithful than
the original coefficients.

**Risks.** Lower reproducibility unless seeds and settings are fixed. A surrogate explanation for an
already interpretable model can look like complexity for its own sake.

**Implementation effort.** **Medium to high** — dependency, sampling, configuration, and stability
checks.

**Reviewer suitability.** **Mixed to weak** for this project: the method itself requires explanation
before the prediction can be explained.

**Portfolio suitability.** **Weak to moderate** — not the right signal for a small, interpretable
portfolio project.

**Fit score: 54 / 100.**

### 4.7 Nearest-neighbour precedent explanation

**Description.** For a prediction, show one or two historically similar matches from the training data
based on approved feature values, and use them as contextual precedents.

**Pros.** Intuitive and football-friendly. Helps readers understand whether a prediction resembles
past cases.

**Cons.** It is not a native explanation of logistic regression. Similarity metrics introduce design
choices and can become a separate mini-project.

**Risks.** Cherry-picked precedents can mislead. Similar matches may not be truly comparable unless the
distance metric is documented.

**Implementation effort.** **Medium** — choose scaled features, distance metric, and selection rules.

**Reviewer suitability.** **Strong** as optional narrative support; not enough as the main method.

**Portfolio suitability.** **Moderate** — potentially engaging, but likely unnecessary for completion.

**Fit score: 72 / 100.**

---

## 5. Why Logistic Regression Does Not Need SHAP or LIME by Default

SHAP and LIME are most valuable when the model is hard to inspect directly. StatSport's selected model
is the opposite: multinomial logistic regression is deliberately chosen because its behaviour can be
read through coefficients and feature contributions. Adding SHAP or LIME would introduce extra
dependencies, extra assumptions, and extra explanation burden before improving the reader's
understanding.

For this project, the question is not "can we use a modern XAI tool?" It is "can a reviewer understand
why the model predicted home, draw, or away?" Native coefficients, standardized feature rankings, and
local contribution tables answer that question more directly. Simpler approaches better satisfy
[`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md), [`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md),
[`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md), and [`AGENTS.md`](../../AGENTS.md)
because they are easier to explain, easier to regenerate, and less likely to expand the project into a
research-grade XAI exercise.

SHAP remains reasonable only if the fallback random forest becomes the selected model and native
random-forest explanations prove insufficient. LIME is lower priority even then because its local
surrogate randomness and configuration choices are harder to justify in a small reproducible portfolio
project.

---

## 6. Recommended Global Explainability

**Recommended Global Explainability:** **standardized logistic regression coefficient analysis,
summarized as class-specific feature rankings, with optional odds-ratio examples for a few headline
effects.**

This strategy should include:

- A global table or figure ranking standardized coefficients by class: Home, Draw, Away.
- Plain-language labels for each approved feature group.
- A short explanation of direction: which features push probability toward or away from each class.
- A caveat that coefficients describe model associations, not causal football truths.
- Optional odds-ratio examples only where they clarify an intuitive point, such as home advantage.

This is the strongest fit because it is native to the selected model, deterministic, easy to reproduce,
and understandable without extra XAI tooling. It also supports draw-class visibility by showing whether
the model has meaningful draw-related signals or mostly struggles there.

Permutation feature importance should be treated as an optional sanity check, not the main global
strategy. Random Forest importance should be reserved for fallback use only.

---

## 7. Recommended Local Explainability

**Recommended Local Explainability:** **coefficient contribution analysis for selected predictions,
paired with feature-difference explanations and concise probability/uncertainty language.**

This strategy should include:

- For each showcased prediction, the predicted probabilities for Home / Draw / Away.
- A small ranked list of the strongest feature contributions toward the predicted class.
- A plain-language team comparison using approved feature values.
- A brief uncertainty statement, especially when probabilities are close or the draw class is
  plausible.
- The actual result when reporting retrospective test-set examples, framed honestly.

The local explanation should avoid burying readers in log-odds. The underlying method can use log-odds
contributions, but the portfolio artifact should translate them into statements such as: "recent form
and goal difference pushed the model toward home win, while defensive weakness kept confidence
moderate."

Example-based explanations should be used as the delivery format: at least one confident correct
prediction, one draw or draw-adjacent case, and one error or low-confidence case. This makes
limitations visible and aligns with the honesty requirements in `EVALUATION_SPEC.md` and
`PORTFOLIO_HANDOFF_SPEC.md`.

---

## 8. Recommended Portfolio Explainability Artifacts

**Recommended Portfolio Explainability Artifacts:**

1. **Global feature influence table/figure.** Class-specific standardized coefficient ranking for
   Home / Draw / Away, with feature labels and one-sentence interpretation.
2. **Model behaviour summary.** A short reader-facing paragraph explaining what the model generally
   learned, including whether draw predictions are weak or uncertain.
3. **Local prediction explanation cards.** Three compact examples from the chronological hold-out test
   season: a correct confident case, a draw/hard case, and an error or low-confidence case.
4. **Feature context table for each example.** Home/away team values for recent form, goals scored,
   goals conceded, goal difference, and any included optional features.
5. **Limitations note.** A visible explanation of uncertainty, non-causality, small data, class
   imbalance, and draw difficulty.
6. **Fallback appendix or note.** If random forest is used, include permutation feature importance and
   a brief statement that explanations are less direct than logistic regression.

These artifacts satisfy the portfolio handoff requirement for a coherent story from methodology to
results to interpretation. They are also small enough to regenerate from the modelling and evaluation
workflow without creating a dashboard, deployment, or research-grade explainability subsystem.

---

## 9. Recommended Fallback Explainability

**Recommended Fallback Explainability:** if multinomial logistic regression is not sufficient and the
random forest fallback is used, explain it with **permutation feature importance plus example-based
local explanations**, while clearly stating that the fallback is less transparent than logistic
regression.

Fallback global explanation:

- Use permutation feature importance on the approved validation/test procedure.
- Prefer permutation importance over impurity-based random forest importance because it is easier to
  connect to evaluated performance and less tied to tree internals.
- Fix random seeds and repeat counts so the result is reproducible.
- Report feature groups, not an overwhelming list of engineered columns.

Fallback local explanation:

- Use feature-difference and example-based explanation as the main reader-facing method.
- Avoid SHAP unless random forest becomes the final selected model and the simpler fallback artifacts
  cannot explain individual predictions adequately.
- Avoid LIME by default because it adds local surrogate complexity and reproducibility burden.

Fallback rationale:

The fallback strategy preserves portfolio honesty: it acknowledges that random forest may improve
performance but costs interpretability. It still gives reviewers a feature-level explanation and
concrete examples, but it does not pretend the fallback is as naturally explainable as logistic
regression.

---

## 10. Rationale Against the Specifications

### 10.1 `PROJECT_OVERVIEW.md`

The recommended strategy supports the project's purpose: explainable analytics and defensible match
predictions, not a product or research programme. It is small, finished, and reviewer-facing. It avoids
dashboards, services, hosted explainability tools, and broad XAI exploration.

### 10.2 `MODELING_SPEC.md`

The selected model is multinomial logistic regression, so explanations should use the model's native
structure first. Standardized coefficients and local contributions are the most direct way to explain
an interpretable model. Random forest explanations are reserved for fallback use because the fallback
model is less transparent.

### 10.3 `EVALUATION_SPEC.md`

The strategy connects explanations to evaluated predictions from chronological hold-out and
season-blocked validation. Example cards should include uncertainty, errors, and draw-class difficulty
so explanations do not overclaim performance. Local explanations should be tied to predicted
probabilities and baseline-relative results.

### 10.4 `EXPLAINABILITY_SPEC.md`

The recommendation satisfies both global and local explanation requirements. It is reader-first,
plain-language, and accessible. It avoids unnecessary mathematical complexity in the presentation while
preserving a faithful underlying method.

### 10.5 `REPRODUCIBILITY_SPEC.md`

The explanation outputs are deterministic and regenerable from model coefficients, transformed feature
values, prediction probabilities, and documented test examples. No hidden manual judgement is required
if example-selection rules are recorded.

### 10.6 `PORTFOLIO_HANDOFF_SPEC.md`

The artifacts create a coherent portfolio story: what the model learned globally, why specific
predictions happened locally, where it struggled, and how much confidence the reader should place in
the results. This directly supports README/report communication.

### 10.7 `AGENTS.md`

The recommendation follows the repository constitution: finished over ambitious, explainable over
complex, reproducible over clever, honest over impressive, and simplicity over infrastructure. It does
not add data, code, notebooks, dependencies, services, or tooling.

---

## 11. Final Recommendations

### Recommended Global Explainability

Use **standardized logistic regression coefficient analysis** as the primary global explanation,
presented as class-specific feature rankings for Home / Draw / Away. Include raw coefficient direction
where useful and only a few odds-ratio examples if they improve reader understanding.

### Recommended Local Explainability

Use **coefficient contribution analysis** for individual predictions, translated into plain-language
explanation cards and paired with feature-difference context. Include predicted probabilities and
uncertainty language.

### Recommended Portfolio Explainability Artifacts

Create a small, reproducible set of reader-facing artifacts:

- Global class-specific feature influence table/figure.
- Plain-language model behaviour summary.
- Three local prediction explanation cards from the 2024/25 hold-out season.
- Feature context tables for the showcased matches.
- Limitations and uncertainty note.
- Fallback explainability note only if the fallback model is used.

### Recommended Fallback Explainability

If random forest becomes necessary, use **permutation feature importance** for global explanation and
**example-based feature-difference explanations** for local explanation. Treat SHAP as optional future
work only if simpler fallback explanations are inadequate; avoid LIME by default.

### Overall recommendation

Select the native logistic-regression explanation strategy. It is the best match for StatSport's
approved model, approved feature set, reproducibility requirements, reviewer-first communication goals,
and 40–60 hour budget. SHAP and LIME are not recommended for the default path because they solve a
problem the selected model deliberately avoids: opaque model behaviour.

---

## 12. Next Step

Review this analysis and choose the final explainability strategy to record in
[`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md). The likely approval package is:

- Global: standardized logistic regression coefficient analysis.
- Local: coefficient contribution analysis plus feature-difference examples.
- Artifacts: global influence table/figure, three local explanation cards, and limitations note.
- Fallback: permutation feature importance plus example-based explanation for random forest.
