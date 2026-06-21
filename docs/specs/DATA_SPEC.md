# StatSport — Data Specification

**Data strategy specification**

> _How StatSport sources, handles, and governs data — without locking in a final dataset._

| | |
|---|---|
| **Status** | Specification Phase |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Downstream specification (conforms to `PROJECT_OVERVIEW.md`) |
| **Parent** | [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) |

> **What this document is:** the data strategy for StatSport. It defines *what kind* of data the
> project will use, *how* it must be handled, and *which decisions are deferred*. The final dataset,
> source, league, and season range are now recorded in **[Selected Dataset Decision](#selected-dataset-decision)**
> below; the remaining data decisions stay deferred. It conforms to the constraints, priorities, scope
> boundaries, and deferred-decision model of the anchor specification.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total. Reproducibility is
> more important than data volume; simplicity is preferred over breadth.

---

## Selected Dataset Decision

> **Status:** Approved. This section converts four previously deferred decisions — final dataset, final
> source, final league, and final season range — into fixed project decisions. It follows the approved
> candidate analysis in
> [`docs/research/DATASET_CANDIDATE_ANALYSIS.md`](../research/DATASET_CANDIDATE_ANALYSIS.md). All other
> data decisions remain deferred (see §18).

| Decision | Selected value |
|----------|----------------|
| **Selected source** | Football-Data.co.uk |
| **Selected league** | Bundesliga (Germany, top division) |
| **Selected season range** | 2020/21 – 2024/25 (five completed seasons) |

### Decision rationale

The Bundesliga slice of Football-Data.co.uk over five completed seasons was selected because it best
satisfies the project's inherited priorities (portfolio value → reproducibility → explainability →
evaluation quality → presentation clarity) within the 40–60 hour budget. Specifically:

- **Bundesliga relevance & Germany/Passau context.** StatSport is a portfolio piece aimed in part at
  University of Passau admissions readers (`PROJECT_OVERVIEW.md`). Choosing Germany's top division
  gives the work a locally resonant, recognizable subject without expanding scope.
- **Explainable match-level features.** Football-Data.co.uk supplies a ready-made home/draw/away
  result label plus interpretable per-match statistics (goals, shots, shots on target, corners, fouls,
  cards). These map directly to plain-language football intuition, supporting the interpretable model
  families in `MODELING_SPEC.md` and the reader-first explanations in `EXPLAINABILITY_SPEC.md`.
- **Reproducibility.** The source distributes small per-season, per-division CSVs via a stable,
  predictable URL scheme, enabling deterministic re-acquisition by another person — consistent with
  `REPRODUCIBILITY_SPEC.md` and §15 of this document. Provenance, license, scope, and acquisition date
  will be recorded at acquisition (§16).
- **Laptop-friendliness.** Five Bundesliga seasons are a handful of tiny CSVs that load and process
  comfortably in memory on a typical laptop, with no scraping pipeline, cloud, or GPU dependency.
- **Fit within the 40–60 hour budget.** Low acquisition and cleaning effort leaves the budget for
  modelling, honest evaluation, and explanation — and for the two further portfolio projects.

A single league and a bounded five-season range keep the scope focused, consistent with the bounded
scope already required by §3–§4 and by `PROJECT_OVERVIEW.md`. This decision changes no non-goal or
scope boundary; it only fixes the previously deferred dataset, source, league, and season range.

> **Full comparison and ranking:** see
> [`docs/research/DATASET_CANDIDATE_ANALYSIS.md`](../research/DATASET_CANDIDATE_ANALYSIS.md).

---

## 1. Purpose of the Data Layer

The data layer provides StatSport with a **small, clean, reproducible** foundation of historical
football data on which exploratory analysis, feature engineering, modelling, evaluation, and
explanation can be built. Its job is to make the rest of the project *possible and trustworthy*, not
to maximize data volume or coverage.

Concretely, the data layer must:

- Supply enough well-understood data to characterize performance and predict a well-defined outcome.
- Be acquirable and re-acquirable by anyone, deterministically.
- Keep raw and processed data out of version control while keeping the *process* fully documented.
- Stay comfortably within the 40–60 hour budget.

---

## 2. Data Philosophy

StatSport's data choices follow a clear set of preferences:

- **Prefer smaller, cleaner datasets over larger, noisier ones.** Quality and clarity beat volume.
- **Prefer openly usable datasets.** Open licensing is a hard preference, not a nicety.
- **Prefer reproducible datasets.** Acquisition must be repeatable by others, deterministically.
- **Prefer laptop-friendly datasets.** Everything must run on a typical laptop without cloud scale.
- **Prefer datasets that support explainability.** Interpretable features beat opaque, exotic signals.

When these preferences conflict, the inherited priority order (portfolio value → reproducibility →
explainability → evaluation quality → presentation clarity) and the time budget decide.

---

## 3. Data Requirements

The chosen data must, at minimum:

- Cover a **bounded scope** (a single competition/league and a limited set of seasons — now fixed as
  the Bundesliga, 2020/21–2024/25, in [Selected Dataset Decision](#selected-dataset-decision)).
- Contain **historical match outcomes** sufficient to define a prediction target.
- Provide **team- and/or season-level statistics** usable as interpretable features.
- Be **static and historical** — no real-time or streaming dependency.
- Be **documented well enough** to understand fields and their meaning.
- Be **acquirable through a reproducible, low-complexity process** (no fragile scraping pipelines).

These are capability-level requirements. Field names, schemas, and formats are **not** defined here.

---

## 4. Acceptable Dataset Characteristics

A dataset is a *candidate* if it is:

- **Static / historical**, not live.
- **Bounded** in league and season breadth (focused, not exhaustive).
- **Small-to-medium** and laptop-friendly.
- **Openly and legally usable** for a public portfolio repository.
- **Reasonably documented**, with understandable fields.
- **Tabular and interpretable**, lending itself to explainable features.
- **Reproducibly obtainable** through a simple, repeatable acquisition step.

---

## 5. Dataset Selection Criteria

A candidate dataset must satisfy **all** of the following to be eligible:

- **Publicly obtainable** — freely accessible without privileged access.
- **Legally usable** — licensing clearly permits use in a public portfolio project.
- **Reasonably documented** — fields and provenance are understandable.
- **Reproducible acquisition** — the same data can be re-obtained deterministically by others.
- **Suitable for a 40–60 hour project** — small enough in scope and effort to fit the budget.

---

## 6. Dataset Exclusion Criteria

A candidate is **disqualified** if it requires any of the following:

- **Real-time feeds** or streaming ingestion.
- **Paid commercial feeds** or subscription data.
- **Proprietary data** that cannot be openly shared or reproduced.
- **Massive multi-league archives** that exceed the project's bounded scope.
- **Complex scraping infrastructure** (fragile, multi-stage, or rate-limited pipelines).
- **Cloud-scale processing** to acquire or prepare.

---

## 7. Candidate Data Domains

The following data domains are *acceptable in principle*. They describe the **kinds** of data in
play, not specific sources:

- **Historical match results** — outcomes of past fixtures.
- **Team statistics** — team-level performance measures.
- **Seasonal performance statistics** — aggregate measures across a season.
- **Fixture information** — scheduling and match framing.
- **Player-level information** — *optional*, included only if it is clearly justified within the
  budget and supports explainability; otherwise deferred to "future work".

---

## 8. Licensing Requirements

- Data must be **openly and legally usable** in a **public** GitHub repository.
- The dataset's **license/terms must be identified and recorded** as part of data documentation.
- If licensing is ambiguous or restrictive, the dataset is **excluded**.
- Because raw data is **not** committed (see §14), the repository distributes the *acquisition process
  and documentation*, not the data itself — this must remain consistent with the source's terms.

---

## 9. Dataset Size Expectations

- **Small-to-medium and laptop-friendly.** It must load and process comfortably in memory on a
  typical laptop.
- **Volume is explicitly not a goal.** Per the philosophy, a smaller clean dataset is preferred over a
  larger noisy one.
- Scope is bounded to a single competition and a limited season range (now fixed as the Bundesliga,
  2020/21–2024/25 — see [Selected Dataset Decision](#selected-dataset-decision)), which naturally keeps
  size modest.
- If a candidate is large enough to require special tooling or cloud-scale processing, it is
  **excluded** (see §6).

---

## 10. Data Quality Expectations

- **Understandable fields** with reasonable documentation of meaning and provenance.
- **Consistent structure** across the chosen scope (e.g., comparable fields across seasons).
- **Manageable missingness** — gaps that can be handled transparently and documented.
- **Coherent outcomes** sufficient to define a clear prediction target.
- **No silent quality compromises** — known issues are documented rather than hidden, consistent with
  the project's commitment to honest evaluation.

Specific cleaning rules and transformations are **not** defined here; they belong to later work.

---

## 11. Raw Data Principles

- **Raw data is immutable.** It is treated as the original source of truth and never edited in place.
- **Raw data lives under `data/raw/`** and is **never committed** to version control.
- **Acquisition is reproducible.** The means of obtaining raw data is documented so it can be
  re-fetched deterministically.
- **Provenance is recorded** — where the raw data came from, its license, and when it was obtained.

---

## 12. Processed Data Principles

- **Processed data is derived, never authored by hand.** It is produced from raw data through a
  documented, repeatable process.
- **Processed data lives under `data/processed/`** and is **not committed** (it is regenerable).
- **Regenerable from raw + documented process** — given the raw data and the documented steps, the
  processed data can be reproduced.
- **Transformations are transparent** and described well enough to be understood and re-run.

> The exact transformation steps, formats, and schemas are **deferred** to later work.

---

## 13. Data Storage Boundaries

- **`data/raw/`** — immutable source data, as obtained. Not committed.
- **`data/processed/`** — cleaned, model-ready data derived from raw. Not committed.
- **`data/external/`** — third-party/reference data, if any. Not committed.
- Data must remain **local and laptop-scale**; no external data stores, databases, or cloud buckets
  are introduced (consistent with the overview's non-goals).
- Generated artifacts (figures, reports, exports) belong under `outputs/`, not `data/`.

---

## 14. Version-Control Boundaries

- **Raw data must not be committed.**
- **Processed data and large generated artifacts must not be committed.**
- Data handling must remain **consistent with the repository `.gitignore`**, which already ignores the
  contents of `data/raw/`, `data/processed/`, `data/external/`, and `outputs/` (while preserving the
  empty-directory `.gitkeep` markers).
- What *is* committed is the **process and documentation** that make the data reproducible — not the
  data itself.

---

## 15. Reproducibility Requirements

Reproducibility outranks data volume. The data layer must ensure that another person can recreate the
data state from scratch:

- **Deterministic acquisition** — the same raw data can be re-obtained from the documented source.
- **Deterministic processing** — the same processed data can be regenerated from raw data via the
  documented steps.
- **Recorded provenance** — source, license, acquisition date, and scope are documented.
- **No hidden manual steps** — any manual action required is written down explicitly.

> The concrete mechanism (script, notebook, or combination) is **deferred**, consistent with the
> overview's allowance for notebooks, scripts, or both.

---

## 16. Data Documentation Requirements

The repository must document, in human-readable form:

- **Source and provenance** of the raw data.
- **License / terms** under which it is used.
- **Scope** actually chosen (league, seasons) once that decision is made downstream.
- **Acquisition steps** — how to obtain the raw data reproducibly.
- **Processing overview** — how raw becomes processed, at a level that supports re-running.
- **Known limitations** — quality issues, gaps, or caveats.

This documentation is what allows raw/processed data to remain un-committed while keeping the project
fully reproducible. Its exact location and format are **deferred**.

---

## 17. Data Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Scope creep via data breadth** | Temptation to add leagues/seasons/sources | Keep scope bounded; excess goes to Non-Goals / future work. |
| **Licensing ambiguity** | Source terms unclear or restrictive | Exclude ambiguous sources; record license before use. |
| **Reproducibility drift** | Source changes or becomes unavailable | Record provenance and acquisition date; prefer stable sources. |
| **Hidden data-quality issues** | Silent gaps or inconsistencies | Document known issues; handle missingness transparently. |
| **Acquisition complexity** | Fragile scraping or heavy pipelines | Exclude sources needing complex scraping/cloud-scale processing. |
| **Accidental commit of data** | Raw/processed data added to git | Rely on `.gitignore`; never force-add data files. |
| **Player-data overreach** | Optional player data inflates scope | Include only if justified within budget; otherwise defer. |

---

## 18. Deferred Data Decisions

The following decisions are intentionally **not** made here and remain deferred:

| Deferred decision | Status / owning step |
|-------------------|----------------------|
| **Final dataset** | ✅ **Decided** — Football-Data.co.uk (Bundesliga), see [Selected Dataset Decision](#selected-dataset-decision). |
| **Final source** | ✅ **Decided** — Football-Data.co.uk, with provenance and license to be recorded at acquisition (§16). |
| **Final league / competition** | ✅ **Decided** — Bundesliga (Germany, top division). |
| **Final season range** | ✅ **Decided** — 2020/21–2024/25 (five completed seasons). |
| Whether to include player-level data | Deferred — only if justified within budget. |
| Concrete acquisition mechanism (script vs. notebook vs. both) | Deferred (overview allows either or both). |
| Processing steps, formats, and schemas | Deferred — out of scope for this document. |
| Exact location/format of data documentation | Deferred. |

> The dataset, source, league, and season range are now **fixed** in
> [Selected Dataset Decision](#selected-dataset-decision). This specification continues to establish the
> **rules** for choosing and handling data, and the remaining decisions above stay open by design.

---

> **Conformance:** This document inherits and respects the scope boundaries, non-goals, priorities,
> budget philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md). It
> introduces no new project requirements beyond data-layer rules.
