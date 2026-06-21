# StatSport — Model Candidate Analysis

**Research / decision-support document**

> _A structured comparison of realistic classical model candidates against the StatSport specifications — to inform, but not to make, the final modelling decision._

| | |
|---|---|
| **Status** | Research — for review |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Research artifact (informs `MODELING_SPEC.md` / `EVALUATION_SPEC.md`; conforms to all existing specifications) |
| **Parents** | [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](../specs/DATA_SPEC.md) · [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) · [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) · [`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md) · [`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md) · [`PORTFOLIO_HANDOFF_SPEC.md`](../specs/PORTFOLIO_HANDOFF_SPEC.md) · [`AGENTS.md`](../../AGENTS.md) |
| **Related** | [`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md) · [`PREDICTION_TARGET_ANALYSIS.md`](./PREDICTION_TARGET_ANALYSIS.md) · [`FEATURE_ENGINEERING_ANALYSIS.md`](./FEATURE_ENGINEERING_ANALYSIS.md) |

> **What this document is:** a model-candidate analysis performed *before* the modelling decision. It
> identifies realistic classical model candidates appropriate for the approved target and feature
> strategy, scores each against the StatSport specifications, and produces a ranked recommendation with
> an explicit **baseline**, **selected model**, and **fallback model**. **It does not select the final
> algorithm** — that decision is owned by [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) (its "Final
> algorithm" remains a deferred decision) and is the human's to make. This document is **decision-support
> only**: it changes no specification, selects no metrics, and commits to no implementation.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total; one of three summer
> portfolio repositories.

---

## 1. Context and Scope

The dataset, prediction-target, and feature-strategy decisions are approved (see the related research
documents and the corresponding decisions in [`DATA_SPEC.md`](../specs/DATA_SPEC.md) and
[`MODELING_SPEC.md`](../specs/MODELING_SPEC.md)):

- **Source / league / seasons:** Football-Data.co.uk · Bundesliga · 2020/21–2024/25 (five seasons)
- **Prediction target:** Home / Draw / Away (1X2), three-class classification
- **Fallback target:** Home Win vs Not Home Win, binary classification
- **Core features:** home advantage, recent form, goals scored, goals conceded, goal difference
- **Optional features:** shots on target, league position, Elo-style rating

The next major decision is **model selection** — which algorithm serves as the baseline, the selected
model, and a fallback. The final algorithm is a deferred decision in
[`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) §6/§16. This document evaluates the candidates so the
eventual choice is defensible, documented, and traceable.

**Out of scope (by constraint):** modifying any spec, selecting final metrics, writing code, creating
datasets/notebooks/scripts, or committing to implementation. Selecting the modelling strategy is the
**next** step (§9).

### 1.1 What the approved decisions imply for model choice

- **A small, tabular, interpretable feature set.** A handful of engineered numeric features over ~1,530
  matches (five seasons × 306 fixtures) is **small-to-medium tabular data**. This rewards classical
  models and penalizes anything data-hungry or high-variance.
- **A three-class target with a hard draw class.** The model must produce sensible **multiclass**
  predictions (ideally calibrated probabilities) for home/draw/away, knowing draws (~1 in 4) are
  intrinsically hard (`EVALUATION_SPEC.md`).
- **Interpretability is a first-class constraint, not a preference.** `MODELING_SPEC.md` §5–§8 and
  `EXPLAINABILITY_SPEC.md` require classical, interpretable families and reader-facing explanations;
  §7 and `AGENTS.md` §10 **exclude** deep learning, large neural nets, foundation models, LLMs, and
  GPU-dependent workflows.
- **Baseline-first is mandatory.** `MODELING_SPEC.md` §4 requires a simple, transparent baseline that
  every other model is measured against; the named reference is a **home-advantage / majority-class
  prior**.
- **Finishability governs.** `MODELING_SPEC.md` §12 forbids model zoos, large hyperparameter searches,
  AutoML, and elaborate ensembles. The whole modelling effort is a fraction of 40–60 hours.

**Consequence:** all candidates here are **classical and laptop-friendly**, and differentiation comes
mostly from **explainability, portfolio value, fit to the target/features, and finishability** — not
from raw predictive ceiling, which the project deliberately does not prize.

> **No metrics are selected here.** "Evaluation clarity" below judges how *cleanly a model's outputs
> support honest evaluation* (e.g. interpretable probabilities), not which metrics will be used — metric
> selection remains deferred to [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §4/§14.

---

## 2. Method

### 2.1 Scoring rubric

Each candidate is scored **1 (poor) – 5 (excellent)** on the ten evaluation criteria. Weights encode the
inherited priority order (portfolio value → reproducibility → explainability → evaluation quality →
presentation clarity) and the finishability mandate. The **Fit Score /100** is the weighted average
rescaled: `Fit = Σ(score × weight) ÷ Σ(weight) × 20`, with `Σ(weight) = 39`.

| # | Criterion | Weight | What a 5 looks like |
|---|-----------|:------:|---------------------|
| 1 | Explainability | 5 | Inherently interpretable; drivers map to plain-language football intuition |
| 2 | Portfolio value | 5 | A recognizable, credible modelling choice a reviewer respects |
| 3 | Reproducibility | 5 | Deterministic from the same data + fixed configuration/seed |
| 4 | Reviewer comprehension | 4 | A non-expert instantly grasps how the model decides |
| 5 | Fit for Home/Draw/Away prediction | 4 | Native, well-behaved multiclass with sensible probabilities |
| 6 | Suitability for the selected feature set | 4 | Handles small, correlated, numeric engineered features well |
| 7 | Evaluation clarity | 3 | Outputs (esp. probabilities) support honest, baseline-relative evaluation |
| 8 | Implementation simplicity | 3 | Few moving parts; little tuning; low failure surface |
| 9 | Fit for a 40–60 hour project | 4 | Cheap to build and finish, leaving room for two more projects |
| 10 | Long-term maintainability | 2 | Stable, standard, unlikely to need rework |

> **Note on criterion 8.** The brief lists "implementation complexity"; it is scored here as
> **implementation simplicity** (5 = simplest) so a higher score is consistently better.

> **Note on scoring baselines.** The two baselines are scored *in their role as mandatory references*.
> They deliberately use little or none of the feature set, so they score low on "suitability for the
> selected feature set" and "portfolio value" by design — this is expected and not a defect. Their value
> is as the honest yardstick every other model must beat (`MODELING_SPEC.md` §4).

> **Caveat:** fit scores are a structured judgment encoding the inherited priorities, not a precise
> measurement. The **ranking and the baseline/selected/fallback split**, not the decimal, are the point.

---

## 3. Candidate Models

### 3.1 Majority-class baseline

**Description.** Always predict the most frequent class in the training data. For 1X2 Bundesliga this is
the home win (the plurality outcome); for the binary fallback it is the base-rate majority.

**Pros.** The textbook simplest, most honest reference. Zero tuning, fully deterministic, instantly
understood. Sets the absolute floor any real model must clear.

**Cons.** Uses no features and makes no per-match distinction; predicts one class for every match.
Ignores draws and away wins entirely, so per-class insight is trivial.

**Risks.** Essentially none — its only "risk" is being mistaken for a model rather than a yardstick.

**Expected implementation effort.** **Trivial** — a constant prediction / class-prior.

**Explainability suitability.** **Excellent** — there is nothing to explain beyond "the most common
result."

**Portfolio suitability.** **Moderate** — necessary and respected as a baseline, not a headline.

**Fit score: 87 / 100.**

---

### 3.2 Home-advantage baseline

**Description.** Encode the dominant football prior directly: predict the home team to win every match
(equivalently, predict class probabilities equal to the historical H/D/A base rates). The named
reference in `MODELING_SPEC.md` §4.

**Pros.** As simple and reproducible as majority-class, but **more football-honest and interpretable**:
it states the single best-known effect in the sport. In this target it effectively coincides with the
majority-class prediction, while the base-rate variant also yields sensible reference probabilities for
honest, baseline-relative evaluation.

**Cons.** Still feature-free and undifferentiated per match; cannot distinguish a strong home side from a
weak one. Draw/away performance is weak by construction.

**Risks.** Minimal — the main caveat is not over-claiming insight for a prior.

**Expected implementation effort.** **Trivial** — predict home / use H/D/A base rates.

**Explainability suitability.** **Excellent** — "home teams win more often" is self-explanatory and ties
the baseline to the project's home-advantage narrative.

**Portfolio suitability.** **Moderate–Strong** — a meaningful, domain-aware reference a reviewer
appreciates.

**Fit score: 89 / 100.**

---

### 3.3 Logistic Regression (multinomial)

**Description.** A linear probabilistic classifier; multinomial (softmax) for the three-class 1X2 target,
binary for the fallback. Outputs calibrated-ish class probabilities and signed coefficients per feature.

**Pros.** The canonical interpretable classifier: coefficients give **direction and rough magnitude** of
each feature's influence, mapping straight to plain-language drivers (home edge, form, goal difference).
Native multiclass with probabilistic outputs ideal for honest evaluation. Excellent fit to a small set
of correlated numeric features (with light scaling/regularization). Fully deterministic; near-zero
tuning; finishable in hours.

**Cons.** A linear decision boundary may miss strong feature interactions, so its raw predictive ceiling
can trail tree ensembles. Correlated features (goals scored/conceded/difference) need mild
regularization for stable coefficients.

**Risks.** Mild multicollinearity among the engineered features; under-fitting if relationships are
strongly non-linear — both low-severity and well-understood.

**Expected implementation effort.** **Low** — a standard fit with optional scaling/regularization.

**Explainability suitability.** **Excellent** — the gold standard for reader-first, plain-language
explanation (coefficients, odds ratios, signed contributions).

**Portfolio suitability.** **Excellent** — demonstrates sound, interpretable ML judgment; the clearest
baseline-to-model narrative.

**Fit score: 97 / 100.**

---

### 3.4 Decision Tree

**Description.** A single classification tree splitting on feature thresholds to predict H/D/A.

**Pros.** The most *visually* interpretable model — a literal flowchart a non-expert can read. Native
multiclass; no scaling needed; deterministic with a fixed seed; very cheap to build.

**Cons.** A single tree is **high-variance** and prone to overfitting on small data; small data changes
can reshape it. Probability estimates are coarse. Often underperforms both logistic regression and
ensembles on tabular data.

**Risks.** Overfitting without depth limits; instability undermines a "stable, reproducible" story if not
constrained.

**Expected implementation effort.** **Low** — a standard fit with depth/leaf constraints.

**Explainability suitability.** **Excellent** — arguably the easiest model to *show* a reviewer.

**Portfolio suitability.** **Strong** — a clear, teachable model, though weaker predictively than the
ensembles or logistic.

**Fit score: 91 / 100.**

---

### 3.5 Random Forest

**Description.** An ensemble of de-correlated decision trees (bagging + feature subsampling); predictions
by vote/averaged probabilities.

**Pros.** **Robust, low-tuning, and strong** on small tabular data; handles correlated/non-linear
features well and resists overfitting better than a single tree. Native multiclass with reasonable
probabilities. Deterministic with a fixed seed. Provides **feature-importance** summaries for global
explanation.

**Cons.** An ensemble of many trees is **not inherently interpretable** — feature importances help, but
it is a step down from logistic/tree transparency, in tension with the explainability priority. Heavier
and slower than the simpler options (still laptop-trivial here).

**Risks.** Reduced interpretability vs. priority #3; importance measures can mislead with correlated
features; mild risk of being treated as a black box.

**Expected implementation effort.** **Low–Medium** — robust defaults; little tuning required.

**Explainability suitability.** **Moderate** — global feature importance is interpretable; per-prediction
logic is not transparent without extra tooling.

**Portfolio suitability.** **Excellent** — a recognized, credible, robust ensemble; a strong predictive
safety net.

**Fit score: 87 / 100.**

---

### 3.6 Gradient Boosted Trees

**Description.** Trees built sequentially, each correcting the previous ensemble's errors
(gradient boosting).

**Pros.** Typically the **strongest predictive** classical model on tabular data; native multiclass;
deterministic with fixed seed/config.

**Cons.** **Least interpretable** of the tree models (needs post-hoc tooling like SHAP, which
`EXPLAINABILITY_SPEC.md` §12 cautions against over-investing in). **Most tuning-sensitive** (learning
rate, depth, estimators), which risks the budget and the §12 complexity boundaries, and can drift toward
accuracy-chasing the project explicitly avoids.

**Risks.** Tuning/complexity creep against `MODELING_SPEC.md` §12; opacity against the explainability
priority; over-claiming marginal accuracy gains.

**Expected implementation effort.** **Medium** — meaningful tuning and validation discipline to use well.

**Explainability suitability.** **Weak** — not inherently interpretable; reader-facing explanation needs
extra machinery.

**Portfolio suitability.** **Strong** — impressive predictively, but off-priority for *this* project's
interpretability-first framing.

**Fit score: 75 / 100.**

---

### 3.7 Extra Trees (Extremely Randomized Trees)

**Description.** An ensemble like Random Forest but with randomized split thresholds, adding variance
reduction.

**Pros.** Robust and fast; similar strengths to Random Forest; deterministic with a fixed seed; handles
the feature set well.

**Cons.** Same ensemble opacity as Random Forest, and **less widely recognized** — it offers no clear
advantage over Random Forest for this project while being slightly less familiar to a reviewer.

**Risks.** Same interpretability trade-off as Random Forest, with weaker name recognition and no
offsetting benefit.

**Expected implementation effort.** **Low–Medium** — robust defaults.

**Explainability suitability.** **Moderate** — feature importance only, as with Random Forest.

**Portfolio suitability.** **Moderate–Strong** — solid, but a less obvious choice than Random Forest.

**Fit score: 82 / 100.**

---

### 3.8 k-Nearest Neighbours

**Description.** Classify a match by the majority class among its k most similar past matches in feature
space.

**Pros.** Intuitive concept ("similar fixtures tended to end this way"); no training step; deterministic.

**Cons.** Sensitive to **feature scaling** and the **curse of dimensionality**; no global structure,
coefficients, or rules, so explanation is shallow. Probability estimates are crude (vote fractions).
Tends to underperform on this kind of tabular data and needs k-selection.

**Risks.** Scaling/distance choices materially change results; weak, hard-to-explain predictions; poor
fit to correlated engineered features.

**Expected implementation effort.** **Low–Medium** — simple algorithm but scaling and k-tuning required.

**Explainability suitability.** **Moderate** — the *idea* is intuitive, but there is little to inspect.

**Portfolio suitability.** **Moderate** — recognizable but a weaker, less insightful choice here.

**Fit score: 71 / 100.**

---

### 3.9 Naive Bayes

**Description.** A probabilistic classifier applying Bayes' rule under a (naive) feature-independence
assumption; native multiclass.

**Pros.** Extremely simple, fast, and deterministic; gives class probabilities and per-feature
contributions; a respectable, honest baseline-adjacent model.

**Cons.** The **independence assumption is badly violated** by the engineered features (goals scored,
conceded, and difference are strongly correlated), which hurts both fit and calibration. Probabilities
are often poorly calibrated.

**Risks.** Misleading confidence from violated assumptions; weaker fit to the chosen feature set.

**Expected implementation effort.** **Low** — a standard, near-zero-tuning fit.

**Explainability suitability.** **Good** — probabilistic and decomposable, though the independence story
needs a caveat.

**Portfolio suitability.** **Moderate** — simple and honest, but a weaker fit to correlated features than
logistic regression.

**Fit score: 77 / 100.**

---

### 3.10 Linear Discriminant Analysis (other realistic classical model)

**Description.** A classical linear classifier that models each class with a shared-covariance Gaussian
and derives linear decision boundaries; native multiclass with probabilities.

**Pros.** Simple, fast, deterministic; interpretable linear structure; works on small numeric feature
sets and naturally handles multiple classes.

**Cons.** Assumes Gaussian features with shared covariance — only roughly true here. Offers little over
**logistic regression** while being **less familiar** to a general reviewer and giving a slightly less
direct "coefficient" story.

**Risks.** Assumption violations; redundancy with logistic regression without a clear advantage.

**Expected implementation effort.** **Low** — a standard, near-zero-tuning fit.

**Explainability suitability.** **Good** — linear and interpretable, if less intuitive than logistic
coefficients.

**Portfolio suitability.** **Moderate** — competent and classical, but logistic regression is the
stronger, more recognizable linear choice.

**Fit score: 82 / 100.**

> **Other candidates considered and set aside.** A **linear Support Vector Machine** is classical but
> less probabilistic and less reader-friendly than logistic regression; an **ordinal logistic model**
> (exploiting a home>draw>away ordering) is intriguing but adds interpretive nuance for little gain and
> is better noted as future work; **deep learning, large neural nets, foundation models, and
> LLM/GPU-dependent approaches are excluded by `MODELING_SPEC.md` §7 and `AGENTS.md` §10.** None
> displaces the ten scored candidates.

---

## 4. Model Comparison Table

Scores are 1–5 per criterion (see §2.1 rubric); the final column is the weighted Fit Score /100.
Abbreviations: **Ex** explainability, **PV** portfolio value, **Rep** reproducibility, **Rev** reviewer
comprehension, **HDA** fit for Home/Draw/Away, **Feat** suitability for the selected feature set,
**EvCl** evaluation clarity, **Simp** implementation simplicity, **40–60h** budget fit, **Maint**
maintainability.

| Model | Ex (×5) | PV (×5) | Rep (×5) | Rev (×4) | HDA (×4) | Feat (×4) | EvCl (×3) | Simp (×3) | 40–60h (×4) | Maint (×2) | **Fit /100** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Logistic Regression** | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | **97** |
| **Decision Tree** | 5 | 4 | 5 | 5 | 4 | 4 | 4 | 5 | 5 | 4 | **91** |
| **Home-advantage baseline** | 5 | 3 | 5 | 5 | 5 | 2 | 5 | 5 | 5 | 5 | **89** |
| **Majority-class baseline** | 5 | 3 | 5 | 5 | 4 | 2 | 5 | 5 | 5 | 5 | **87** |
| **Random Forest** | 3 | 5 | 5 | 4 | 5 | 5 | 4 | 4 | 4 | 4 | **87** |
| **Extra Trees** | 3 | 4 | 5 | 3 | 5 | 5 | 4 | 4 | 4 | 4 | **82** |
| **Linear Discriminant Analysis** | 4 | 3 | 5 | 3 | 4 | 4 | 4 | 5 | 5 | 4 | **82** |
| **Naive Bayes** | 4 | 3 | 5 | 4 | 3 | 2 | 4 | 5 | 5 | 4 | **77** |
| **Gradient Boosted Trees** | 2 | 5 | 4 | 3 | 5 | 5 | 4 | 3 | 3 | 3 | **75** |
| **k-Nearest Neighbours** | 3 | 3 | 5 | 4 | 3 | 3 | 3 | 4 | 4 | 3 | **71** |

> Weighted Fit = Σ(score × weight) ÷ 39 × 20, rounded to the nearest whole number.

---

## 5. Ranked Recommendation

1. **Logistic Regression** (97) — the interpretable, probabilistic, multiclass classifier that best fits
   the project's priorities and feature set.
2. **Decision Tree** (91) — maximally transparent and simple; higher variance limits it as the headline.
3. **Home-advantage baseline** (89) — the football-honest reference (recommended baseline).
4. **Majority-class baseline** (87) — the absolute-floor reference (companion baseline).
4. **Random Forest** (87) — robust predictive safety net; less interpretable (recommended fallback).
6. **Extra Trees** (82) — Random-Forest-like, less recognized, no offsetting advantage.
6. **Linear Discriminant Analysis** (82) — competent linear model, but logistic is the better linear choice.
8. **Naive Bayes** (77) — simple, but its independence assumption fits the correlated features poorly.
9. **Gradient Boosted Trees** (75) — strongest predictively, weakest on interpretability/budget priorities.
10. **k-Nearest Neighbours** (71) — intuitive but shallow and a poor fit to the data.

> **Reading the ranking.** The interpretable, deterministic, low-tuning models cluster at the top because
> they best satisfy the highest-weighted criteria (portfolio value, reproducibility, explainability). The
> tree *ensembles* score respectably on power and robustness but are pulled down by opacity; Gradient
> Boosting in particular is penalized precisely because the project does **not** prize raw accuracy over
> interpretability and finishability. Baselines score well in their reference role despite using no
> features — exactly as intended.

---

## 6. Recommended Baseline, Selected Model, Fallback, and Rationale

### Recommended Baseline

**Home-advantage baseline** (predict the home win / H/D/A base rates), with the **majority-class
baseline** reported alongside as the absolute floor.

It best satisfies the four baseline criteria:

- **Honesty** — it states the single best-established effect in football and nothing more; every later
  claim is measured against this honest yardstick (`MODELING_SPEC.md` §4; `EVALUATION_SPEC.md` §3).
- **Simplicity** — a constant home prediction / base-rate prior, with zero tuning.
- **Interpretability** — self-explanatory to any reader and tied directly to the project's
  home-advantage narrative.
- **Reproducibility** — fully deterministic from the documented data, with no randomness.

In this target the home-advantage prior effectively coincides with the majority class, so the two are
near-equivalent; the home-advantage framing is preferred as the headline because it is more
football-meaningful, while majority-class is reported as the no-information floor.

### Recommended Selected Model

**Multinomial Logistic Regression** (binary logistic for the fallback target).

It best satisfies the four selected-model criteria:

- **Portfolio value** — the canonical, respected demonstration of interpretable classification; it gives
  the cleanest baseline → selected-model narrative a reviewer can follow (`PORTFOLIO_HANDOFF_SPEC.md`).
- **Explainability** — signed coefficients / odds ratios map directly to plain-language drivers (home
  edge, recent form, goal difference), supporting both local and global reader-facing explanations
  (`EXPLAINABILITY_SPEC.md` §6–§8) — the gold standard for this project.
- **Predictive usefulness** — native multiclass with probabilistic outputs well-suited to the small,
  correlated, numeric engineered feature set, and a genuine, justified improvement over the baseline.
- **Finishability** — near-zero tuning, fully deterministic, and trivially within the 40–60 hour budget
  (`MODELING_SPEC.md` §12).

### Recommended Fallback Model

**Random Forest** — a lower-risk alternative if the selected model underperforms or the modelling becomes
too complex.

- **If logistic regression underperforms** (its linear boundary misses important feature interactions),
  Random Forest is the robust, low-tuning ensemble that recovers predictive power while remaining a
  classical, allowed family (`MODELING_SPEC.md` §5), staying deterministic with a fixed seed, and
  offering global feature-importance explanations.
- **If anything richer becomes too complex** (e.g. drifting toward Gradient Boosting and its tuning),
  Random Forest is the safer stop: strong defaults, little tuning, and no budget/complexity blow-up
  (§12).
- It is recommended over Extra Trees (less recognized, no advantage) and over Gradient Boosting (more
  tuning, less interpretable). For a fallback in the **opposite** direction — *even simpler and more
  transparent* — a single **Decision Tree** is the natural alternative, accepting its higher variance.

> **Why not the #2-ranked Decision Tree as fallback?** The fallback's job is to be a low-risk safety net
> if the linear model *underperforms*; a single high-variance tree is a weak remedy for that, whereas
> Random Forest robustly adds predictive power. The Decision Tree's higher fit score reflects its
> transparency and simplicity (where it genuinely excels), not its suitability for recovering
> performance — so it is offered as the simpler-direction alternative, not the primary fallback.

### Rationale (alignment with the specifications)

- **`PROJECT_OVERVIEW.md` — portfolio value & scope.** The trio (honest baseline → interpretable
  selected model → robust classical fallback) is exactly the bounded, interpretable-first story the
  overview prizes, with no drift toward excluded deep-learning or accuracy-chasing territory.
- **`MODELING_SPEC.md` — baseline-first, interpretable, finishable.** A mandatory transparent baseline
  (§4), a selected model from the classical interpretable families (§5–§6), and respect for the
  complexity boundaries (§12) are all satisfied; the excluded families (§7) are excluded.
- **`EVALUATION_SPEC.md` — honest, baseline-relative.** Logistic regression's calibrated-ish
  probabilities and the baseline's reference probabilities support honest, baseline-relative evaluation
  and per-class (incl. draw) inspection — without selecting metrics here (deferred to §4/§14).
- **`EXPLAINABILITY_SPEC.md` — reader-first.** Coefficients give intuitive local and global explanations;
  the fallback's feature importances remain interpretable, and opaque options (Gradient Boosting) are
  down-ranked precisely for failing this priority.
- **`REPRODUCIBILITY_SPEC.md` — deterministic & laptop-friendly.** Every recommended model is
  deterministic from the same data plus a fixed configuration/seed, with no GPU/cloud dependency.
- **`PORTFOLIO_HANDOFF_SPEC.md` & `AGENTS.md` — finished, credible, in-scope.** The recommendation reads
  as competent, honest, and finishable, protecting the three-project strategy and the operating
  principles (explainable > complex; reproducible > clever; finished > ambitious).

---

## 7. Risks Carried Into the Decision

| Risk | Affects | Mitigation at decision time |
|------|---------|------------------------------|
| Linear model underperforms | Logistic Regression | Report honestly vs. baseline; if material, move to the Random Forest fallback. |
| Reduced interpretability of the fallback | Random Forest | Use feature importances; keep it a fallback, not the headline; explain the trade-off. |
| Multicollinearity among features | Logistic Regression | Apply light regularization; sanity-check coefficient stability. |
| Hard-to-predict draw class | All models | Inspect the draw class explicitly; don't rely on accuracy alone (`EVALUATION_SPEC.md`). |
| Tuning / complexity creep | Gradient Boosting (if reached) | Excluded from the recommendation; honor §12 boundaries. |
| Accuracy-chasing over interpretability | tree ensembles | Hold the interpretability-first priority; justify any complexity by a demonstrated gain. |
| Non-determinism in ensembles | Random Forest / Extra Trees | Fix seeds; document configuration for reproducibility. |

---

## 8. Honest Limitations of This Analysis

- **No data was inspected or modelled** (per constraints); scores reflect model characteristics against
  the spec criteria, not empirical accuracy on the Bundesliga data.
- **Fit scores are a structured judgment**, not a measurement; the **ranking and the
  baseline/selected/fallback split** are more meaningful than the exact number, and several mid-table
  models are deliberately close.
- **Predictive power is intentionally under-weighted** — the rubric encodes the project's priorities
  (interpretability, reproducibility, finishability), so the strongest pure predictor (Gradient Boosting)
  ranks low *for this project*, not in general.
- **No metrics are selected** — "evaluation clarity" judges how cleanly outputs support honest evaluation,
  not which metrics will be used; metric selection remains deferred to `EVALUATION_SPEC.md`.

---

## 9. Next Natural Step

Review this analysis and **select the modelling strategy** — recording the chosen baseline, selected
model, and fallback in [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md), per its deferred-decision table
(§16, "Final algorithm"). This document is **non-binding input** to that decision; it makes no change to
any spec, selects no metrics, and commits to no implementation.

---

> **Conformance:** This research artifact respects the scope boundaries, non-goals, priorities, budget
> philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) and
> the downstream specifications. It introduces no new project requirements, modifies no specification,
> selects no metrics, and does not finalize the modelling decision.
