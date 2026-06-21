# StatSport — Modelling Specification

**Modelling strategy specification**

> _How StatSport approaches modelling — interpretable, baseline-first, and finishable — without locking in a final algorithm._

| | |
|---|---|
| **Status** | Specification Phase |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Downstream specification (conforms to `PROJECT_OVERVIEW.md` and `DATA_SPEC.md`) |
| **Parents** | [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](DATA_SPEC.md) |

> **What this document is:** the modelling strategy for StatSport. It defines the modelling
> philosophy, objectives, boundaries, selection principles, and workflow. The prediction target is now
> fixed in **[Selected Prediction Target](#selected-prediction-target)** below, and the feature strategy
> is now fixed in **[Selected Feature Strategy](#selected-feature-strategy)** below; this document still
> does not select a final algorithm, validation scheme, hyperparameters, or training configuration. It
> conforms to the anchor overview and the data specification.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total.
> **Inherited rules of thumb:** reproducibility over raw predictive performance; explainability over
> model complexity; finishability over sophistication.

---

## Selected Prediction Target

> **Status:** Approved. This section converts the previously deferred *exact prediction target / label*
> into a fixed project decision. It follows the approved analysis in
> [`docs/research/PREDICTION_TARGET_ANALYSIS.md`](../research/PREDICTION_TARGET_ANALYSIS.md). All other
> modelling decisions remain deferred (see §16).

| Decision | Selected value |
|----------|----------------|
| **Approved prediction target** | Home / Draw / Away (1X2) — three-class classification of the full-time result |
| **Approved fallback target** | Home Win vs Not Home Win — binary classification |

### Decision rationale

The full-time match result (home win / draw / away win) was selected as the prediction target because
it is the canonical, recognizable football-prediction problem and is available directly from the
selected dataset (Football-Data.co.uk, Bundesliga, 2020/21–2024/25; see
[`DATA_SPEC.md`](DATA_SPEC.md)). It tells the complete match-outcome story, has an obvious and honest
baseline (a home-advantage / majority-class prior, per §4), and suits the classical, interpretable
model families this spec prefers (§5). The **fallback** — collapsing the result to *home win vs not
home win* — is a trivial, deterministic relabeling of the same data; it is held in reserve in case the
draw class proves too hard to model meaningfully or multiclass work threatens the budget, and switching
to it is cheap and reproducible.

### Alignment with portfolio goals

A home/draw/away predictor is the definitive demonstration of football match prediction — the
strongest, most recognizable signal to public project reviewers,
consistent with the portfolio-value priority in [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md). It stays
within the bounded scope and clear of the betting non-goal.

### Alignment with explainability goals

"Why home win, draw, or away win?" maps directly to intuitive, plain-language drivers (home advantage,
recent form, shot quality), supporting both local and global reader-facing explanations per
[`EXPLAINABILITY_SPEC.md`](EXPLAINABILITY_SPEC.md). The fallback's binary framing is, if anything, even
simpler to explain.

### Alignment with the 40–60 hour project budget

The target is taken directly from the dataset's result field (the fallback is a one-line relabeling),
so it adds no acquisition or derivation cost. It is modellable with standard classical methods — no
GPUs, model zoos, or heavy tuning (§7, §12) — keeping the work comfortably finishable within the
40–60 hour budget and leaving room for the other two summer portfolio projects.

> **Full comparison and ranking:** see
> [`docs/research/PREDICTION_TARGET_ANALYSIS.md`](../research/PREDICTION_TARGET_ANALYSIS.md).

---

## Selected Feature Strategy

> **Status:** Approved. This section converts the previously deferred *final feature set* into a fixed
> project decision. It follows the approved analysis in
> [`docs/research/FEATURE_ENGINEERING_ANALYSIS.md`](../research/FEATURE_ENGINEERING_ANALYSIS.md). All
> other modelling decisions remain deferred (see §16). The decision fixes *which feature groups are in,
> optional, and out*; concrete window lengths, encodings, and the implementation mechanism remain
> deferred to later work, consistent with §9.

### Approved Core Feature Set

Result-derived, deterministic, leakage-safe, and maximally interpretable — the spine of the model and
the explainability narrative. These should almost certainly be included.

| Core feature group | What it captures |
|--------------------|------------------|
| **Home advantage** | The home/away edge — fixture home/away encoding plus home/away result splits. |
| **Recent form** | Rolling recent results over a team's last N matches, pre-match. |
| **Goals scored** | Rolling attacking rate (goals scored per match), pre-match. |
| **Goals conceded** | Rolling defensive rate (goals conceded per match), pre-match. |
| **Goal difference** | Rolling net strength (scored minus conceded) as a compact summary. |

### Approved Optional Feature Set

Worth including only while implementation stays simple and the budget holds; each must earn its place
against the baseline (§4). They add genuine value but cost more in leakage discipline, reconstruction,
or complexity.

| Optional feature group | What it captures / cost |
|------------------------|-------------------------|
| **Shots on target** | Rolling shot-quality proxy (for/against), pre-match; the strongest event-statistic feature. Requires rolling pre-match aggregation. |
| **League position** | Pre-match standings context, reconstructed leak-free as of each matchday. |
| **Elo-style rating** | A running team-strength rating; the highest-value optional. Include **one** deterministic, documented rating only if budget allows. |

### Approved Excluded Feature Set

Excluded by default — they add complexity, dimensionality, or noise without enough portfolio value, or
are excluded by data availability or project principle. Excluded means *out of the default plan*, not
forbidden as future work.

| Excluded feature group | Reason for exclusion |
|------------------------|----------------------|
| **Corner features** | Weak link to outcomes; betting-flavored as a standalone metric. |
| **Card features** | Noisy discipline proxy; reflects style/refereeing more than team quality. |
| **Strength-of-schedule features** | Circular and complex; a real complexity-creep risk for limited gain (§12). |
| **Bookmaker odds** | Excluded by the betting non-goal (`PROJECT_OVERVIEW.md`; `AGENTS.md` §8). |
| **xG features** | Not available in the selected dataset. |
| **Possession features** | Not available in the selected dataset. |
| **Player-level features** | Not available in the selected dataset; also out of the bounded scope. |

### Decision rationale

The selected strategy keeps a **small, coherent, non-redundant** feature set built on the cleanest,
most interpretable signals the dataset offers. The core is entirely **result-derived** — home advantage,
recent form, and rolling goals scored/conceded/difference — which is trivially reproducible, leakage-safe,
and immediately understandable. Because every match statistic is only known *after* a match, **all
features are pre-match rolling aggregates over prior fixtures** (no future information leaks into a
prediction), consistent with §11. The optional set adds the highest-value extensions (shot quality,
standings context, an Elo rating) without making them prerequisites, and the excluded set removes weak,
noisy, unavailable, or principle-excluded signals before they inflate scope. Form, rolling points, and
goal difference overlap by design, so they are treated as one family and consolidated rather than
double-counted.

> **Full comparison, scoring, and ranking:** see
> [`docs/research/FEATURE_ENGINEERING_ANALYSIS.md`](../research/FEATURE_ENGINEERING_ANALYSIS.md).

### Alignment with portfolio goals

The core set is the recognizable, expected feature spine of a football predictor — the strongest, cleanest
signal to public project reviewers, consistent with the
portfolio-value priority in [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md). It stays squarely within the
bounded scope and well clear of the betting non-goal (so odds, corners, and cards are excluded or
down-weighted), and the compactness reads as competent, finished judgment rather than feature sprawl.

### Alignment with explainability goals

Every core feature maps to a plain-language driver — home edge, recent form, attacking and defensive
strength — supporting both local ("why this prediction") and global ("how the model behaves")
explanations for a non-expert reader, per [`EXPLAINABILITY_SPEC.md`](EXPLAINABILITY_SPEC.md). Noisy
features that explain poorly (corners, cards) are excluded precisely because they would weaken the
reader-facing narrative.

### Alignment with reproducibility goals

All approved features are **regenerable deterministically** from the documented Football-Data.co.uk
fields via rolling computations, consistent with [`REPRODUCIBILITY_SPEC.md`](REPRODUCIBILITY_SPEC.md)
and §14. The one stateful optional (Elo) is flagged to require fixed, documented parameters and
initialization so its output stays deterministic. No feature depends on unavailable signals (xG,
possession, player data) or external tooling.

### Alignment with the 40–60 hour budget

The core features are cheap rolling aggregates over clean columns, leaving budget for honest evaluation
and explanation — and for the other two summer portfolio projects. The optional set is explicitly
gated ("only while implementation stays simple"), and the most complex candidates (strength of schedule)
are excluded, protecting finishability and the complexity boundaries in §12.

---

## 1. Purpose of the Modelling Layer

The modelling layer turns the prepared data (per `DATA_SPEC.md`) into **explainable predictions** for
a well-defined match outcome, demonstrating sound machine-learning practice end to end. Its job is to
show **competence and judgment** — clean baselines, justified improvements, honest comparison, and
interpretable results — not to chase maximum predictive performance.

Concretely, the modelling layer must:

- Establish a mandatory **baseline** as the reference point for all later claims.
- Develop a **selected model** from interpretable, classical ML families that improves on the baseline
  in a justified way.
- Keep the entire workflow **reproducible** and **finishable** within the 40–60 hour budget.
- Produce outputs that can be **explained** to a non-expert reviewer.

---

## 2. Modelling Philosophy

StatSport's modelling is governed by these preferences:

- **Demonstrate sound machine-learning practice** — the point is to show *how* one models well.
- **Do not optimize for maximum leaderboard performance** — marginal accuracy is not the goal.
- **Prefer interpretable models** — understandable behavior outranks opaque power.
- **Prefer simplicity over sophistication** — the simplest credible approach wins.
- **Prefer understanding over marginal gains** — insight beats a fractionally better score.
- **Prefer reproducibility over experimentation volume** — a few clean, repeatable runs beat many
  ad-hoc ones.

When these preferences conflict, the inherited priority order and the time budget decide.

---

## 3. Modelling Objectives

- Define and predict a **single, well-bounded outcome** (the exact target is **deferred** to the data
  and modelling decisions, consistent with the overview).
- Produce a **baseline** and at least one **selected model**, with the baseline as the reference.
- **Justify any improvement** of the selected model over the baseline — never assume it.
- Make predictions **explainable**, so a reader understands *why* a prediction was made.
- Keep the whole effort **reproducible and within budget**.

> "Selected model" follows the overview's wording: a baseline model and a selected model (or candidate
> model(s)); there is no mandatory single "primary" model.

---

## 4. Baseline-First Principle

- **A baseline model is mandatory.** No modelling claim is made without one.
- **Every selected (or candidate) model must be compared against the baseline.**
- **Improvement must be justified, not assumed** — a more complex model earns its place only if it
  demonstrably and meaningfully beats the baseline under a reproducible procedure.
- The baseline is intentionally **simple and transparent**, serving as an honest reference and a guard
  against over-claiming.

---

## 5. Candidate Model Families

The following **classical, interpretable** families are acceptable *in principle* (named as
categories, not as a final choice):

- **Linear models**
- **Logistic models**
- **Decision-tree models**
- **Random-forest–style models**
- **Gradient-boosted tree models**
- **Other classical, interpretable ML families** consistent with the philosophy

> These are candidate categories only. **No final algorithm is selected** in this document.

---

## 6. Model Selection Criteria

A model family/approach is a *candidate* when it is:

- **Interpretable** — its behavior can be explained to a reviewer.
- **Simple enough** to implement, understand, and finish within budget.
- **Reproducible** — produces the same results from the same inputs and configuration.
- **Appropriate to the data** prepared per `DATA_SPEC.md` (small-to-medium, tabular).
- **Comparable to the baseline** under a consistent, reproducible procedure.
- **Justifiable** — its complexity is warranted by a meaningful, demonstrated gain.

---

## 7. Model Exclusion Criteria

A model/approach is **excluded** if it is:

- A **deep-learning-first** approach.
- A **large neural network**.
- A **foundation model**.
- **LLM-based modelling**.
- A **GPU-dependent workflow**.
- Any **architecture that threatens the 40–60 hour budget** (excessive training time, tuning, or
  infrastructure).

These exclusions are consistent with the overview's non-goals (no deep-learning rabbit holes, no
large-scale or specialized infrastructure).

---

## 8. Explainability Requirements

Explainability is a **first-class** modelling requirement, inherited from the overview:

- Predictions must be **accompanied by interpretation**, not presented as bare numbers.
- The chosen approach must **lend itself to clear explanation** (e.g., understandable feature
  influence or inherently interpretable structure).
- Explanations must be **reader-facing** (figures and/or narrative), suitable for a non-expert.
- **Interpretability informs model choice** — given a tie, the more explainable option wins.

> Specific explainability methods/tools are **deferred** (named as candidates only), consistent with
> the overview.

---

## 9. Feature Engineering Principles

- **Features must be understandable** — a reader can grasp what each represents.
- **Features must be explainable** — they support, rather than obscure, interpretation.
- **Features must be reproducible** — derivable deterministically from the processed data.
- **Features should support interpretation** — chosen to illuminate *why*, not just to boost a score.
- Feature work stays **modest and justified**, avoiding excessive engineering that threatens the
  budget (consistent with the overview's scope-creep guardrails).

> The **final feature set** is now **fixed** — see
> [Selected Feature Strategy](#selected-feature-strategy). These principles continue to govern *how*
> those features are derived; concrete window lengths, encodings, and the implementation mechanism
> remain deferred to later work.

---

## 10. Training Principles

- **Reproducible training** — same data + configuration ⇒ same model (e.g., controlled randomness).
- **Modest and bounded** — training must run comfortably on a laptop, with no GPU dependence.
- **Transparent** — training steps are documented well enough to be re-run by others.
- **Budget-aware** — training cost (time and complexity) must fit within the 40–60 hour budget.
- **Honest** — no training-time practices that would inflate apparent performance.

> The **final training configuration** is **deferred**.

---

## 11. Validation Principles

- **Avoid leakage** — no information from the evaluation target leaks into training or features.
- **Preserve temporal integrity where appropriate** — respect chronological order when the problem is
  time-dependent (e.g., do not train on the future to predict the past).
- **Use reproducible evaluation procedures** — the same procedure yields the same results.
- **Keep validation aligned with portfolio goals** — clear, honest, and explainable over elaborate.
- Always frame results **relative to the baseline** (see §4).

> The **final validation scheme** is **deferred** (detailed metrics and scheme belong to the
> evaluation specification).

---

## 12. Complexity Boundaries

To protect finishability and the budget, the project will **not** build:

- **A model zoo** — no sprawling collection of models.
- **Massive hyperparameter searches** — no exhaustive sweeps.
- **AutoML dependency** — no reliance on automated model-search tooling.
- **Ensemble stacks of excessive complexity** — no elaborate stacking/blending.
- **Research-grade experimentation** — no open-ended research programme.

A small number of clean, well-understood, reproducible models is the target.

---

## 13. Portfolio-Quality Expectations

The modelling work should read as **competent, honest, and finished**:

- A **clear baseline → selected-model** narrative a reviewer can follow.
- **Justified choices** — every step explainable in plain language.
- **Honest comparison** against the baseline, with limitations acknowledged.
- **Interpretable results** suitable for public GitHub publication and technical review.
- **Reproducibility** that lets a reader re-run and trust the results.
- Scoped to remain **one of three** completed summer portfolio repositories.

---

## 14. Reproducibility Requirements

Reproducibility outranks raw predictive performance:

- **Deterministic results** — controlled randomness (e.g., fixed seeds) so runs are repeatable.
- **Documented workflow** — the path from processed data to model to results is written down.
- **Regenerable artifacts** — models and results can be reproduced from documented inputs and steps;
  large artifacts are not committed (consistent with `DATA_SPEC.md` and the repository `.gitignore`).
- **No hidden manual steps** — any manual action is recorded explicitly.
- **Mechanism-agnostic** — notebooks, scripts, or a combination are acceptable (per the overview).

---

## 15. Modelling Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Chasing accuracy** | Over-optimizing for marginal score gains | Baseline-first; justify improvement; stop at a defensible result. |
| **Complexity creep** | Drifting into model zoos / heavy tuning | Enforce §12 complexity boundaries. |
| **Deep-learning rabbit hole** | Reaching for neural nets / foundation models | Excluded per §7; prefer classical interpretable families. |
| **Data leakage** | Target information leaking into features/training | Apply §11 validation principles; review feature provenance. |
| **Temporal leakage** | Using future data to predict the past | Preserve temporal integrity where appropriate. |
| **Reproducibility drift** | Non-deterministic or undocumented runs | Control randomness; document the workflow. |
| **Budget overrun** | Modelling work exceeds 40–60h | Keep models few and simple; defer extras to future work. |
| **Opaque results** | Models that cannot be explained | Prioritize interpretable families; require reader-facing explanations. |

---

## 16. Deferred Modelling Decisions

The following are intentionally **not** decided here and remain deferred:

| Deferred decision | Status / owning step |
|-------------------|----------------------|
| **Final algorithm** | Deferred — chosen later from the candidate families under §6. |
| **Final feature set** | ✅ **Approved** — core/optional/excluded feature groups fixed; see [Selected Feature Strategy](#selected-feature-strategy). |
| **Final validation scheme** | Deferred — detailed in the evaluation specification. |
| **Final hyperparameters** | Deferred. |
| **Final training configuration** | Deferred. |
| Exact prediction target/label | ✅ **Decided** — Home / Draw / Away (1X2), fallback Home Win vs Not Home Win; see [Selected Prediction Target](#selected-prediction-target). |
| Specific explainability methods/tools | Deferred — named as candidates only. |
| Concrete implementation mechanism (script vs. notebook vs. both) | Deferred (overview allows either or both). |

> This specification establishes the **rules and philosophy** for modelling. With the prediction target
> and the feature strategy now fixed, it deliberately still does **not** select a final algorithm,
> validation scheme, hyperparameters, or training configuration — those decisions remain open by design.

---

> **Conformance:** This document inherits and respects the scope boundaries, non-goals, priorities,
> budget philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md), and
> builds on the data rules in [`DATA_SPEC.md`](DATA_SPEC.md). It introduces no new project
> requirements beyond modelling-layer rules.
