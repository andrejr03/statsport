# StatSport — AI-Powered Football Analytics and Prediction

**Project specification — anchor document**

> _Turning historical football data into explainable analytics and defensible match predictions._

| | |
|---|---|
| **Status** | Specification Phase |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Top-level project specification (the anchor document all later specs conform to) |

> **What this document is:** the authoritative overview of StatSport — its purpose, scope,
> boundaries, and the decisions deliberately deferred to later specifications. It is written at
> *overview altitude*: it states *what* the project is and *why*, not *how* it will be implemented.
> Every downstream specification must conform to this document.

---

## Purpose

StatSport exists to demonstrate, end to end, that its author can take real football data and turn it
into **explainable analytics** and **defensible match predictions**. It is a learning artifact and a
portfolio piece: a complete, honest, reproducible workflow from raw data to evaluated, interpretable
results.

It is deliberately **not** a product. There is no business model, no user base to serve, and no
production system to operate. Success is measured by the quality of the demonstrated reasoning and
the clarity of its presentation — not by commercial outcomes.

---

## Portfolio Strategy Alignment

StatSport is **repository 1 of 3** in a focused summer portfolio. The goal is for the author to
complete **three strong, finished GitHub repositories** rather than one sprawling, unfinished one. For
that reason, StatSport must be *finishable* within its budget so that two further high-quality AI
projects can follow.

The signals this repository is intended to send to a reviewer:

- **Data competence** — sourcing, cleaning, and reasoning about real-world, imperfect data.
- **ML judgment** — choosing appropriate, interpretable methods and justifying them.
- **Evaluation rigor** — comparing against baselines and reporting results honestly.
- **Communication** — a clear README, readable figures, and a coherent narrative.
- **Discipline** — a project that is scoped, completed, and presented, not abandoned mid-stream.

> The other two portfolio projects are out of scope for this document and are referenced only to
> explain why StatSport is intentionally bounded.

---

## Time Budget Philosophy

StatSport is constrained to a **total effort budget of 40–60 hours**. This constraint is a
first-class design input, not an afterthought: it shapes the scope, the goals, and especially the
non-goals.

An indicative (non-binding) allocation, to show the budget is realistic:

| Phase | Rough share of budget |
|-------|-----------------------|
| Specification & research | ~10–15% |
| Data acquisition & preparation | ~20–25% |
| Modelling (baseline + selected model) | ~20–25% |
| Evaluation & explainability | ~20–25% |
| Presentation (README, figures, report) | ~15–20% |

**Governing rule:** if a task threatens the 40–60 hour budget, it does not get quietly absorbed — it
moves to **Non-Goals**, to **Scope Boundaries**, or to a **later specification**. The test every
addition must pass is: *does this fit within 40–60 hours and still leave room for two more projects?*

---

## Problem Statement

Given historical football data — match results and team/season-level statistics — StatSport sets out
to **characterize team performance** and **predict a well-defined match outcome**. The problem is
framed to be tractable and well-bounded: a portfolio-sized prediction-and-analytics task, not an
open-ended research programme.

The project treats this as a two-part problem: a **descriptive** part (understanding and summarizing
performance through exploratory analysis) and a **predictive** part (forecasting a clearly defined
outcome and explaining the forecast).

> The *exact* prediction target — the specific label, league, and seasons — is named here only as a
> candidate. Locking it in is a **deferred decision** (see below), to be settled in the data and
> modelling specifications.

---

## Target Audience

The people who will **read and evaluate** this repository:

- **Portfolio reviewers** assessing breadth, depth, and finish.
- **Technical reviewers** assessing analytical maturity.
- **GitHub readers** skimming for evidence of competence.
- **The author's future self**, returning to extend or explain the work.

Each of these readers wants to understand the project quickly, trust its claims, and see honest,
well-communicated results.

---

## Target Users

The illustrative personas who would *use* such analytics and predictions, used here only to frame the
work — there is no real production user base:

- A **football enthusiast** curious about data-driven views of matches.
- An **amateur analyst** exploring whether outcomes can be modelled.
- A **student** learning how sports data and machine learning fit together.

> These personas motivate design choices (clarity, interpretability). They do not imply any
> delivered application, UX flows, or user-acceptance commitments.

---

## Goals

1. Acquire and clean a chosen, openly usable football dataset into a reproducible processed form.
2. Perform exploratory analysis that meaningfully characterizes team/match performance.
3. Engineer a sensible, defensible set of features from the data.
4. Build a **baseline model and a selected model**, with the baseline as the reference.
5. Produce **explainable outputs** so a reader can understand *why* a prediction was made.
6. Evaluate honestly against the baseline using appropriate, clearly justified methods.
7. Ship a polished presentation layer: a clear `README.md`, readable figures, and a short report.

Every goal is intended to be achievable within the 40–60 hour budget.

---

## Non-Goals

StatSport explicitly will **not**:

- **StatSport is NOT a SaaS product.**
- **StatSport is NOT a commercial football platform.**
- **StatSport is NOT a live prediction service.**
- **StatSport is NOT a large-scale MLOps system.**
- Deploy any model or expose any hosted endpoint.
- Ingest real-time or streaming data feeds.
- Ship a front-end application or interactive dashboard.
- Function as a betting, odds, or gambling product.
- Attempt broad multi-league, multi-season "mega-dataset" coverage.
- Pursue maximal predictive accuracy through exhaustive tuning or deep-learning rabbit holes.

---

## Scope Boundaries

| Dimension | In scope | Out of scope |
|-----------|----------|--------------|
| **Data breadth** | A focused, laptop-friendly dataset (a bounded league/seasons) | Many leagues, exhaustive historical archives, live feeds |
| **Modelling depth** | One baseline + one selected, interpretable model | Large model zoos, heavy ensembling, deep-learning exploration |
| **Evaluation depth** | Honest comparison vs. baseline with a small, justified method set | Exhaustive metric sweeps, leaderboard chasing |
| **Explainability** | First-class, reader-facing interpretation of predictions | Bespoke interpretability research |
| **Presentation** | README, figures, short written report | Web app, hosted demo, marketing site |

All boundaries trace back to the 40–60 hour budget: depth is preferred over breadth, and finish is
preferred over feature count.

---

## High-Level Capabilities

The finished repository will demonstrate the following capabilities (described as capabilities, not
modules or libraries):

- **Data ingestion & cleaning** — turning raw football data into a reproducible processed form.
- **Exploratory analysis** — summarizing and visualizing performance patterns.
- **Feature engineering** — deriving informative inputs from the cleaned data.
- **Baseline modelling** — a simple, honest reference point.
- **Selected-model development** — an interpretable model that improves on the baseline.
- **Evaluation** — measuring performance honestly and comparatively.
- **Explainability** — communicating *why* predictions are made.
- **Presentation** — a clear narrative through README, figures, and a short report.

---

## High-Level Architecture Overview

At a conceptual level, StatSport is a linear analytics-and-prediction flow. No orchestration,
service, or deployment layer is implied.

```
raw data ──▶ processed data ──▶ features ──▶ model(s) ──▶ evaluation + explainability ──▶ outputs
 (data/raw)   (data/processed)               (src/)                                       (outputs/)
```

This flow maps conceptually onto the existing repository folders: source data lives under `data/`,
analysis and modelling logic under `src/` (with exploratory work in `notebooks/` and/or `scripts/`), and generated
artifacts (figures, reports) under `outputs/`. Detailed component design, interfaces, and file
formats are intentionally **not** specified here — they belong to later specifications.

---

## Expected Data Domains

The kinds of football data anticipated (named as domains, not specific sources):

- **Match results** — outcomes of historical fixtures.
- **Team / season statistics** — aggregate performance measures.
- **Fixtures / schedule data** — to frame matches and ordering.
- **(Possibly) player-level statistics** — only if it fits the budget.

Constraints on the data: it must be **openly and legally usable**, **small-to-medium** and
laptop-friendly, and handled so that **raw data stays out of version control** (consistent with the
repository's `.gitignore`).

> Specific dataset names, sources, and URLs are **not** chosen here. Dataset selection is a
> **deferred decision**.

---

## Expected ML and Analytics Domains

The families of techniques expected to be in play (named as domains, not specific algorithms):

- **Descriptive analytics / exploratory data analysis** — understanding the data before modelling.
- **Classical supervised learning** — classification and/or regression for the prediction target.
- **Baseline methods** — a deliberately simple reference for honest comparison.

Given the explainability priority, **interpretable model families are preferred** over opaque,
high-complexity approaches.

> Specific algorithms, hyperparameters, and frameworks are **not** chosen here. Algorithm selection
> is a **deferred decision**.

---

## Explainability Requirements

Explainability is a **first-class requirement**, not an add-on. The intent is that a reader can
understand *why* a given prediction was produced.

- Predictions must be accompanied by interpretation, not presented as bare numbers.
- The chosen modelling approach should lend itself to clear explanation (e.g., understandable feature
  influence or inherently interpretable behavior).
- Explanations must be communicated in reader-facing form (figures and/or narrative), not buried.
- Interpretability should inform model choice, consistent with the project's stated priorities.

> The specific explainability methods or tools are **not** chosen here; they are a **deferred
> decision**, named as candidates only.

---

## Evaluation Philosophy

StatSport judges success by the **honesty and clarity** of its evaluation, not by impressive-looking
numbers.

- **Always compare against a baseline** — improvement is only meaningful relative to a reference.
- **Use appropriate, clearly justified methods** — chosen for the problem, not for show.
- **Prefer a small set of well-justified measures** over many weakly-motivated ones.
- **Avoid data leakage** and other silent sources of over-optimistic results.
- **Acknowledge uncertainty and limitations** openly.

> The final evaluation metrics and validation scheme are **not** chosen here. They are a **deferred
> decision**, to be settled in the evaluation specification.

---

## Deliverables

At completion, the repository is expected to contain:

- [ ] The specification set under `docs/specs/` (beginning with this anchor document).
- [ ] Reproducible data handling producing a processed dataset (the raw/processed data itself remains git-ignored).
- [ ] Exploratory analysis work — notebooks, scripts, or a combination of both (e.g., under `notebooks/` and/or `scripts/`).
- [ ] Analysis and modelling source code under `src/`.
- [ ] Evaluation results comparing the selected model against the baseline.
- [ ] Figures under `outputs/figures/`.
- [ ] A short written report under `outputs/reports/`.
- [ ] A polished `README.md` tying the narrative together.

Each deliverable is scoped to remain within the 40–60 hour budget.

---

## Repository Relationship

This document is the **anchor specification** within `docs/specs/`. It sits above and constrains all
later specifications. It is consistent with the existing repository scaffolding and conventions:

- `assets/` — static assets, including the project showcase image.
- `data/` — raw, processed, and external data (contents git-ignored).
- `docs/` — specifications, research, evidence, reviews, and plans (this document lives in `docs/specs/`).
- `notebooks/` — exploratory analysis.
- `outputs/` — generated figures, reports, and exports (contents git-ignored).
- `src/` — source code for analytics, features, and models.
- `tests/` — automated tests.
- `scripts/` — utility and automation scripts.

The full directory tree is documented in the repository `README.md` and is not duplicated here. This
document is consistent with that `README.md` and with the repository's `.gitignore` (raw data and
generated outputs are excluded from version control).

---

## Future Specification Dependencies

This overview will spawn the following downstream specifications, in dependency order. Each must
conform to this anchor document:

1. **`DATA_SPEC.md`** — defines the chosen dataset(s), acquisition, and processed data handling.
2. **`MODELING_SPEC.md`** — defines the baseline, the selected model, and feature decisions.
3. **`EVALUATION_SPEC.md`** — defines metrics, validation scheme, and baseline comparison.
4. **`EXPLAINABILITY_SPEC.md`** — defines the interpretation methods and how they are presented.
5. **Presentation / report specification** — defines the final README, figures, and written report.

> Only the name, purpose, and ordering of these specs are stated here. Their contents are out of
> scope for this document.

---

## Scope-Creep Risks

Tempting expansions that would jeopardize the 40–60 hour budget, with mitigations:

| Risk | Mitigation |
|------|------------|
| Chasing many leagues / seasons | Fix a single bounded dataset; park the rest in Non-Goals. |
| Adding live / streaming data ingestion | Out of scope; historical data only. |
| Deep-learning rabbit holes | Prefer interpretable classical methods; defer DL to "future work". |
| Building a web app or dashboard | Out of scope; presentation is README + figures + report. |
| Over-tuning for marginal accuracy | Stop at a defensible, well-explained result vs. baseline. |
| Deployment / MLOps tooling | Explicit Non-Goal; no serving, monitoring, or pipelines. |
| Excessive feature engineering | Keep a focused, justified feature set within budget. |

---

## Deferred Decisions

Decisions intentionally **not** made in this overview, each routed to the specification that will own
it:

| Deferred decision | Owning specification |
|-------------------|----------------------|
| Final dataset(s) and source | `DATA_SPEC.md` |
| Exact prediction target / label | `DATA_SPEC.md` → `MODELING_SPEC.md` |
| Specific algorithms and baseline method | `MODELING_SPEC.md` |
| Evaluation metrics and validation scheme | `EVALUATION_SPEC.md` |
| Explainability methods and tools | `EXPLAINABILITY_SPEC.md` |
| Presentation / report format | Presentation / report specification |

These remain open by design. This document does not attempt to settle them.

---

## Open Questions

A parking lot of questions to resolve while authoring the downstream specifications (not answered
here):

- Which league and seasons are realistically obtainable under an open, usable license?
- Is the prediction framed as classification (e.g., outcome category) or regression?
- What is the simplest credible baseline for this target?
- Is player-level data worth including given the budget, or does it belong in "future work"?

---

> **Priorities (in order), reaffirmed:** **1. Portfolio value · 2. Reproducibility ·
> 3. Explainability · 4. Evaluation quality · 5. Presentation clarity** — these take precedence over
> engineering breadth throughout the project.
