# StatSport — Evaluation Specification

**Evaluation strategy specification**

> _How StatSport judges success — honestly, against a baseline, and reproducibly — using an approved
> evaluation strategy while preserving later reporting and success-criteria decisions._

| | |
|---|---|
| **Status** | Specification Phase |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Downstream specification (conforms to `PROJECT_OVERVIEW.md`, `DATA_SPEC.md`, `MODELING_SPEC.md`) |
| **Parents** | [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](DATA_SPEC.md) · [`MODELING_SPEC.md`](MODELING_SPEC.md) |

> **What this document is:** the evaluation strategy for StatSport. It defines the evaluation
> philosophy, baseline-comparison rules, validation discipline, and reporting expectations. The
> prediction target is now fixed (see
> **[Selected Prediction Target Context](#selected-prediction-target-context)** below), and the
> train/test strategy, validation strategy, and metric set are now approved (see
> **[Selected Evaluation Strategy](#selected-evaluation-strategy)** below). It conforms to the anchor
> overview, the data specification, and the modelling specification.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total.
> **Inherited rules of thumb:** evaluation quality over impressive-looking scores; honest
> interpretation over leaderboard performance; reproducibility is mandatory.

---

## Selected Prediction Target Context

> **Status:** Approved (target only). This section records the now-fixed prediction target so the
> evaluation rules can be read against it. It follows the approved analysis in
> [`docs/research/PREDICTION_TARGET_ANALYSIS.md`](../research/PREDICTION_TARGET_ANALYSIS.md) and the
> **Selected Prediction Target** in [`MODELING_SPEC.md`](MODELING_SPEC.md). **The final metric set,
> validation scheme, and split strategy are approved in
> [Selected Evaluation Strategy](#selected-evaluation-strategy).**

| Decision | Selected value |
|----------|----------------|
| **Approved prediction target** | Home / Draw / Away (1X2) — three-class classification of the full-time result |
| **Approved fallback target** | Home Win vs Not Home Win — binary classification |

### Evaluation implications

Fixing the target as a classification problem narrows the *kind* of evaluation that applies. Evaluation
will compare the selected model against a mandatory baseline on the same data and procedure (§3), using
the approved classification metrics in
[Selected Evaluation Strategy](#selected-evaluation-strategy). A sensible, honest baseline for this
target is a majority-class / home-advantage prior. The fallback (home win vs not) would make the problem
binary, simplifying metric interpretation further; the choice between target and fallback does not
change these rules.

### Multiclass evaluation expectations

For the primary three-class target, evaluation must account for **three outcomes (home / draw / away)**
rather than two. The approved metric set therefore supports:

- Metrics that are meaningful across multiple classes and not misleading under class imbalance.
- Awareness that overall accuracy alone can flatter a model that simply favors the majority outcome.
- Per-class insight (how the model does on home wins, draws, and away wins separately), reported in a
  reader-facing way consistent with §9–§10.

### Draw-class considerations

Draws (~1 in 4 matches) are well known to be the hardest class to predict. Evaluation must therefore:

- **Examine the draw class explicitly** rather than letting it disappear into an aggregate score.
- **Avoid overclaiming** when apparent accuracy is driven by easy home/away calls (§8, §13).
- Treat weak draw-class performance as a **valid, reportable result**, not something to hide (§3).
- If the fallback target is adopted, draws fold into the negative class, which removes this specific
  difficulty while changing the interpretation accordingly.

### Honest-reporting expectations

Consistent with the inherited honesty priority, results for this target must be reported with
uncertainty and limitations stated (§8), framed against the baseline (§3), interpreted in plain
language (§9), and reproducibly (§11). A null or marginal improvement over the baseline — entirely
plausible for football outcomes — is an acceptable, publishable result and must not be inflated.

> **Full comparison and ranking:** see
> [`docs/research/PREDICTION_TARGET_ANALYSIS.md`](../research/PREDICTION_TARGET_ANALYSIS.md).

---

## Selected Evaluation Strategy

> **Status:** Approved. This section converts the previously deferred metric, validation, and split
> decisions into fixed project decisions. It follows the approved analysis in
> [`docs/research/EVALUATION_STRATEGY_ANALYSIS.md`](../research/EVALUATION_STRATEGY_ANALYSIS.md).
> Final target-specific success criteria, final reporting format, and the concrete implementation
> mechanism remain deferred (see §14).

### Approved Train/Test Strategy

**Chronological hold-out**

- **Train:** 2020/21–2023/24
- **Test:** 2024/25

### Approved Validation Strategy

**Season-blocked walk-forward validation**

Equivalent expanding-window methodology:

- Train 2020/21 -> Validate 2021/22
- Train 2020/21–2021/22 -> Validate 2022/23
- Train 2020/21–2022/23 -> Validate 2023/24

### Approved Core Metrics

- Accuracy
- Balanced Accuracy
- Log Loss
- Macro-F1
- Confusion Matrix

### Approved Optional Metrics

- Brier Score
- Calibration Assessment

### Evaluation Rationale

This strategy is approved because it turns the evaluation layer into a clear, honest, and
reproducible demonstration of project judgment without expanding the project beyond its portfolio
scope.

It aligns with [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) by keeping evaluation bounded, readable,
and suitable for a finished portfolio repository. A chronological hold-out gives reviewers a simple
headline comparison: train on past seasons, test on the next unseen season. The walk-forward validation
adds useful stability checks across earlier seasons without becoming an exhaustive benchmark suite.

It aligns with [`MODELING_SPEC.md`](MODELING_SPEC.md) by evaluating the mandatory baseline and selected
model on the same temporally valid procedure. The approved metrics fit the Home / Draw / Away
classification target and the selected probabilistic, interpretable modelling approach: accuracy is
easy to understand, balanced accuracy and Macro-F1 reduce the risk of hiding weak class performance,
log loss rewards honest probabilities, and the confusion matrix makes outcome-level errors visible.

It aligns with [`EXPLAINABILITY_SPEC.md`](EXPLAINABILITY_SPEC.md) by preserving draw-class visibility
and supporting reader-facing interpretation. Balanced Accuracy, Macro-F1, and the confusion matrix help
explain where the model succeeds or struggles across home wins, draws, and away wins, while Log Loss
and optional calibration checks connect predicted probabilities to honest uncertainty.

It aligns with [`REPRODUCIBILITY_SPEC.md`](REPRODUCIBILITY_SPEC.md) by using deterministic,
documentable season-based splits. The train/test split and validation folds can be recreated from the
season labels alone, avoiding hidden manual choices and reducing leakage risk. Because all validation
blocks occur after their training blocks, the strategy preserves temporal integrity and prevents future
matches from informing earlier predictions.

The selected metrics and split procedure improve portfolio value by showing evaluation rigor without
metric shopping, leakage, or inflated claims. They do not define exact performance thresholds, exact
success criteria, reporting templates, or implementation mechanics; those remain later decisions under
§14.

---

## 1. Purpose of the Evaluation Layer

The evaluation layer determines, **honestly and reproducibly**, whether StatSport's selected model
improves on its baseline and what that result actually means. Its job is to demonstrate **sound
evaluation practice and honest interpretation** — not to produce impressive-looking numbers.

Concretely, the evaluation layer must:

- Compare every selected (or candidate) model against the mandatory **baseline** (per `MODELING_SPEC.md`).
- Use a **small set of appropriate, understandable metrics** matched to the prediction target.
- Guard against **leakage** and respect **temporal integrity** where appropriate.
- Report **uncertainty, limitations, and honest interpretation**, avoiding overclaiming.
- Remain **reproducible** and **finishable** within the 40–60 hour budget.

---

## 2. Evaluation Philosophy

StatSport's evaluation is governed by these preferences:

- **Evaluate honestly** — results are reported as they are, not as one wishes them to be.
- **Always compare against the baseline** — improvement is only meaningful relative to a reference.
- **Use a small number of appropriate metrics** — few, justified, and fit for the target.
- **Prefer understandable metrics over impressive but opaque ones** — clarity outranks sophistication.
- **Avoid overclaiming** — conclusions must be proportionate to the evidence.
- **Report limitations clearly** — caveats are part of the result, not an afterthought.

When these preferences conflict, the inherited priority order and the time budget decide.

---

## 3. Baseline Comparison Requirements

- **Every selected (or candidate) model must be compared against the baseline.**
- **Improvement must be demonstrated, not assumed** — a model earns its place only by beating the
  baseline under a reproducible procedure.
- **If improvement is weak or absent, the project must report that honestly** — a null or marginal
  result is a valid, publishable outcome and must not be hidden or inflated.
- Comparisons must be made **on the same data and procedure**, so the baseline and selected model are
  judged on equal terms.

---

## 4. Metric-Selection Principles

- **Metrics must match the final prediction target** — the target is now fixed as a classification
  problem (Home / Draw / Away; fallback Home Win vs Not — see
  [Selected Prediction Target Context](#selected-prediction-target-context)), so metrics must suit
  classification.
- **Metrics must be understandable to a portfolio reviewer** — interpretable by a non-expert.
- **Metrics must be few, justified, and clearly explained** — a small set, each with a stated reason.
- **Metrics must follow the approved set** in
  [Selected Evaluation Strategy](#selected-evaluation-strategy), unless a later documented decision
  changes the target-specific success criteria or reporting needs without contradicting this spec.

> This document defines both the approved metric set and the principles for explaining and applying it.

---

## 5. Validation Principles

- **Avoid leakage** — no information from the evaluation target reaches training or feature creation.
- **Preserve temporal integrity where appropriate** — respect chronological order when the problem is
  time-dependent (do not validate on the past using the future).
- **Use reproducible splits/procedures** — the same procedure yields the same result for anyone.
- **Keep validation simple enough for a 40–60 hour project** — a clear, defensible scheme over an
  elaborate one.
- Frame all results **relative to the baseline** (see §3).

> The **final validation scheme** and **final split strategy** are approved in
> [Selected Evaluation Strategy](#selected-evaluation-strategy).

---

## 6. Leakage-Avoidance Requirements

- **Target leakage** is prohibited: features must not encode the outcome being predicted.
- **Train/test contamination** is prohibited: evaluation data must not influence training or feature
  decisions.
- **Preprocessing discipline**: any data-dependent transformation must be derived only from training
  data and applied consistently, so evaluation data stays unseen.
- **Provenance review**: features are checked against their source (per `DATA_SPEC.md`) to ensure no
  outcome information leaks in.
- Leakage checks are part of the evaluation, and any identified risk is documented.

---

## 7. Temporal-Integrity Requirements

- Where the prediction problem is **time-dependent**, evaluation must **respect chronological order**.
- Training/feature information must **precede** the matches being evaluated — no using future data to
  predict earlier outcomes.
- Any time-based split or ordering must be **reproducible** and **documented**.
- Where temporal structure is **not** relevant to the chosen target, this requirement is applied
  accordingly — the decision and its rationale are recorded.

---

## 8. Uncertainty and Limitation Reporting

- **Acknowledge uncertainty** — results are reported with appropriate caveats rather than as exact
  truths.
- **State limitations explicitly** — data scope, sample size, class balance, and method constraints
  are named.
- **Distinguish signal from noise** — small differences are not presented as decisive.
- **No false precision** — results are reported at a level of confidence the evidence supports.
- Limitations are treated as **first-class content**, consistent with the project's honesty priority.

---

## 9. Result Interpretation Requirements

- **Interpret, don't just report** — explain what a result means in plain language.
- **Tie results to the baseline** — every claim is framed as a comparison to the reference.
- **Connect to explainability** — interpretation should align with the model's explanations
  (per `MODELING_SPEC.md`), so *what* and *why* are consistent.
- **Proportionate conclusions** — claims match the strength of the evidence; weak results are stated
  as weak.
- **Reader-facing** — interpretation is written for a portfolio reviewer, not buried in raw output.

---

## 10. Portfolio-Quality Reporting Expectations

The evaluation should read as **competent, honest, and finished**:

- A **clear baseline → selected-model comparison** a reviewer can follow.
- **Few, well-explained metrics** with stated rationale.
- **Honest framing** of improvement, including null or marginal outcomes.
- **Visible limitations and uncertainty**.
- **Reproducible results** a reader can trust and re-run.
- Suitable for **public GitHub publication** and **technical review**, and scoped to remain
  **one of three** completed summer portfolio repositories.

> The **final reporting format** (where/how results are presented) is **deferred** (see §14).

---

## 11. Reproducibility Requirements

Reproducibility is **mandatory** and outranks impressive scores:

- **Deterministic evaluation** — controlled randomness (e.g., fixed seeds) so results repeat.
- **Reproducible splits/procedures** — anyone can recreate the same evaluation from documented steps.
- **Documented workflow** — the path from processed data and models to reported results is written
  down, mechanism-agnostic (notebooks, scripts, or both, per the overview).
- **Regenerable artifacts** — evaluation outputs (figures, tables) can be regenerated; large artifacts
  are not committed, consistent with `DATA_SPEC.md` and the repository `.gitignore`.
- **No hidden manual steps** — any manual action is recorded explicitly.

---

## 12. Evaluation Exclusions

To protect honesty, simplicity, and the budget, the project will **not** do:

- **Leaderboard chasing** — no optimizing evaluation to maximize a headline number.
- **Metric shopping** — no selecting metrics after the fact to flatter results.
- **Exhaustive benchmark suites** — no sprawling battery of metrics or datasets.
- **Production monitoring** — no live performance tracking.
- **A/B testing** — no experimentation against live users.
- **Live-system evaluation** — no real-time or deployed-system assessment.

These exclusions are consistent with the overview's non-goals (no live service, no MLOps).

---

## 13. Evaluation Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Overclaiming** | Presenting marginal gains as decisive | Proportionate conclusions; report uncertainty (§8). |
| **Metric shopping** | Choosing metrics to flatter results | Fix few justified metrics up front, matched to target (§4). |
| **Data leakage** | Target/feature contamination inflates scores | Apply leakage-avoidance requirements (§6). |
| **Temporal leakage** | Using future data to predict the past | Preserve temporal integrity (§7). |
| **Unfair baseline comparison** | Baseline and model judged on different terms | Same data and procedure for both (§3). |
| **Irreproducibility** | Undocumented or non-deterministic evaluation | Control randomness; document splits/procedures (§11). |
| **Scope/budget overrun** | Evaluation grows too elaborate | Keep it simple; honor exclusions (§12) and the budget. |
| **Hidden negative results** | Suppressing weak/absent improvement | Report honestly, including null results (§3). |

---

## 14. Deferred Evaluation Decisions

The following table records which evaluation decisions are now approved and which intentionally remain
deferred:

| Deferred decision | Status / owning step |
|-------------------|----------------------|
| **Final metrics** | Approved — see [Selected Evaluation Strategy](#selected-evaluation-strategy). |
| **Final validation scheme** | Approved — season-blocked walk-forward validation; see [Selected Evaluation Strategy](#selected-evaluation-strategy). |
| **Final split strategy** | Approved — chronological hold-out; see [Selected Evaluation Strategy](#selected-evaluation-strategy). |
| **Final target-specific success criteria** | Deferred. |
| **Final reporting format** | Deferred. |
| Exact prediction target/label | ✅ **Decided** — Home / Draw / Away (1X2), fallback Home Win vs Not Home Win; see [Selected Prediction Target Context](#selected-prediction-target-context). |
| Concrete implementation mechanism (script vs. notebook vs. both) | Deferred (overview allows either or both). |

> This specification establishes the **rules, philosophy, approved metric set, approved validation
> scheme, and approved split strategy** for evaluation. It deliberately does **not** set exact
> performance thresholds, target-specific success criteria, reporting templates, or the concrete
> implementation mechanism — those decisions remain open by design.

---

> **Conformance:** This document inherits and respects the scope boundaries, non-goals, priorities,
> budget philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md), and
> builds on [`DATA_SPEC.md`](DATA_SPEC.md) and [`MODELING_SPEC.md`](MODELING_SPEC.md). It introduces no
> new project requirements beyond evaluation-layer rules.
