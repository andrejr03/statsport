# StatSport — `PROJECT_OVERVIEW.md` Documentation Plan

> **What this is:** A planning document that defines the structure, scope, and required
> content of the future `PROJECT_OVERVIEW.md` specification. This is **planning only** —
> it does not create the spec itself, code, datasets, or notebooks.

**Plan author context:** University-level AI portfolio project for André.
**Plan status:** Draft for review.
**Date:** 2026-06-20.

---

## 1. Target Spec Identity

| Field | Value |
|-------|-------|
| **Suggested final spec file name** | `PROJECT_OVERVIEW.md` |
| **Suggested final spec location** | `docs/specs/PROJECT_OVERVIEW.md` |
| **Document type** | Top-level project specification (the anchor doc all later specs reference) |
| **Owner** | André |
| **Phase** | Specification Phase |
| **Audience for the spec** | André (author), portfolio reviewers, Passau admissions/faculty readers, future-self maintainer |

---

## 2. Planning Principles & Guardrails

These constraints MUST be reflected verbatim (in spirit) inside the future `PROJECT_OVERVIEW.md`.

### 2.1 What StatSport is NOT
The spec must state explicitly and prominently that StatSport is:
- **NOT a SaaS product.**
- **NOT a commercial football platform.**
- **NOT a live / real-time prediction service.**
- **NOT a large-scale MLOps system.**

It is a **self-contained, reproducible, university-level AI portfolio project** demonstrating a
complete analytics-and-prediction workflow on football data.

### 2.2 What the project prioritizes
The spec must state that StatSport prioritizes — in this order — over engineering breadth:
1. **Portfolio value** (a reviewer can quickly see competence)
2. **Reproducibility** (anyone can re-run it and get the same result)
3. **Explainability** (model decisions are interpretable, not black-box)
4. **Evaluation quality** (honest, well-chosen metrics and baselines)
5. **Presentation clarity** (clean README, figures, and narrative)

> Engineering breadth (microservices, pipelines, deployment, scaling) is explicitly *de-prioritized*.

### 2.3 Time budget
- The project is scoped to **40–60 hours total**.
- Reason: André must complete **two additional serious AI projects** over the summer, arriving at
  Passau with **three strong GitHub portfolio repositories**.
- Every section of the spec must respect this budget; anything that threatens it belongs in
  **Non-Goals**, **Scope Boundaries**, or **Deferred Decisions**.

### 2.4 Authoring constraints carried into the spec
The future `PROJECT_OVERVIEW.md` must remain at **overview altitude**. It must NOT:
- Select final datasets (name candidates/domains only).
- Select final algorithms (name families/domains only).
- Define detailed architecture (component diagram + data flow at a high level only).
- Define schemas, APIs, or file formats (those belong to later specs).

---

## 3. Content Coverage Map

This proves the 20 required planning elements are all placed in the spec outline.

| # | Required element | Spec section that carries it |
|---|------------------|------------------------------|
| 1 | Purpose of the project | §B Purpose |
| 2 | Portfolio strategy alignment | §C Portfolio Strategy Alignment |
| 3 | 40–60 hour time budget | §D Time Budget & Effort Strategy |
| 4 | Problem statement | §E Problem Statement |
| 5 | Target audience | §F Target Audience |
| 6 | Target users | §G Target Users |
| 7 | Project goals | §H Goals |
| 8 | Non-goals | §I Non-Goals |
| 9 | Scope boundaries | §J Scope Boundaries |
| 10 | High-level capabilities | §K High-Level Capabilities |
| 11 | High-level architecture overview | §L High-Level Architecture Overview |
| 12 | Expected data domains | §M Expected Data Domains |
| 13 | Expected ML/analytics domains | §N Expected ML & Analytics Domains |
| 14 | Explainability requirements | §O Explainability Requirements |
| 15 | Evaluation philosophy | §P Evaluation Philosophy |
| 16 | Deliverables | §Q Deliverables |
| 17 | Repository relationship | §R Repository Relationship |
| 18 | Future specification dependencies | §S Future Specification Dependencies |
| 19 | Scope-creep risks | §T Scope-Creep Risks |
| 20 | Explicit decisions deferred to later specs | §U Deferred Decisions |

---

## 4. Detailed Section-by-Section Outline for `PROJECT_OVERVIEW.md`

Each entry below specifies: **what the section must contain**, **target length**, and
**what to deliberately leave out**. The spec author should write prose + light bullets, not code.

### §A — Title & Document Metadata
- **Content:** Title (`StatSport — AI-Powered Football Analytics and Prediction`), one-line tagline,
  status (`Specification Phase`), version (`0.1 / draft`), author (André), date, and a 1-line
  "what this document is" statement.
- **Length:** ~8–12 lines (a small metadata block + tagline).
- **Leave out:** Changelog tables, approval signatures.

### §B — Purpose *(covers #1)*
- **Content:** 2–4 sentences on *why this project exists*: to demonstrate, end-to-end, that André
  can take football data and produce explainable analytics and defensible match predictions. State
  that it is a learning + portfolio artifact, not a product.
- **Length:** 1 short paragraph.
- **Leave out:** Feature lists (they live in §K), business/monetization framing.

### §C — Portfolio Strategy Alignment *(covers #2)*
- **Content:** Position StatSport as **repo 1 of 3** in André's summer portfolio. Explain the
  intended signal to Passau reviewers (data handling, ML reasoning, evaluation rigor, communication).
  State the "three strong GitHub repositories" goal and how StatSport must be *finishable* so the
  other two projects can happen.
- **Length:** 1 paragraph + a short bullet list of "signals this repo should send".
- **Leave out:** Details of the other two projects (out of scope; one sentence reference max).

### §D — Time Budget & Effort Strategy *(covers #3)*
- **Content:** State the **40–60 hour** total budget. Provide an *indicative, non-binding* phase
  allocation (e.g., spec & research / data prep / modelling / evaluation & explainability /
  presentation) as rough percentage bands — to show the budget is realistic. Add the rule: "if a
  task threatens the budget, it moves to Non-Goals or a later spec."
- **Length:** 1 paragraph + a small allocation table (phase → rough hour band).
- **Leave out:** A day-by-day schedule, sprint plans, or task-level estimates.

### §E — Problem Statement *(covers #4)*
- **Content:** Define the analytical/predictive problem in plain language: e.g., "given historical
  match and team data, characterize performance and predict a well-defined match outcome." Frame it
  as a tractable, well-bounded prediction + analytics problem suitable for a portfolio.
- **Length:** 1–2 paragraphs.
- **Leave out:** The *final* prediction target definition (e.g., exact label, league, season) — name
  it as a candidate and defer the lock-in to a later spec (§U).

### §F — Target Audience *(covers #5)*
- **Content:** Who *reads/evaluates* the repo: portfolio reviewers, Passau faculty/admissions,
  recruiters, and André's future self. Describe what each wants to see.
- **Length:** Short bullet list (3–5 items).
- **Leave out:** End-user personas (those are §G).

### §G — Target Users *(covers #6)*
- **Content:** Who would *use the analytics/predictions* in a hypothetical sense: e.g., a football
  enthusiast, an amateur analyst, a student exploring sports data. Make clear these are illustrative
  personas to frame the work — there is no production user base.
- **Length:** Short bullet list (2–4 personas), 1 clarifying sentence that usage is illustrative.
- **Leave out:** UX flows, user stories, acceptance criteria.

### §H — Goals *(covers #7)*
- **Content:** 4–7 concrete, checkable project goals (e.g., "ingest and clean a chosen football
  dataset", "build at least one baseline + one main model", "produce explainable outputs", "report
  honest evaluation against a baseline", "ship a clear README + figures"). Each goal must be
  achievable within the time budget.
- **Length:** Numbered list, one line each.
- **Leave out:** Stretch goals (those become Non-Goals or Deferred).

### §I — Non-Goals *(covers #8)*
- **Content:** Explicit list of what the project will NOT do. MUST include the §2.1 NOT-statements
  (no SaaS, no commercial platform, no live prediction service, no large-scale MLOps) plus practical
  exclusions (no deployment, no real-time data feeds, no front-end app, no betting/odds product,
  no multi-league mega-dataset).
- **Length:** Bullet list (6–10 items).
- **Leave out:** Nothing — this section is where exclusions belong; be generous.

### §J — Scope Boundaries *(covers #9)*
- **Content:** Draw the in/out line crisply. A two-column "In scope / Out of scope" table covering
  data breadth, modelling depth, evaluation depth, explainability, and presentation. Tie boundaries
  back to the 40–60h budget.
- **Length:** One table + 1–2 framing sentences.
- **Leave out:** Final technical choices; keep boundaries at capability level.

### §K — High-Level Capabilities *(covers #10)*
- **Content:** The capabilities the finished repo will demonstrate, e.g.: data ingestion & cleaning,
  exploratory analysis, feature engineering, baseline + primary model, evaluation, explainability,
  and a presentation layer (README/figures/short report). Phrase as capabilities, not modules.
- **Length:** Bullet list (6–9 capabilities), one line each.
- **Leave out:** Library names, function/module design, file layout.

### §L — High-Level Architecture Overview *(covers #11)*
- **Content:** A *conceptual* data-flow description: raw data → processed data → features →
  model(s) → evaluation + explainability → outputs (figures/reports). Reference the existing repo
  folders (`data/`, `src/`, `notebooks/`, `outputs/`) at a conceptual level. A simple ASCII/mermaid
  flow is acceptable.
- **Length:** 1 paragraph + 1 simple diagram.
- **Leave out:** Class/module design, interfaces, config formats, orchestration tooling.

### §M — Expected Data Domains *(covers #12)*
- **Content:** Name the *kinds* of football data likely needed (e.g., match results, team/season
  stats, possibly player-level stats, fixtures). State expectations on size (small/medium,
  laptop-friendly), licensing (must be openly usable), and that raw data stays out of git
  (consistent with `.gitignore`).
- **Length:** Bullet list of candidate domains + 2–3 sentences of constraints.
- **Leave out:** Specific dataset names/sources/URLs — selection is **deferred** (§U).

### §N — Expected ML & Analytics Domains *(covers #13)*
- **Content:** Name the *families* of techniques in play: descriptive analytics/EDA, classical
  supervised learning (classification and/or regression), and a strong baseline for comparison.
  Note a preference for interpretable model families given the explainability priority.
- **Length:** Bullet list of domains + 1–2 framing sentences.
- **Leave out:** Specific algorithms, hyperparameters, frameworks — selection is **deferred** (§U).

### §O — Explainability Requirements *(covers #14)*
- **Content:** State that explainability is a first-class requirement, not an add-on. Define the
  *intent*: outputs must let a reader understand *why* a prediction was made (e.g., feature
  importance / interpretable model behavior / clear narrative around predictions). Tie to the
  portfolio priority on explainability.
- **Length:** 1 paragraph + 2–4 requirement bullets.
- **Leave out:** Specific explainability libraries/methods (name as candidates, defer the choice).

### §P — Evaluation Philosophy *(covers #15)*
- **Content:** Describe *how success is judged*: always compare against a baseline, use honest and
  appropriate metrics, acknowledge uncertainty/limits, avoid leakage, and prefer a small set of
  well-justified metrics over many. Emphasize honesty over impressive-looking numbers.
- **Length:** 1 paragraph + 3–5 principle bullets.
- **Leave out:** The final metric set and validation scheme (defer to an evaluation spec, §S/§U).

### §Q — Deliverables *(covers #16)*
- **Content:** Enumerate concrete artifacts the repo will contain at completion: the spec set under
  `docs/specs/`, cleaned/processed data handling (not the data itself), analysis notebook(s),
  source modules under `src/`, evaluation results, figures under `outputs/figures/`, a short written
  report under `outputs/reports/`, and a polished `README.md`. Mark each as in-budget.
- **Length:** Checklist-style bullet list.
- **Leave out:** Detailed file names/APIs; keep to deliverable level.

### §R — Repository Relationship *(covers #17)*
- **Content:** Explain how this spec relates to the existing scaffolding: it is the anchor document
  in `docs/specs/`; map how the repo folders (`data/`, `docs/`, `notebooks/`, `outputs/`, `src/`,
  `tests/`, `scripts/`, `assets/`) support the project. Confirm consistency with the current
  `README.md` and `.gitignore` (raw data and outputs are git-ignored).
- **Length:** 1 paragraph + a short folder→role mapping (can reference README to avoid duplication).
- **Leave out:** Re-documenting the full tree (link to README instead).

### §S — Future Specification Dependencies *(covers #18)*
- **Content:** List the downstream specs this overview will spawn and their dependency order, e.g.:
  `DATA_SPEC.md` → `MODELING_SPEC.md` → `EVALUATION_SPEC.md` → `EXPLAINABILITY_SPEC.md` →
  `PRESENTATION/REPORT spec`. State that `PROJECT_OVERVIEW.md` is the parent each must conform to.
- **Length:** Ordered list with a 1-line purpose per downstream spec.
- **Leave out:** The contents of those specs (only name + purpose + order here).

### §T — Scope-Creep Risks *(covers #19)*
- **Content:** A risk register of tempting expansions that would blow the 40–60h budget, each with a
  mitigation. Candidates: chasing many leagues/seasons; live data ingestion; deep-learning
  rabbit holes; building a web app/dashboard; over-tuning; deployment/MLOps; excessive feature
  engineering. Mitigation = "park in Non-Goals / later spec / future work."
- **Length:** Two-column table (Risk → Mitigation), 6–9 rows.
- **Leave out:** Nothing — be candid; this protects the timeline.

### §U — Deferred Decisions *(covers #20)*
- **Content:** Explicit register of decisions intentionally NOT made in this overview, each routed
  to the spec that will own it: final dataset(s) & source (→ DATA_SPEC), exact prediction target/
  label (→ DATA/MODELING), specific algorithms & baseline (→ MODELING_SPEC), evaluation metrics &
  validation scheme (→ EVALUATION_SPEC), explainability methods/tools (→ EXPLAINABILITY_SPEC),
  presentation/report format (→ presentation spec).
- **Length:** Two-column table (Decision → Owning spec).
- **Leave out:** Any attempt to actually decide these here.

### §V — Open Questions (optional, recommended)
- **Content:** A short list of questions André should resolve before/while writing downstream specs
  (e.g., which league/season is realistically obtainable for free; classification vs. regression
  target). Keeps unknowns visible without forcing premature decisions.
- **Length:** 3–6 bullets.
- **Leave out:** Answers (this is a parking lot).

---

## 5. Acceptance Criteria for the Future `PROJECT_OVERVIEW.md`

The spec is "done" when:
- [ ] All sections §A–§U are present (coverage of all 20 required elements).
- [ ] The four "NOT" statements (SaaS / commercial platform / live service / large-scale MLOps) appear explicitly.
- [ ] The five priorities (portfolio value, reproducibility, explainability, evaluation quality, presentation clarity) are stated as ranked priorities over engineering breadth.
- [ ] The 40–60 hour budget is stated and reflected in scope, goals, and non-goals.
- [ ] No final dataset, algorithm, metric, or detailed architecture is locked in (all such choices appear in §U Deferred Decisions).
- [ ] The document stays at overview altitude (no schemas, APIs, or code).
- [ ] It is internally consistent with `README.md` and `.gitignore`.
- [ ] It is readable in ~10 minutes by a reviewer with no prior context.

---

## 6. Writing Guidance for the Spec Author

- **Altitude:** Overview only. When tempted to specify "how", stop and route it to §S/§U.
- **Tone:** Clear, honest, portfolio-facing. Short paragraphs + tight bullets/tables.
- **Length target:** ~3–6 pages rendered. Long enough to be credible, short enough to finish.
- **Reuse, don't duplicate:** Reference `README.md` for the folder tree rather than repeating it.
- **Budget discipline:** Every added ambition must pass the test "does this fit in 40–60h *and*
  leave room for two more projects?" If not, it goes to Non-Goals or Deferred.

---

## 7. Validation Checklist for This Plan
- [x] Plan saved at `docs/plans/STATSPORT_PROJECT_OVERVIEW_PLAN.md` (this file).
- [x] Suggested spec name `PROJECT_OVERVIEW.md` and location `docs/specs/PROJECT_OVERVIEW.md` stated.
- [x] Detailed section-by-section outline provided (§A–§V) covering all 20 required elements.
- [x] Explicit "NOT a SaaS / commercial platform / live prediction service / large-scale MLOps" statement included (§2.1, §I).
- [x] Explicit prioritization of portfolio value, reproducibility, explainability, evaluation quality, presentation clarity over engineering breadth (§2.2).
- [x] No spec file, code, dataset, or notebook created by this plan.

---

## 8. Next Natural Step
Review this plan (`STATSPORT_PROJECT_OVERVIEW_PLAN.md`). Once approved, author
`docs/specs/PROJECT_OVERVIEW.md` following the §A–§V outline above.
