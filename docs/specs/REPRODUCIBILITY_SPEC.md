# StatSport — Reproducibility Specification

**Reproducibility strategy specification**

> _How StatSport stays re-creatable by another person — from repository contents and documented steps — without hidden knowledge or the original author._

| | |
|---|---|
| **Status** | Specification Phase |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Downstream specification (conforms to all existing specifications) |
| **Parents** | [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](DATA_SPEC.md) · [`MODELING_SPEC.md`](MODELING_SPEC.md) · [`EVALUATION_SPEC.md`](EVALUATION_SPEC.md) · [`EXPLAINABILITY_SPEC.md`](EXPLAINABILITY_SPEC.md) |

> **What this document is:** the reproducibility strategy for StatSport. It defines how the project
> remains reproducible, reviewable, maintainable, and re-creatable by another person — without
> selecting final environment setup, dependency lists, workflow implementation, artifact-generation
> mechanisms, or automation approach. It conforms to all existing specifications.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total.
> **Inherited rules of thumb:** reproducibility is a first-class requirement; simplicity is preferred
> over infrastructure; a future reviewer should be able to recreate the project from repository
> contents and documented acquisition steps.

---

## 1. Purpose of the Reproducibility Layer

The reproducibility layer ensures that **anyone** — a portfolio reviewer, an admissions reader, or a
future version of the author — can **recreate StatSport's results** from the repository and its
documentation alone. Its job is to make the project **self-contained and trustworthy**, so results
are verifiable rather than taken on faith.

Concretely, the reproducibility layer must:

- Make the repository and its documentation **sufficient** to recreate the work.
- Ensure data, modelling, evaluation, and explanation workflows are **documented and repeatable**.
- Eliminate **hidden knowledge** and **undocumented manual steps**.
- Stay **laptop-friendly** and **simple**, within the 40–60 hour budget.

---

## 2. Reproducibility Philosophy

StatSport's reproducibility is governed by these principles:

- **Reproducibility is mandatory** — it is a first-class requirement across every layer.
- **Hidden knowledge is unacceptable** — nothing required to recreate the work lives only in the
  author's head.
- **Manual undocumented steps are unacceptable** — any required manual action is written down.
- **Repository contents and documentation should be sufficient** — they are the complete recipe.
- **Simplicity is preferred over infrastructure complexity** — the least machinery that achieves
  reproducibility wins.

When these principles conflict, the inherited priority order and the time budget decide.

---

## 3. Reproducibility Objectives

- A reviewer can **recreate the project** from repository contents and documented acquisition steps.
- Every layer's workflow (**data → modelling → evaluation → explainability**) is **documented and
  repeatable**.
- Results, figures, and reports are **traceable** back to data and code.
- The project remains **laptop-friendly**, with no cloud, GPU, or paid-infrastructure dependency.
- Reproducibility is achieved with **minimal tooling**, consistent with the budget.

---

## 4. Repository-First Principle

- **The repository is the source of truth** — the canonical record of the project.
- **Documentation must explain how to recreate results** — acquisition, processing, modelling,
  evaluation, and explanation are all described.
- **Future reviewers should not depend on the original author** — no need to contact André, access
  private notes, or rely on undocumented context.
- Anything required to reproduce the work is **either in the repository or fully documented within it**
  (raw data itself may live outside version control, but its acquisition is documented — see §6).

---

## 5. Environment Reproducibility Requirements

- **Laptop-friendly** — the project runs on a typical personal computer.
- **No cloud dependency** — nothing requires hosted services to reproduce.
- **No specialized hardware dependency** — standard consumer hardware suffices.
- **No GPU dependency** — consistent with the modelling spec's exclusion of GPU-dependent workflows.
- **No paid infrastructure dependency** — reproduction requires no paid services.
- The environment must be **describable plainly enough** for another person to recreate it; the
  *concrete* environment setup and dependency list are **deferred** (see §15).

### Cross-Platform Reproducibility Requirements

The project must remain reproducible across the two environments in active use — the project's macOS
environment and André's Windows 11 environment:

- The repository must remain **reproducible on macOS and on Windows 11**.
- Documentation should **avoid unnecessary operating-system-specific assumptions** whenever practical.
- Workflows should remain **cross-platform whenever reasonably achievable** within the project's
  40–60 hour scope.
- When platform-specific instructions are unavoidable, documentation should provide guidance for
  **both macOS and Windows 11**.
- The project should **avoid introducing tooling that unnecessarily prevents reproduction** on either
  platform.
- **Cross-platform compatibility is a reproducibility objective, not a product feature** — it serves
  recreation by another person, consistent with the repository-first principle, and does not expand
  the project's scope or non-goals.

> The *concrete* environment setup, dependency list, and any platform-specific steps remain
> **deferred** (see §15); this subsection sets the cross-platform requirement, not its implementation.

---

## 6. Data Reproducibility Requirements

Consistent with [`DATA_SPEC.md`](DATA_SPEC.md):

- **Data acquisition must be documented** — how to obtain the data, reproducibly.
- **Data provenance must be documented** — source, license, scope, and acquisition date.
- **Data transformations must be documented** — how raw becomes processed, repeatably.
- **Raw data itself may remain outside version control** if licensing or size requires it; what is
  distributed is the **documented process**, not the data (consistent with the repository
  `.gitignore`, which ignores `data/` contents while preserving `.gitkeep` markers).
- Given the documented steps, the data state is **regenerable** by another person.

---

## 7. Modelling Reproducibility Requirements

Consistent with [`MODELING_SPEC.md`](MODELING_SPEC.md):

- **Training workflow must be documented** — the path from processed data to model is written down.
- **Randomness control should be documented where applicable** — e.g., fixed seeds so runs repeat.
- **Model generation should be repeatable** — the same inputs and configuration yield the same model.
- Large model artifacts are **regenerable** and **not committed**, consistent with `DATA_SPEC.md` and
  the repository `.gitignore`.

---

## 8. Evaluation Reproducibility Requirements

Consistent with [`EVALUATION_SPEC.md`](EVALUATION_SPEC.md):

- **Evaluation workflow must be documented** — how results are produced is recorded.
- **Validation procedure must be reproducible** — splits/procedures repeat for anyone.
- **Reported results must be traceable** — each reported number can be tied back to the data, model,
  and procedure that produced it (including baseline comparisons).

---

## 9. Explainability Reproducibility Requirements

Consistent with [`EXPLAINABILITY_SPEC.md`](EXPLAINABILITY_SPEC.md):

- **Explanations must be regenerable** — the same inputs and configuration reproduce the same
  explanations.
- **Explanation workflow must be documented** — how explanations are produced is recorded.
- **Explanation outputs must be traceable to model and data** — they reference the evaluated model and
  reproducible features, not ad-hoc constructs.

---

## 10. Documentation Requirements

The repository documentation must make recreation possible:

- **README expectations** — a clear entry point describing what the project is and how to recreate it
  at a high level, linking to the specs.
- **Spec expectations** — the `docs/specs/` set remains the authoritative description of intent and
  rules; downstream work conforms to it.
- **Provenance expectations** — data source, license, scope, and acquisition are recorded
  (per `DATA_SPEC.md`).
- **Assumption documentation** — non-obvious assumptions, decisions, and limitations are written down
  rather than left implicit.

> The exact structure, location, and depth of this documentation are **deferred** (see §15).

---

## 11. Artifact Reproducibility Requirements

- **Figures should be regenerable** — produced from documented steps, not hand-edited.
- **Reports should be regenerable** — derived from the documented workflow.
- **Outputs should be traceable** — every artifact under `outputs/` can be tied to the data, model,
  and procedure that produced it.
- Generated artifacts are **not committed** when large/regenerable, consistent with the repository
  `.gitignore` (which ignores `outputs/` contents while preserving `.gitkeep` markers).

---

## 12. Reviewer Recreation Requirements

- **A technically literate reviewer should be able to recreate the project** using only repository
  contents and documented acquisition steps.
- **A future version of André should be able to recreate the project** without relying on memory or
  private context.
- **No private tribal knowledge** — nothing essential exists only outside the repository.
- Recreation should be achievable on a **typical laptop**, within reasonable effort consistent with
  the project's simplicity and budget.

---

## 13. Reproducibility Exclusions

To keep reproducibility **simple and budget-safe**, the project will **not** require:

- **Enterprise MLOps** — no production ML platforms or pipelines.
- **Deployment infrastructure** — no serving, hosting, or runtime environment.
- **CI/CD requirements** — no continuous integration/deployment is mandated for reproducibility.
- **Cloud reproducibility platform** — no hosted reproduction service.
- **Experiment-tracking platform dependency** — no required external tracking service.

These exclusions are consistent with the overview's non-goals (no large-scale MLOps, no deployment).

---

## 14. Reproducibility Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Hidden knowledge** | Steps that live only in the author's head | Document everything; repository-first principle (§4). |
| **Undocumented manual steps** | Silent manual actions break recreation | Record every required manual action (§2). |
| **Environment drift** | Results depend on an unspecified environment | Describe a laptop-friendly environment; defer concrete setup (§5, §15). |
| **Data unavailability** | Source data changes or disappears | Document provenance and acquisition date (§6). |
| **Non-deterministic runs** | Uncontrolled randomness | Document randomness control where applicable (§7). |
| **Untraceable results** | Reported numbers can't be tied to a procedure | Require traceability across layers (§8–§11). |
| **Infrastructure creep** | Reaching for MLOps/cloud/CI tooling | Honor exclusions (§13); prefer simplicity. |
| **Budget overrun** | Reproducibility effort grows too large | Keep tooling minimal; defer extras (§15). |

---

## 15. Deferred Reproducibility Decisions

The following are intentionally **not** decided here and remain deferred:

| Deferred decision | Status / owning step |
|-------------------|----------------------|
| **Final environment setup details** | Deferred. |
| **Final dependency list** | Deferred. |
| **Final workflow implementation** | Deferred. |
| **Final artifact-generation mechanism** | Deferred. |
| **Final automation approach** | Deferred. |
| Concrete implementation mechanism (script vs. notebook vs. both) | Deferred (overview allows either or both). |
| Exact documentation structure/location | Deferred (see §10). |

> This specification establishes the **rules and philosophy** for reproducibility. It deliberately
> does **not** fix the environment setup, dependency list, workflow implementation,
> artifact-generation mechanism, or automation approach — those decisions remain open by design.

---

> **Conformance:** This document inherits and respects the scope boundaries, non-goals, priorities,
> budget philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md), and
> builds on [`DATA_SPEC.md`](DATA_SPEC.md), [`MODELING_SPEC.md`](MODELING_SPEC.md),
> [`EVALUATION_SPEC.md`](EVALUATION_SPEC.md), and [`EXPLAINABILITY_SPEC.md`](EXPLAINABILITY_SPEC.md).
> It introduces no new project requirements beyond reproducibility-layer rules.
