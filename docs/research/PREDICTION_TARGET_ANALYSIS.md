# StatSport — Prediction Target Analysis

**Research / decision-support document**

> _A structured comparison of realistic Bundesliga prediction targets against the StatSport specifications — to inform, but not to make, the final target decision._

| | |
|---|---|
| **Status** | Research — for review |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Research artifact (informs `MODELING_SPEC.md` / `EVALUATION_SPEC.md`; conforms to all existing specifications) |
| **Parents** | [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](../specs/DATA_SPEC.md) · [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) · [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) · [`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md) · [`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md) · [`PORTFOLIO_HANDOFF_SPEC.md`](../specs/PORTFOLIO_HANDOFF_SPEC.md) · [`AGENTS.md`](../../AGENTS.md) |
| **Related** | [`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md) |

> **What this document is:** a prediction-target analysis performed *before* the target decision. It
> identifies realistic prediction targets achievable from the selected dataset, scores each against the
> StatSport specifications, and produces a ranked recommendation with a primary choice and a fallback.
> **It does not select the final prediction target** — that decision is owned by `MODELING_SPEC.md`
> (with metrics following in `EVALUATION_SPEC.md`) and remains the human's to make. This document is
> **decision-support only**: it changes no specification and commits to no implementation.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total; one of three summer
> portfolio repositories.

---

## 1. Context and Scope

The dataset decision is approved (see [`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md)
and the **Selected Dataset Decision** in [`DATA_SPEC.md`](../specs/DATA_SPEC.md)):

- **Source:** Football-Data.co.uk
- **League:** Bundesliga
- **Seasons:** 2020/21–2024/25 (five completed seasons)

The next major decision is the **prediction target** — the specific outcome the model forecasts. This
is a deferred decision in `PROJECT_OVERVIEW.md`, owned by `MODELING_SPEC.md` (label) and
`EVALUATION_SPEC.md` (metrics). This document evaluates the candidates so the eventual choice is
defensible, documented, and traceable.

**Out of scope (by constraint):** modifying any spec, writing code, creating datasets/notebooks/scripts,
or committing to implementation. The final selection is the **next** step (§7).

### 1.1 What the selected data supports

Football-Data.co.uk Bundesliga rows provide, per match: the full-time result (a direct **H/D/A**
label), full-time and half-time goals for each side, and match-level statistics (shots, shots on
target, corners, fouls, yellow/red cards), plus bookmaker odds columns the project will **not** use as
a target or framing (consistent with the betting non-goal in `PROJECT_OVERVIEW.md`).

**Consequence:** every candidate target below is **derivable deterministically** from the selected
fields. So *data suitability and reproducibility are high and roughly equal across all candidates* —
differentiation comes almost entirely from portfolio value, explainability, evaluation simplicity,
modelling suitability, and budget fit.

---

## 2. Method

### 2.1 Scoring rubric

Each candidate is scored **1 (poor) – 5 (excellent)** on the twelve evaluation criteria. Weights
encode the inherited priority order (portfolio value → reproducibility → explainability → evaluation
quality → presentation clarity) and the finishability mandate. The **Fit Score /100** is the weighted
average rescaled: `Fit = Σ(score × weight) ÷ Σ(weight) × 20`, with `Σ(weight) = 47`.

| # | Criterion | Weight | What a 5 looks like |
|---|-----------|:------:|---------------------|
| 1 | Portfolio value | 6 | The canonical, recognizable "football prediction" a reviewer respects |
| 2 | Explainability | 5 | Outcome and drivers map cleanly to plain-language football intuition |
| 3 | Evaluation simplicity | 3 | Few, standard, understandable metrics with an obvious baseline |
| 4 | Reviewer comprehension | 4 | A non-expert instantly grasps what is being predicted |
| 5 | Feature-engineering suitability | 3 | Available fields yield informative, interpretable features |
| 6 | Modelling suitability | 3 | Well-behaved for classical, interpretable models within budget |
| 7 | Reproducibility | 5 | Label derived deterministically from documented fields |
| 8 | Data suitability | 4 | Directly and cleanly available from the selected dataset |
| 9 | Fit for a 40–60 hour project | 4 | Comfortably finishable, leaving room for two more projects |
| 10 | Admissions-review suitability | 4 | Reads as mature, honest analytical work to a Passau reader |
| 11 | Technical communication value | 4 | Supports a clear, complete narrative end to end |
| 12 | Long-term maintainability | 2 | Stable definition unlikely to need rework |

> **Caveat:** fit scores are a structured judgment encoding the inherited priorities, not a precise
> measurement. Other defensible weightings exist; the ranking, not the decimal, is the point.

---

## 3. Candidate Targets

### 3.1 Home / Draw / Away (1X2)

**Description.** Three-class classification of the full-time result (home win / draw / away win), taken
directly from the dataset's result field.

**Pros.** The canonical football prediction; immediately recognizable and credible. Directly available
(no derivation). Tells the *complete* match-outcome story. Rich, interpretable feature space (home
advantage, recent form, shot quality). Natural, honest baseline (majority/home-advantage prior).

**Cons.** Three classes, with **draws (~1 in 4 matches) genuinely hard to predict** — a known,
well-documented difficulty. Multiclass evaluation (accuracy + multiclass log-loss) is slightly more
involved than binary.

**Risks.** Draw class may be under-predicted, and class imbalance can flatter naive accuracy — but this
is a *feature* for an honest narrative, not a defect, if reported transparently per `EVALUATION_SPEC.md`.

**Expected implementation complexity.** **Low–Medium.** Standard multiclass workflow with classical
models; the draw class adds analysis (not infrastructure).

**Explainability suitability.** **Excellent** — "why home win vs draw vs away" maps directly to
intuitive drivers; ideal for the reader-first explanations in `EXPLAINABILITY_SPEC.md`.

**Portfolio suitability.** **Excellent** — the definitive demonstration of a football match predictor;
strongest admissions and communication signal.

**Fit score: 96 / 100.**

---

### 3.2 Home Win vs Not Home Win

**Description.** Binary classification: did the home team win (yes/no), collapsing draw and away win
into the negative class.

**Pros.** The **simplest, cleanest** framing — binary metrics (accuracy, ROC-AUC, log-loss, Brier) and
an obvious base-rate baseline. Excellent reviewer comprehension. Centers the most intuitive football
phenomenon (home advantage), giving a tidy explainability story. Maximally finishable.

**Cons.** Collapses two distinct outcomes (draw, away win) into "not home win," losing nuance and some
of the complete-story value of 1X2. Slightly less impressive as a headline than full match prediction.

**Risks.** Minimal — well-behaved and low-risk; the main "risk" is that it under-sells the work
relative to 1X2.

**Expected implementation complexity.** **Low.** The most straightforward target to model and evaluate.

**Explainability suitability.** **Excellent** — home advantage + form + shot quality explain the
binary outcome cleanly.

**Portfolio suitability.** **Strong** — recognizable and credible, though a simplification of the full
result.

**Fit score: 94 / 100.**

---

### 3.3 Away Win vs Not Away Win

**Description.** Binary classification: did the away team win (yes/no).

**Pros.** Same binary simplicity and clean metrics as §3.2.

**Cons.** Away wins are **rarer (~30%)**, so the positive class is more imbalanced and harder. Framing
is less natural than home-win as a headline (home advantage is the intuitive anchor). Slightly weaker
reviewer framing.

**Risks.** Class imbalance can depress recall on the positive class and complicate honest reporting.

**Expected implementation complexity.** **Low–Medium** (imbalance handling/analysis).

**Explainability suitability.** **Good** — interpretable, but a less intuitive default framing than home win.

**Portfolio suitability.** **Moderate–Strong** — valid but a less obvious choice than home win or 1X2.

**Fit score: 86 / 100.**

---

### 3.4 Over / Under Goals (e.g., Over 2.5)

**Description.** Binary classification of whether total match goals exceed a threshold (conventionally 2.5).

**Pros.** Clean binary with simple metrics; interpretable via attacking/defensive features; derivable
from goal columns.

**Cons.** The threshold is **arbitrary** (2.5 is a betting convention), and the target is **strongly
associated with betting markets** — in tension with the project's "**NOT a betting/odds product**"
non-goal framing (`PROJECT_OVERVIEW.md`, `AGENTS.md` §8). Analytically legitimate, but a weaker
*portfolio and admissions* framing.

**Risks.** Optics: may read as a betting-flavored project despite the non-goal; threshold choice needs
justification.

**Expected implementation complexity.** **Low.**

**Explainability suitability.** **Good** — total-goals drivers are interpretable.

**Portfolio suitability.** **Moderate** — capable but off-narrative for "match outcome" and
betting-adjacent.

**Fit score: 76 / 100.**

---

### 3.5 Both Teams To Score (BTTS)

**Description.** Binary classification of whether both teams score at least one goal.

**Pros.** Simple binary with clean metrics; interpretable via both sides' attacking strength.

**Cons.** Also a **betting-market staple** (same non-goal tension as §3.4); somewhat **niche/gimmicky**
as a portfolio headline and further from "who wins."

**Risks.** Betting-framing optics; less compelling admissions narrative.

**Expected implementation complexity.** **Low.**

**Explainability suitability.** **Good** — attack/defense strength of both teams.

**Portfolio suitability.** **Moderate** — valid but off the core match-prediction story.

**Fit score: 74 / 100.**

---

### 3.6 Total Goals Regression

**Description.** Regression predicting the total number of goals in a match (a count outcome).

**Pros.** Demonstrates regression skill; derivable; interpretable feature drivers.

**Cons.** Continuous/count target with **less intuitive evaluation** (RMSE/MAE) than classification
accuracy; harder to frame as a crisp "prediction of the match"; explanation of a continuous goals
figure is less sharp than a class probability.

**Risks.** Noisy target; metric interpretation may confuse a non-expert reader.

**Expected implementation complexity.** **Medium.**

**Explainability suitability.** **Moderate** — interpretable but less crisp than a class outcome.

**Portfolio suitability.** **Moderate** — competent but less recognizable than 1X2/home-win.

**Fit score: 74 / 100.**

---

### 3.7 Goal Difference Regression

**Description.** Regression predicting home goals minus away goals (the margin; its sign implies the result).

**Pros.** Captures **margin and direction** in one target; the sign recovers a result, giving some
explanatory bridge back to 1X2; derivable.

**Cons.** Regression with **less intuitive metrics**; noisy; lower headline recognizability than the
classification targets.

**Risks.** Noise and metric interpretation, as with §3.6.

**Expected implementation complexity.** **Medium.**

**Explainability suitability.** **Moderate–Good** — margin and sign are interpretable.

**Portfolio suitability.** **Moderate.**

**Fit score: 75 / 100.**

---

### 3.8 Other realistic Bundesliga targets considered

- **Draw vs No-Draw (binary):** interesting and honest (draws are hard), but niche and a weak headline —
  better as an *analysis angle within* 1X2 than as the primary target.
- **Outcome via score-line / exact score:** far too many classes and too sparse for the budget;
  excluded on finishability and modelling grounds (`MODELING_SPEC.md` §12).
- **xG-based or possession-based targets:** **not available** — the selected dataset carries no
  expected-goals/possession fields (a known trade-off of the dataset decision; see
  [`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md)).

None of these displaces the seven scored candidates.

---

## 4. Comparison Table

Scores are 1–5 per criterion (see §2.1 rubric); the final column is the weighted Fit Score /100.

| Target | PV (×6) | Explain (×5) | EvalSimp (×3) | Reviewer (×4) | FeatEng (×3) | Model (×3) | Reprod (×5) | Data (×4) | 40–60h (×4) | Admiss. (×4) | TechComm (×4) | Maint. (×2) | **Fit /100** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Home / Draw / Away** | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 5 | **96** |
| **Home Win vs Not** | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 5 | **94** |
| Away Win vs Not | 3 | 5 | 4 | 4 | 5 | 4 | 5 | 5 | 5 | 3 | 4 | 5 | **86** |
| Over / Under Goals | 2 | 4 | 5 | 4 | 4 | 5 | 5 | 4 | 5 | 2 | 3 | 4 | **76** |
| Goal Difference (reg) | 3 | 4 | 3 | 3 | 4 | 3 | 5 | 5 | 4 | 3 | 4 | 4 | **75** |
| Total Goals (reg) | 3 | 4 | 3 | 3 | 4 | 3 | 5 | 5 | 4 | 3 | 3 | 4 | **74** |
| Both Teams To Score | 2 | 4 | 5 | 3 | 4 | 5 | 5 | 4 | 5 | 2 | 3 | 4 | **74** |

> Weighted Fit = Σ(score × weight) ÷ 47 × 20, rounded to the nearest whole number.

---

## 5. Ranked Recommendation

1. **Home / Draw / Away (1X2)** — the canonical target; tops the weighted score on the highest-priority criteria.
2. **Home Win vs Not Home Win** — very close; the simplest, safest, most finishable framing.
3. **Away Win vs Not Away Win** — solid binary, weaker framing and more imbalance.
4. **Over / Under Goals** — clean but betting-adjacent and off-narrative.
5. **Goal Difference Regression** — informative margin target, less intuitive evaluation.
6. **Total Goals Regression** — competent regression, less recognizable.
7. **Both Teams To Score** — valid but niche and betting-flavored.

> **Note on the top two:** 1X2 and Home-Win-vs-Not score within a few points and are genuinely close.
> Home-Win edges ahead on *evaluation simplicity, modelling, and budget fit*; 1X2 wins on the single
> **highest-weighted** criterion (portfolio value) plus admissions and communication value, and tells
> the complete match-outcome story. Under the inherited priority order (portfolio value first), 1X2
> leads — but Home-Win is the deliberate, well-matched fallback precisely because it is simpler.

---

## 6. Recommended Target, Fallback, and Rationale

### 6.1 Recommended prediction target

**Home / Draw / Away (1X2)** — three-class classification of the full-time result.

### 6.2 Recommended fallback target

**Home Win vs Not Home Win** — binary classification.

If 1X2's draw class proves too hard to model meaningfully, or multiclass evaluation threatens the
budget, collapsing to the binary home-win target preserves nearly all portfolio value while maximizing
evaluation simplicity, modelling robustness, and finishability. It is a one-line relabeling of the same
data, so switching is cheap and reproducible.

### 6.3 Rationale (alignment with the specifications)

- **`PROJECT_OVERVIEW.md` — portfolio value & scope.** Portfolio value is the #1 priority. 1X2 is the
  definitive, recognizable football prediction, giving the strongest signal to reviewers and Passau
  admissions readers. It stays squarely within the bounded scope and well clear of the betting non-goal
  (unlike Over/Under and BTTS, which are analytically valid but betting-adjacent in framing).
- **`MODELING_SPEC.md` — interpretable, baseline-first, finishable.** 1X2 has an obvious, honest
  baseline (a home-advantage / majority-class prior) and suits classical, interpretable families
  (logistic/tree models) without GPUs, model zoos, or heavy tuning. It is comfortably finishable within
  40–60 hours; the fallback is even more so.
- **`EXPLAINABILITY_SPEC.md` — reader-first.** "Why home win, draw, or away win?" maps directly to
  intuitive, plain-language drivers (home advantage, recent form, shot quality), supporting both local
  and global explanations for a non-expert reader.
- **`EVALUATION_SPEC.md` — honest, baseline-relative.** The well-known difficulty of predicting draws
  is an *asset* for honest evaluation: it invites a transparent discussion of class imbalance,
  uncertainty, and limitations framed against the baseline — exactly the honesty the spec rewards.
- **`REPRODUCIBILITY_SPEC.md` — deterministic & laptop-friendly.** The 1X2 label is taken directly from
  the dataset's result field (the fallback is a trivial deterministic relabeling), so the target is
  fully reproducible on a typical laptop with no extra tooling.
- **`PORTFOLIO_HANDOFF_SPEC.md` & `AGENTS.md` — finished, credible, in-scope.** 1X2 yields a coherent,
  complete narrative (motivation → problem → approach → results → interpretation → limitations) that
  reads as competent and finished, with the fallback guaranteeing finishability if the draw class
  misbehaves.

---

## 7. Risks Carried Into the Decision

| Risk | Affects | Mitigation at decision time |
|------|---------|------------------------------|
| Hard-to-predict draw class | 1X2 | Report honestly vs. baseline; if it threatens budget, switch to the home-win fallback. |
| Class imbalance flattering accuracy | 1X2, Away-win | Use a small set of appropriate metrics (per `EVALUATION_SPEC.md`); don't rely on accuracy alone. |
| Betting-framing optics | Over/Under, BTTS | Prefer outcome targets; if chosen, justify framing and avoid odds-as-features. |
| Less intuitive regression metrics | Total Goals, Goal Diff | Only choose if the narrative justifies regression; otherwise prefer classification. |
| Scope creep toward richer targets (xG) | all | Not supported by the selected data; hold the line on the bounded plan. |

---

## 8. Honest Limitations of This Analysis

- **No data was inspected or modelled** (per constraints); scores reflect target characteristics and
  the spec criteria, not empirical results from the Bundesliga data.
- **Fit scores are a structured judgment**, not a measurement; the ranking is more meaningful than the
  exact number, and the top two are deliberately close.
- **Betting-adjacent targets are scored lower on framing, not capability** — they remain analytically
  valid; the penalty reflects portfolio/admissions optics under the project's non-goals.

---

## 9. Next Natural Step

Review this analysis and **select the prediction target** — recording the choice (and its baseline and
metric implications) in [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) and
[`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md), per their deferred-decision tables. This document
is **non-binding input** to that decision; it makes no change to any spec and commits to no
implementation.

---

> **Conformance:** This research artifact respects the scope boundaries, non-goals, priorities, budget
> philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) and
> the downstream specifications. It introduces no new project requirements, modifies no specification,
> and does not finalize the prediction-target decision.
