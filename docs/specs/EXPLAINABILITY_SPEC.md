# StatSport — Explainability Specification

**Explainability strategy specification**

> _How StatSport makes its predictions understandable — reader-first and accessible — using an
> approved native explainability strategy while preserving later visualization and presentation
> decisions._

| | |
|---|---|
| **Status** | Specification Phase |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Downstream specification (conforms to `PROJECT_OVERVIEW.md`, `DATA_SPEC.md`, `MODELING_SPEC.md`, `EVALUATION_SPEC.md`) |
| **Parents** | [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](DATA_SPEC.md) · [`MODELING_SPEC.md`](MODELING_SPEC.md) · [`EVALUATION_SPEC.md`](EVALUATION_SPEC.md) |

> **What this document is:** the explainability strategy for StatSport. It defines the explainability
> philosophy, objectives, interpretation standards, communication expectations, and boundaries — with
> the final explainability method, tooling stance, and workflow now approved in
> **[Selected Explainability Strategy](#selected-explainability-strategy)** below. Final explanation
> visualizations and final presentation format remain deferred. It conforms to the anchor overview and
> the data, modelling, and evaluation specifications.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total.
> **Inherited rules of thumb:** explainability is a first-class requirement; understanding over
> sophistication; communication over technical novelty; a reviewer should be able to understand *why*
> a prediction was produced.

---

## Selected Explainability Strategy

> **Status:** Approved. This section converts the previously deferred explainability method, tooling
> stance, and workflow into fixed project decisions. It follows the approved analysis in
> [`docs/research/EXPLAINABILITY_STRATEGY_ANALYSIS.md`](../research/EXPLAINABILITY_STRATEGY_ANALYSIS.md).
> Final explanation visualizations and final presentation format remain deferred (see §14).

### Approved Global Explainability

**Standardized coefficient analysis**

The primary global explanation strategy is standardized logistic regression coefficient analysis,
supported by:

- Class-specific feature rankings.
- Coefficient direction interpretation.
- Optional odds-ratio examples for a small number of headline effects.

### Approved Local Explainability

**Coefficient contribution analysis**

The primary local explanation strategy is coefficient contribution analysis for individual predictions,
supported by:

- Feature-difference explanations.
- Probability explanations.
- Example-based explanations.

### Approved Portfolio Explainability Artifacts

The approved portfolio explainability artifact set is:

- Global feature influence table/figure.
- Model behaviour summary.
- Three prediction explanation cards.
- Feature context tables.
- Limitations and uncertainty note.

These artifact categories define the required reader-facing content, not exact chart designs, report
layouts, or visual templates.

### Approved Fallback Explainability

If Random Forest becomes the selected model, the fallback explainability strategy is:

- Permutation feature importance.
- Example-based explanations.
- Feature-difference explanations.

SHAP is **not recommended by default**. It should be considered only if Random Forest becomes the final
selected model and simpler fallback explanations prove insufficient. LIME is **not recommended** for
this project.

### Explainability Rationale

This strategy is approved because it uses the selected model's native interpretability rather than
adding unnecessary explainability machinery.

It aligns with [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) by keeping explainability bounded,
reader-facing, and finishable within the 40–60 hour portfolio budget. The project needs a clear
demonstration of data and ML communication, not a research-grade XAI subsystem.

It aligns with [`MODELING_SPEC.md`](MODELING_SPEC.md) because multinomial logistic regression was
chosen partly for interpretability. Standardized coefficients explain global model behaviour directly,
and coefficient contributions explain individual predictions using the same model parameters. Native
interpretability is preferred because it explains the actual selected model without an additional
surrogate explanation layer.

It aligns with [`EVALUATION_SPEC.md`](EVALUATION_SPEC.md) because the artifacts can be tied to the
approved chronological evaluation workflow, predicted probabilities, class-specific performance, and
known draw-class difficulty. Explanation cards should support honest interpretation of correct,
uncertain, and weak predictions rather than only flattering examples.

It aligns with [`REPRODUCIBILITY_SPEC.md`](REPRODUCIBILITY_SPEC.md) because standardized coefficients,
coefficient contributions, feature context tables, and probability explanations are deterministic and
traceable to the evaluated model, approved features, and documented data pipeline. This avoids hidden
manual reasoning and keeps explanations regenerable.

Logistic Regression does not require SHAP by default because its coefficients and feature
contributions already expose the model's decision structure. SHAP would add dependency, background
sample, multiclass-output, and interpretation choices without improving the core reader question:
"why did this model predict home, draw, or away?"

Logistic Regression does not require LIME because LIME would fit a local surrogate to explain a model
that is already locally explainable through its own coefficients. That extra surrogate layer would add
randomness and configuration choices while weakening reproducibility and reader comprehension.

Simplicity is preferred because the goal is a finished, honest, reproducible portfolio project.
Native coefficient-based explanations are easier to audit, easier to communicate, and easier to
regenerate than heavier tooling, while still satisfying the global and local explanation requirements.

---

## 1. Purpose of the Explainability Layer

The explainability layer ensures that StatSport's predictions can be **understood**, not just
produced. Its job is to make the *why* behind predictions and overall model behaviour **clear to a
reader** — demonstrating that the author can communicate machine-learning results responsibly.

Concretely, the explainability layer must:

- Make individual predictions **interpretable**, never bare unexplained outputs.
- Explain **overall model behaviour** and the **important feature influences**.
- Communicate explanations in **plain, accessible language** for non-experts.
- Stay aligned with the modelling and evaluation work, and remain **reproducible** and **finishable**
  within the 40–60 hour budget.

---

## 2. Explainability Philosophy

StatSport's explainability is governed by these principles:

- **Explainability is mandatory** — it is a first-class requirement, not an optional add-on.
- **Predictions must be understandable** — a reader can follow what was predicted and why.
- **Explanations must be accessible to non-experts** — written for technically literate non-specialists.
- **Simpler explanations are preferred** — the clearest sufficient explanation wins.
- **Understanding outranks sophistication** — comprehension matters more than technical depth.
- **Communication outranks novelty** — clear communication matters more than novel methods.

When these principles conflict, the inherited priority order and the time budget decide.

---

## 3. Explainability Objectives

- Ensure **no prediction appears as an unexplained output** — each is accompanied by reasoning.
- Provide both **local** explanations (why a specific prediction) and **global** explanations (how the
  model behaves overall).
- Make **feature influence interpretable** and connected to a plain-language narrative.
- Explain **limitations and uncertainty** honestly, consistent with `EVALUATION_SPEC.md`.
- Keep explanations **reproducible** and **reviewer-friendly**, within budget.

---

## 4. Reader-First Interpretation Principle

Explanations are written **for the reader**, specifically:

- **Portfolio reviewers** assessing competence and communication.
- **Technical reviewers** assessing the project.
- **Technically literate non-specialists** who are not ML experts.

Accordingly:

- **Avoid unnecessary jargon**; define terms when they are needed.
- Lead with **meaning and intuition**, not formulas.
- Assume the reader is intelligent but **lacks project-specific context**.

---

## 5. Explainable Model-Selection Principles

- **Explainability influences model selection** — interpretability is a selection criterion, not an
  afterthought (consistent with `MODELING_SPEC.md`).
- **If two models perform similarly, prefer the more explainable model.**
- **Complexity must justify itself** — added model complexity is acceptable only when it brings a
  meaningful, demonstrated benefit that outweighs the loss of interpretability.
- This reinforces the modelling spec's preference for classical, interpretable families.

---

## 6. Feature Interpretation Principles

- **Features should have understandable meaning** — a reader can grasp what each represents
  (consistent with the feature principles in `MODELING_SPEC.md`).
- **Feature influence should be interpretable** — the direction and rough importance of a feature's
  effect can be communicated plainly.
- **Features should support narrative explanation** — they help tell a coherent story about *why*
  predictions occur, rather than serving as opaque inputs.
- Feature interpretation must trace back to **reproducible, documented** features (per `DATA_SPEC.md`).

---

## 7. Prediction Explanation Requirements

- **Predictions should not appear as unexplained outputs** — a raw number or label alone is
  insufficient.
- **Predictions should be accompanied by reasoning** — a reader should see *why* the model produced a
  given prediction.
- **Explanations should connect model behaviour and feature behaviour** — linking the model's logic to
  the features driving a specific prediction.
- Local explanations should be **honest and proportionate**, not overstated.

---

## 8. Global Explanation Requirements

At the level of the model as a whole, the project must:

- **Explain overall model behaviour** — how the model generally makes decisions.
- **Explain important feature influences** — which features matter most and in what direction.
- **Explain limitations** — where and why the model is weak or uncertain.
- **Explain uncertainty appropriately** — communicate confidence honestly, consistent with
  `EVALUATION_SPEC.md`, without false precision.

---

## 9. Communication Requirements

- **Use plain language where possible** — prioritize clarity over technical phrasing.
- **Avoid unnecessary mathematical complexity** — include math only when it genuinely aids
  understanding.
- **Focus on understanding** — the goal is for the reader to *get it*.
- **Focus on reviewer comprehension** — explanations are judged by whether a reviewer understands them.
- Explanations are delivered in **reader-facing form** (narrative and/or figures), consistent with the
  presentation priority.

---

## 10. Portfolio-Quality Explainability Expectations

The explainability work should read as **clear, honest, and finished**:

- A reader can answer **"why did the model predict this?"** after reading.
- Explanations are **accessible**, jargon-light, and well-communicated.
- **Global and local** views are both present and consistent.
- **Limitations and uncertainty** are explained, not hidden.
- Work is **reproducible** and suitable for **public GitHub publication** and **technical review**,
  scoped to remain **one of three** completed summer portfolio repositories.

---

## 11. Reproducibility Requirements

Explanations must be **reproducible**, consistent with the inherited reproducibility mandate:

- **Deterministic explanations** — the same inputs and configuration yield the same explanations
  (e.g., controlled randomness where relevant).
- **Documented workflow** — how explanations are produced is written down, mechanism-agnostic
  (notebooks, scripts, or both, per the overview).
- **Regenerable artifacts** — explanation figures/outputs can be regenerated; large artifacts are not
  committed, consistent with `DATA_SPEC.md` and the repository `.gitignore`.
- **Traceable to data and model** — explanations reference reproducible features and the evaluated
  model, not ad-hoc constructs.
- **No hidden manual steps** — any manual action is recorded explicitly.

---

## 12. Explainability Exclusions

To protect understanding, simplicity, and the budget, the project will **not** undertake:

- **An explainability research project** — no open-ended investigation.
- **Novel explainability methods** — no inventing new techniques.
- **Explainability framework benchmarking** — no comparing tools/frameworks against one another.
- **Excessive explainability tooling** — no heavy or sprawling tool stacks.
- **Complexity that threatens the 40–60 hour budget** — no effort that endangers finishability.

These exclusions are consistent with the overview's non-goals and the modelling spec's complexity
boundaries.

---

## 13. Explainability Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Jargon overload** | Explanations too technical for the audience | Reader-first principle (§4); plain language (§9). |
| **Unexplained predictions** | Outputs presented without reasoning | Require reasoning with every prediction (§7). |
| **Tooling rabbit hole** | Over-investing in explainability frameworks | Honor exclusions (§12); keep tooling minimal. |
| **Method novelty creep** | Drifting toward research-grade methods | No novel methods; prefer simple, established ideas (§2, §12). |
| **Inconsistent local/global views** | Local and global explanations disagree | Connect model and feature behaviour coherently (§3, §7, §8). |
| **Overclaiming influence** | Overstating what features "cause" | Proportionate, honest interpretation; explain uncertainty (§8). |
| **Irreproducible explanations** | Non-deterministic or undocumented outputs | Deterministic, documented workflow (§11). |
| **Budget overrun** | Explainability work exceeds its share | Keep it simple and reviewer-focused; defer extras. |

---

## 14. Deferred Explainability Decisions

The following table records which explainability decisions are now approved and which intentionally
remain deferred:

| Deferred decision | Status / owning step |
|-------------------|----------------------|
| **Final explainability method** | Approved — standardized coefficient analysis globally and coefficient contribution analysis locally; see [Selected Explainability Strategy](#selected-explainability-strategy). |
| **Final explainability tooling** | Approved — native logistic-regression interpretability by default; SHAP not recommended by default and LIME not recommended; see [Selected Explainability Strategy](#selected-explainability-strategy). |
| **Final explanation visualizations** | Deferred. |
| **Final explanation workflow** | Approved — global analysis, local explanation cards, portfolio artifacts, and fallback handling; see [Selected Explainability Strategy](#selected-explainability-strategy). |
| **Final presentation format** | Deferred. |
| Exact prediction target/label | Deferred (inherited from prior specs). |
| Concrete implementation mechanism (script vs. notebook vs. both) | Deferred (overview allows either or both). |

> This specification establishes the **rules, philosophy, approved explainability method, tooling
> stance, and workflow** for explainability. It deliberately does **not** set exact chart designs,
> report layouts, visual templates, final visualization choices, final presentation format, or concrete
> implementation mechanism — those decisions remain open by design.

---

> **Conformance:** This document inherits and respects the scope boundaries, non-goals, priorities,
> budget philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md), and
> builds on [`DATA_SPEC.md`](DATA_SPEC.md), [`MODELING_SPEC.md`](MODELING_SPEC.md), and
> [`EVALUATION_SPEC.md`](EVALUATION_SPEC.md). It introduces no new project requirements beyond
> explainability-layer rules.
