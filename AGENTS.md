# AGENTS.md — StatSport Repository Constitution

**Operating rules for André, Codex, and any future AI coding agent working in this repository.**

> **Read this before making any change.** This document is the repository constitution. It tells you
> what StatSport is, what it must never become, and how to work inside it. When in doubt, stop and
> read the relevant specification in [`docs/specs/`](docs/specs) — **the specs are authoritative.**

---

## 1. Repository Mission

StatSport exists to demonstrate, in a finished and honest way:

- **Data competence** — sourcing, cleaning, and reasoning about real football data.
- **Machine-learning competence** — choosing and applying appropriate, interpretable methods.
- **Evaluation rigor** — comparing against a baseline and reporting results honestly.
- **Explainability** — making clear *why* a prediction was produced.
- **Technical communication** — presenting the work so a non-expert reviewer understands it.

Every change to this repository should advance at least one of these and undermine none of them.

---

## 2. Project Summary

StatSport is a **university-level AI portfolio project** that turns historical football data into
**explainable analytics and match predictions**. It is intentionally small, interpretable, and
reproducible. It is a portfolio artifact, **not a product**. The authoritative description is
[`PROJECT_OVERVIEW.md`](docs/specs/PROJECT_OVERVIEW.md).

---

## 3. Portfolio Strategy Context

- StatSport is **one of three** summer portfolio repositories.
- Total project budget: **40–60 hours**.
- **Completion is more important than expansion.**
- **Finishability is a hard constraint** — a finished, smaller project beats an unfinished larger one.

Any work that threatens finishability within budget is out of scope by default and must be deferred to
"future work" or a later specification.

---

## 4. Authority Hierarchy

When sources of guidance disagree, follow this order (highest first):

1. **Existing specifications** (`docs/specs/`) — authoritative.
2. **AGENTS.md** (this document) — repository-wide operating rules.
3. **Developer guide** ([`STATSPORT_DEVELOPER_GUIDE.md`](docs/guides/STATSPORT_DEVELOPER_GUIDE.md)) — how-to guidance.
4. **Implementation artifacts** (code, notebooks, outputs) — the lowest authority.

A higher level always overrides a lower one. This document never overrides a spec; it operationalizes
the specs.

---

## 5. Specification Hierarchy

The specifications are the source of truth, anchored by
[`PROJECT_OVERVIEW.md`](docs/specs/PROJECT_OVERVIEW.md), which all others conform to:

- [`PROJECT_OVERVIEW.md`](docs/specs/PROJECT_OVERVIEW.md) — anchor / scope / priorities.
- [`DATA_SPEC.md`](docs/specs/DATA_SPEC.md) — data strategy.
- [`MODELING_SPEC.md`](docs/specs/MODELING_SPEC.md) — modelling strategy.
- [`EVALUATION_SPEC.md`](docs/specs/EVALUATION_SPEC.md) — evaluation strategy.
- [`EXPLAINABILITY_SPEC.md`](docs/specs/EXPLAINABILITY_SPEC.md) — explainability strategy.
- [`REPRODUCIBILITY_SPEC.md`](docs/specs/REPRODUCIBILITY_SPEC.md) — reproducibility strategy.
- [`PORTFOLIO_HANDOFF_SPEC.md`](docs/specs/PORTFOLIO_HANDOFF_SPEC.md) — portfolio readiness / done.

**If implementation conflicts with the specs, the specs win.** Do not "fix" a spec by writing code
that contradicts it; raise the conflict instead (see §18).

---

## 6. Operating Principles

These principles decide close calls:

- **Finished > ambitious**
- **Explainable > complex**
- **Reproducible > clever**
- **Honest > impressive**
- **Simplicity > infrastructure**

When two options are otherwise comparable, choose the one that better satisfies these, in this spirit
and consistent with the inherited priority order (portfolio value → reproducibility → explainability →
evaluation quality → presentation clarity).

---

## 7. Scope Boundaries

Scope is defined by [`PROJECT_OVERVIEW.md`](docs/specs/PROJECT_OVERVIEW.md) and reinforced here:

- A **bounded** dataset (single competition / limited seasons — specifics deferred), laptop-scale.
- A **baseline + a selected model** from classical, interpretable families.
- **Honest evaluation** against the baseline and **reader-facing explanations**.
- A **reproducible** workflow and a **clear** presentation.

Anything beyond this — broader data, heavier modelling, deployment, dashboards, services — is out of
scope. Depth and finish are preferred over breadth.

---

## 8. Non-Goals

StatSport is explicitly:

- **NOT a SaaS product.**
- **NOT a commercial football platform.**
- **NOT a betting / odds product.**
- **NOT a live prediction service.**
- **NOT a research programme.**
- **NOT a large-scale MLOps project.**

Do not add features, infrastructure, or framing that move the project toward any of these.

---

## 9. Data Rules

Per [`DATA_SPEC.md`](docs/specs/DATA_SPEC.md):

- **Raw data is never committed.** Neither are processed/external data or large outputs — `.gitignore`
  enforces this; never force-add them.
- **Process over data** — commit the documented steps to acquire and process data, not the data.
- **Provenance is required** — record source, license, scope, and acquisition date.
- Data must be **openly/legally usable**, small-to-medium, and reproducibly obtainable.

---

## 10. Modelling Rules

Per [`MODELING_SPEC.md`](docs/specs/MODELING_SPEC.md):

- **Baseline first** — a baseline model is mandatory and is the reference for every claim.
- **Interpretable models preferred** — favor classical, explainable families.
- **Complexity must justify itself** — added complexity is acceptable only for a meaningful,
  demonstrated gain over the baseline.
- No deep-learning-first approaches, large neural nets, foundation models, LLM-based modelling, or
  GPU-dependent workflows.

---

## 11. Evaluation Rules

Per [`EVALUATION_SPEC.md`](docs/specs/EVALUATION_SPEC.md):

- **Compare against the baseline** — improvement must be demonstrated, not assumed.
- **Avoid leakage** — no target/temporal leakage; respect chronological order where relevant.
- **Honest reporting** — report weak or null results truthfully; state uncertainty and limitations.
- Use a small set of appropriate, understandable metrics (the final metrics remain deferred).

---

## 12. Explainability Rules

Per [`EXPLAINABILITY_SPEC.md`](docs/specs/EXPLAINABILITY_SPEC.md):

- **Reader-first explanations** — written for non-experts; minimal jargon.
- **No unexplained predictions** — every prediction is accompanied by reasoning.
- Provide both local (per-prediction) and global (overall behaviour) explanations, and explain
  limitations and uncertainty honestly.

---

## 13. Reproducibility Rules

Per [`REPRODUCIBILITY_SPEC.md`](docs/specs/REPRODUCIBILITY_SPEC.md):

- **No hidden knowledge** — nothing required to recreate the work lives only in someone's head.
- **No undocumented manual steps** — any manual action is written down.
- The **repository + documentation must be sufficient** to recreate results, on a typical laptop, with
  no cloud/GPU/paid-infrastructure dependency.
- Control randomness where applicable; keep results traceable to data and code.

---

## 14. Cross-Platform Requirements

The project must remain reproducible on **both**:

- **macOS**.
- **Windows 11**.

Avoid OS-specific assumptions where practical; use relative paths (no hard-coded `C:\...` or
`/Users/...`); when platform-specific steps are unavoidable, document **both** macOS and Windows 11.
Cross-platform compatibility is a reproducibility objective, not a product feature.

---

## 15. Documentation Requirements

- **Documentation is a first-class artifact** — as important as code.
- **Significant decisions must be documented** — assumptions, scope choices, and trade-offs are
  written down, not left implicit.
- Keep documentation **consistent** with the specs and with itself; the `docs/specs/` set stays
  authoritative.
- Update relevant docs in the **same change** that makes a decision real.

---

## 16. Git Workflow Expectations

Per the [developer guide](docs/guides/STATSPORT_DEVELOPER_GUIDE.md):

- **Pull before work** — start from the latest state.
- **Small commits** — one focused change per commit.
- **Clear commit messages** — say what changed and why.
- **Push after validated work** — only push changes you've checked.

> Agents must **not** run `git add`, `git commit`, `git push`, or `git tag` unless the human
> explicitly asks. Propose changes and let the owner commit, unless instructed otherwise.

---

## 17. Commit Quality Expectations

Every commit should leave the repository in a:

- **Working state** — it runs / is not knowingly broken.
- **Reproducible state** — results remain re-creatable; randomness controlled where relevant.
- **Documented state** — any decision the commit embodies is documented.

Avoid commits that leave the project half-broken between sessions.

---

## 18. AI-Agent Behavior Requirements

Any AI agent (Codex or otherwise) working here must:

- **Read the specs before implementation** — understand intent before changing anything.
- **Stay within scope** — respect the scope boundaries (§7) and non-goals (§8).
- **Preserve reproducibility** — never introduce hidden knowledge or undocumented steps.
- **Prefer simple solutions** — least complexity that meets the requirement.
- **Ask for clarification rather than invent requirements** — if a spec is silent or ambiguous, raise
  it; do not guess and bake an assumption into code.
- **Work in small, reviewable steps** — make changes the owner can read and approve.
- **Defer to the authority hierarchy** (§4) and surface any spec conflict instead of resolving it
  silently.

---

## 19. Forbidden Behaviors

Do **not**:

- **Scope creep** — adding features beyond the agreed scope/budget.
- **Undocumented decisions** — making significant choices without writing them down.
- **Hidden assumptions** — relying on context that isn't in the repository.
- **Committing data** — raw/processed/external data or large outputs.
- **Ignoring specs** — implementing anything that contradicts `docs/specs/`.
- **Introducing unnecessary complexity** — infrastructure, tooling, or abstractions the project
  doesn't need.
- **Building toward a non-goal** (§8) — SaaS, commercial platform, betting product, live service,
  research programme, or large-scale MLOps.
- **Committing secrets** — keys, tokens, passwords.
- **Running git write commands** (`add`/`commit`/`push`/`tag`) without explicit human instruction.

---

## 20. Definition of Done

StatSport is **done** when it meets the completion criteria in
[`PORTFOLIO_HANDOFF_SPEC.md`](docs/specs/PORTFOLIO_HANDOFF_SPEC.md), consistent with the 40–60 hour
budget and the three-project strategy. In practice:

- [ ] The **specification suite** is coherent and authoritative under `docs/specs/`.
- [ ] A **baseline and a selected model** exist and are compared **honestly**.
- [ ] **Results** are reported honestly, framed against the baseline, with limitations and uncertainty.
- [ ] **Predictions are explainable**, with reader-facing explanations.
- [ ] The work is **reproducible** from repository contents and documented steps, on macOS and
      Windows 11.
- [ ] A **clear README** communicates motivation, problem, methodology, results, explainability,
      reproducibility, and navigation.
- [ ] **Documentation is consistent, honest, and navigable.**
- [ ] The project **respects the budget, non-goals, and scope boundaries**.
- [ ] The project is **finished** — enabling the other two summer repositories.

When these criteria are met, **stop polishing and ship it.** Finishing is the skill being
demonstrated.

---

> **Final rule:** Specs first, simplicity always, honesty throughout. If a change can't be made
> within scope, within budget, reproducibly, and explainably — don't make it; document the question
> and ask.
