# StatSport — Evaluation Strategy Analysis

**Research / decision-support document**

> _A structured comparison of realistic evaluation strategies — train/test methodology, validation methodology, metrics, and success criteria — against the StatSport specifications, to inform but not make the final evaluation decision._

| | |
|---|---|
| **Status** | Research — for review |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Research artifact (informs `EVALUATION_SPEC.md`; conforms to all existing specifications) |
| **Parents** | [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](../specs/DATA_SPEC.md) · [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) · [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) · [`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md) · [`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md) · [`PORTFOLIO_HANDOFF_SPEC.md`](../specs/PORTFOLIO_HANDOFF_SPEC.md) · [`AGENTS.md`](../../AGENTS.md) |
| **Related** | [`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md) · [`PREDICTION_TARGET_ANALYSIS.md`](./PREDICTION_TARGET_ANALYSIS.md) · [`FEATURE_ENGINEERING_ANALYSIS.md`](./FEATURE_ENGINEERING_ANALYSIS.md) · [`MODEL_CANDIDATE_ANALYSIS.md`](./MODEL_CANDIDATE_ANALYSIS.md) |

> **What this document is:** an evaluation-strategy analysis performed *before* the evaluation decision.
> It identifies realistic train/test methodologies, validation methodologies, and metrics appropriate
> for the approved target, feature strategy, and model, scores each against the StatSport
> specifications, and produces explicit recommendations for a **train/test strategy**, a **validation
> strategy**, a **metric set**, and **success criteria**. **It does not change any specification** — the
> final metrics, validation scheme, split strategy, and target-specific success criteria are deferred
> decisions owned by [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) (§14), and the choice is the
> human's to make. This document is **decision-support only**: it modifies no spec, writes no code,
> creates no datasets/notebooks/scripts, and commits to no implementation.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total; one of three summer
> portfolio repositories.
>
> **Governing rule of thumb (from `EVALUATION_SPEC.md` §2):** evaluation quality over impressive-looking
> scores; honest interpretation over leaderboard performance; reproducibility is mandatory. This
> analysis prioritizes **honest evaluation, explainability, reproducibility, and portfolio value over
> maximizing reported scores.**

---

## 1. Context and Scope

The dataset, prediction-target, feature-strategy, and modelling decisions are approved (see the related
research documents and the corresponding decisions in [`DATA_SPEC.md`](../specs/DATA_SPEC.md),
[`MODELING_SPEC.md`](../specs/MODELING_SPEC.md), and [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md)):

- **Source / league / seasons:** Football-Data.co.uk · Bundesliga · 2020/21–2024/25 (five seasons)
- **Prediction target:** Home / Draw / Away (1X2), three-class classification of the full-time result
- **Fallback target:** Home Win vs Not Home Win, binary classification
- **Core features:** home advantage, recent form, goals scored, goals conceded, goal difference
- **Optional features:** shots on target, league position, Elo-style rating
- **Baseline:** home-advantage baseline (with majority-class reported alongside as the absolute floor)
- **Selected model:** multinomial logistic regression
- **Fallback model:** random forest

The next major decision is the **evaluation strategy** — how train/test is split, how the model is
validated during development, which metrics are reported, and what counts as success. The final
metrics, validation scheme, split strategy, and success criteria are deferred decisions in
[`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §14. This document evaluates the candidates so the
eventual choice is defensible, documented, and traceable.

**Out of scope (by constraint):** modifying any spec, writing code, creating datasets/notebooks/scripts,
or committing to implementation. Selecting the evaluation strategy is the **next** step (§12).

### 1.1 What the approved decisions imply for evaluation

- **The problem is time-dependent.** Every approved feature is a **pre-match rolling aggregate over
  prior fixtures** ([`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) "Selected Feature Strategy"), and
  matches occur in a strict chronological order. [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §7
  therefore requires that evaluation **respect chronological order** — training/feature information must
  *precede* the matches being evaluated. This is the single most consequential constraint on the
  train/test and validation choice: **any scheme that lets future matches inform predictions about past
  matches is a temporal-leakage defect**, no matter how standard it is elsewhere.
- **Small-to-medium tabular data.** Five Bundesliga seasons are ~1,530 matches (18 teams × 34 matchdays
  = 306 fixtures per season × 5). That is enough to train an interpretable model but **small enough that
  a single test split is noisy** — a consideration that pushes toward validation schemes that average
  over several time-ordered folds.
- **A three-class target with a hard draw class.** Draws (~1 in 4 matches) are intrinsically hard
  ([`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md), "Draw-class considerations"). Metrics must give
  **per-class insight** and must not let a model that simply favours the majority (home) outcome look
  good on an aggregate number. This rules *out* relying on accuracy alone and rules *in* per-class and
  probability-aware metrics.
- **The selected model emits probabilities.** Multinomial logistic regression produces class
  probabilities, so **probabilistic, proper-scoring metrics** (log loss, Brier) are natural, honest, and
  directly comparable against the baseline's reference probabilities.
- **Few, understandable metrics — by mandate.** [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §4
  requires a **small set** of metrics, each justified and understandable to a non-expert, and §12
  forbids "metric shopping" and "exhaustive benchmark suites." Differentiation among metrics therefore
  comes mostly from **honesty, explainability, and reviewer comprehension**, not from sophistication.
- **Baseline-first and honest by mandate.** [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §3
  requires every result to be framed against the baseline on the *same data and procedure*, and a null
  or marginal improvement is an acceptable, publishable result that must not be inflated.

**Consequence:** all candidates here are judged first on **temporal honesty** (does the scheme respect
chronological order?) and on whether outputs support **honest, baseline-relative, per-class, reader-facing**
interpretation — not on whichever scheme or metric yields the highest headline number.

> **No spec is changed here.** "Evaluation quality" below judges how *cleanly a strategy supports honest,
> reproducible, reader-facing evaluation*, consistent with the principles in
> [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §2–§11. Final selection remains deferred to that
> spec (§14).

---

## 2. Method

### 2.1 Scoring rubric

Each candidate (methodology or metric) is scored **1 (poor) – 5 (excellent)** on the ten evaluation
criteria from the brief. Weights encode the inherited priority order (portfolio value → reproducibility
→ explainability → evaluation quality → presentation clarity), the finishability mandate, and the
overriding importance of **honesty** in an evaluation layer. The **Fit Score /100** is the weighted
average rescaled: `Fit = Σ(score × weight) ÷ Σ(weight) × 20`, with `Σ(weight) = 41`.

| # | Criterion | Weight | What a 5 looks like |
|---|-----------|:------:|---------------------|
| 1 | Honesty | 5 | No leakage; cannot flatter results; surfaces weakness rather than hiding it |
| 2 | Portfolio value | 5 | A recognizable, credible choice a reviewer respects and trusts |
| 3 | Reproducibility | 5 | Deterministic from the same data + fixed configuration/seed; documented procedure |
| 4 | Explainability | 4 | Easy to explain *what it does* and *what the number means* in plain language |
| 5 | Reviewer comprehension | 4 | A non-expert instantly grasps the scheme/metric |
| 6 | Suitability for football prediction | 4 | Respects match chronology / captures what matters (draws, probabilities) |
| 7 | Alignment with approved target | 4 | Native, well-behaved for Home/Draw/Away (and the binary fallback) |
| 8 | Fit for a 40–60 hour project | 4 | Cheap to build and finish, leaving room for two more projects |
| 9 | Alignment with approved model | 3 | Suits multinomial logistic regression's probabilistic outputs |
| 10 | Implementation simplicity | 3 | Few moving parts; little tuning; low failure surface |

> **Note on criterion 10.** The brief lists "implementation effort / complexity"; it is scored here as
> **implementation simplicity** (5 = simplest) so that, as in
> [`MODEL_CANDIDATE_ANALYSIS.md`](./MODEL_CANDIDATE_ANALYSIS.md) §2.1, a higher score is consistently
> better.

> **Note on scoring the leaky schemes.** Random split, k-fold, and stratified k-fold are scored
> *honestly against a time-dependent problem*. They score low on **honesty** and **football suitability**
> by design, because for this dataset they permit temporal leakage. This is the intended result, not a
> defect of the rubric — it is exactly the judgment [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md)
> §7 asks for.

> **Caveat:** fit scores are a structured judgment encoding the inherited priorities, not a precise
> measurement. The **ranking and the explicit recommendations**, not the decimal, are the point.

---

## 3. Candidate Train/Test & Validation Methodologies

Each candidate is described, weighed (pros / cons / risks), costed, and scored. "Train/test" and
"validation" methodologies are analysed together because the same temporal-integrity logic governs both;
§9 then separates the **recommended train/test strategy** from the **recommended validation strategy**.

### 3.1 Random train/test split

**Description.** Shuffle all ~1,530 matches and randomly assign a fraction (e.g. 80%) to training and
the rest to testing, ignoring match dates.

**Pros.** The textbook default: trivial to implement, instantly familiar, and reproducible with a fixed
seed. Maximizes training data for a given test fraction.

**Cons.** **Breaks chronological order.** Because every feature is a rolling aggregate over prior
fixtures and teams recur across the season, a random split routinely trains on matches that occur
*after* the matches it tests on — **temporal leakage** that inflates apparent performance. It tells a
reviewer nothing about how the model would predict *the next* fixture.

**Risks.** Over-optimistic, dishonest results; a knowledgeable reviewer immediately flags the leakage,
which actively damages portfolio credibility — the opposite of the intended signal.

**Implementation effort.** **Trivial** — one shuffled split.

**Portfolio suitability.** **Poor** — recognizable but, for a time-dependent problem, a competence
red flag rather than a credential.

**Fit score: 61 / 100.**

### 3.2 Chronological train/test split

**Description.** Split by time: train on the earlier seasons and test on the most recent, held-out
matches — e.g. train on **2020/21–2023/24** (~1,224 matches) and test on **2024/25** (~306 matches). No
match in the test set precedes any match in the training set.

**Pros.** **Honest and directly aligned with the problem:** it mirrors the real task — "use the past to
predict the future." Trivially explained to any reviewer ("we trained on four seasons and tested on the
fifth"), fully deterministic, leakage-free by construction, and the simplest scheme that satisfies
[`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §7. Produces one clean, reader-facing
baseline-vs-model comparison on genuinely unseen data.

**Cons.** A **single test season is a noisy estimate** — one season can be unrepresentative (e.g.
an unusual title race, injuries, or the empty-stadium effect of 2020/21 that depressed home advantage).
It uses the final season only for testing, not for learning.

**Risks.** Season-specific quirks could make the held-out year flatter or punish the model; mitigated by
also reporting validation results across earlier seasons (§3.4) and by stating the single-season caveat
honestly (§8 of the spec).

**Implementation effort.** **Trivial–Low** — one date-ordered split.

**Portfolio suitability.** **Excellent** — the clean, honest, recognizable headline a reviewer trusts.

**Fit score: 98 / 100.**

### 3.3 Rolling time-window (sliding-window) validation

**Description.** Train on a **fixed-size** window of recent matches, test on the next block, then slide
the window forward and repeat (older data drops off the back as new data is added to the front).

**Pros.** Temporally honest; produces several time-ordered folds, so the performance estimate is less
noisy than a single split. Models "recent form matters most" by discarding stale data.

**Cons.** **Discards older matches** that this small dataset can ill afford to lose; introduces a window-
length hyperparameter to justify; more code and more folds than a single split, for limited extra value
on five seasons.

**Risks.** Choosing the window length risks looking arbitrary or like quiet tuning; reduced training
data per fold can understate the model's true capability.

**Implementation effort.** **Medium** — multiple folds plus a window-length decision.

**Portfolio suitability.** **Strong** — credible and honest, but the expanding-window variant is the
better fit when data is limited.

**Fit score: 87 / 100.**

### 3.4 Expanding-window (walk-forward) validation

**Description.** Train on **all** data up to time *t*, predict the next block, then expand the training
window to include that block and repeat — "forward chaining" / time-series cross-validation (e.g.
scikit-learn's `TimeSeriesSplit`). The training set grows; predictions are always strictly forward in
time.

**Pros.** The **gold-standard honest validation** for time-dependent prediction: it uses all available
history at each step, never leaks the future, and averages over several forward folds for a **stable,
honest performance estimate** on small data. Recognizable, rigorous, and impressive *without being
dishonest* — strong portfolio signal. Suits the logistic model and the H/D/A target natively.

**Cons.** More moving parts than a single split (multiple folds, careful fold construction); slightly
more to explain; modestly more compute (still laptop-trivial here).

**Risks.** Mild implementation care needed so rolling features are computed *within* each fold's history
only (no cross-fold leakage); the early folds train on little data, which can understate early
performance.

**Implementation effort.** **Medium** — standard library support, but careful, leakage-safe folds.

**Portfolio suitability.** **Excellent** — the most defensible validation methodology; reads as genuine
ML judgment.

**Fit score: 91 / 100.**

### 3.5 k-fold cross-validation

**Description.** Randomly partition matches into *k* folds; train on *k–1* and test on the held-out fold,
rotating through all folds and averaging.

**Pros.** Lower-variance estimate than a single random split; standard, recognizable, well-supported;
uses all data for both training and testing across folds.

**Cons.** **Random folds break chronology** exactly as the random split does — the same temporal
leakage, repeated *k* times. The variance benefit does not redeem the honesty cost for a time-dependent
problem.

**Risks.** Systematically over-optimistic results; a reviewer rightly questions the temporal validity,
undermining the evaluation's credibility.

**Implementation effort.** **Low** — one standard call.

**Portfolio suitability.** **Weak** — recognizable, but misapplied to time-ordered data it signals a gap
in judgment.

**Fit score: 64 / 100.**

### 3.6 Stratified k-fold cross-validation

**Description.** k-fold that **preserves class balance** (the H/D/A proportion) in every fold.

**Pros.** Keeps the hard draw class represented in each fold, which is genuinely helpful for class-imbalanced
classification; otherwise as standard and well-supported as plain k-fold.

**Cons.** **Still random with respect to time** — stratifying on the outcome does nothing to fix temporal
leakage, the decisive defect here. It is the *least-bad* of the random schemes, not a temporally honest
one.

**Risks.** Same over-optimism as k-fold; the class-balance virtue can lull one into ignoring the
temporal-integrity violation.

**Implementation effort.** **Low** — one standard call.

**Portfolio suitability.** **Weak** — marginally better than plain k-fold for the draw class, but the
temporal leakage remains disqualifying for the headline scheme.

**Fit score: 65 / 100.**

### 3.7 Season-blocked walk-forward validation (other realistic strategy)

**Description.** A practical, season-granular instantiation of expanding-window validation: treat each
**season as a block** and walk forward one season at a time — train on 2020/21, test on 2021/22; train
on 2020/21–2021/22, test on 2022/23; and so on, ending with the chronological hold-out of 2024/25. It
unifies the train/test split (§3.2) and the validation methodology (§3.4) into one intuitive,
football-natural scheme.

**Pros.** **Maximally intuitive and honest:** "we always train on completed seasons and predict the next
one" is self-explanatory to any reviewer, respects chronology perfectly, gives several forward folds for
a stable estimate, and uses all history. The season is the natural unit of football competition, so the
blocks are meaningful rather than arbitrary. Deterministic and reproducible.

**Cons.** Coarser granularity than match-level forward chaining (four forward folds across five seasons);
the earliest fold trains on a single season; slightly more to build than one split.

**Risks.** The 2020/21 empty-stadium season as the sole early training block could bias early folds
(reduced home advantage); mitigated by reporting per-fold results and naming the caveat.

**Implementation effort.** **Low–Medium** — a small loop over season boundaries; no tuning.

**Portfolio suitability.** **Excellent** — the clearest possible honest story for a football predictor.

**Fit score: 97 / 100.**

> **Other candidates considered and set aside.** **Nested cross-validation** (an inner loop for tuning
> inside an outer time-series loop) is the rigorous choice when there is heavy hyperparameter search —
> but the selected model needs near-zero tuning ([`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) §12), so
> nesting adds complexity and budget risk for little gain and is better noted as future work. A
> **grouped split by team** does not fit a fixture-prediction target (each match involves two teams).
> **Leave-one-season-out** is a symmetric variant of §3.7 but tests on past seasons using future ones,
> reintroducing mild temporal leakage, so the forward-only walk is preferred. None displaces the seven
> scored candidates.

---

## 4. Methodology Comparison Table

Scores are 1–5 per criterion (see §2.1 rubric); the final column is the weighted Fit Score /100.
Abbreviations: **Hon** honesty, **PV** portfolio value, **Rep** reproducibility, **Ex** explainability,
**Rev** reviewer comprehension, **FB** suitability for football prediction, **Tgt** alignment with
approved target, **40–60h** budget fit, **Mdl** alignment with approved model, **Simp** implementation
simplicity.

| Methodology | Hon (×5) | PV (×5) | Rep (×5) | Ex (×4) | Rev (×4) | FB (×4) | Tgt (×4) | 40–60h (×4) | Mdl (×3) | Simp (×3) | **Fit /100** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Chronological train/test split** | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | **98** |
| **Season-blocked walk-forward** | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 4 | **97** |
| **Expanding-window (walk-forward)** | 5 | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 | 3 | **91** |
| **Rolling time-window** | 5 | 4 | 5 | 4 | 4 | 5 | 5 | 3 | 5 | 3 | **87** |
| **Stratified k-fold** | 1 | 2 | 5 | 4 | 4 | 1 | 4 | 4 | 4 | 4 | **65** |
| **k-fold cross-validation** | 1 | 2 | 5 | 4 | 4 | 1 | 4 | 4 | 4 | 4 | **64** |
| **Random train/test split** | 1 | 1 | 4 | 4 | 5 | 1 | 3 | 5 | 3 | 5 | **61** |

> Weighted Fit = Σ(score × weight) ÷ 41 × 20, rounded to the nearest whole number.

---

## 5. Ranked Methodology Recommendation

1. **Chronological train/test split** (98) — the simplest honest scheme; the recommended **headline
   train/test strategy** (hold out the final season).
2. **Season-blocked walk-forward** (97) — the same idea generalized to several forward folds; the
   recommended **validation strategy** during development.
3. **Expanding-window (walk-forward)** (91) — the rigorous match-level generalization; the technical
   backbone of (2), available if finer granularity is wanted.
4. **Rolling time-window** (87) — honest but discards scarce older data; not preferred on five seasons.
5. **Stratified k-fold** (65) — least-bad random scheme (keeps draw-class balance) but temporally leaky.
6. **k-fold cross-validation** (64) — lower-variance but temporally leaky; misapplied to time data.
7. **Random train/test split** (61) — leakage with no offsetting benefit; a credibility risk.

> **Reading the ranking.** The temporally honest schemes cluster at the top because they satisfy the
> decisive constraint ([`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §7) and the highest-weighted
> criteria (honesty, portfolio value, reproducibility). The random / k-fold family scores respectably on
> reproducibility and comprehension but is **pulled down hard by honesty and football suitability**,
> precisely because random folds leak the future on a time-dependent problem — exactly as intended. The
> top two are near-equivalent and **complementary**: one is the clean final test, the other the
> development-time validation.

---

## 6. Candidate Metrics

Each metric is described, weighed, costed, and scored on the same rubric (§2.1), reinterpreted for
metrics: "alignment with approved model" rewards using the logistic model's probability outputs;
"suitability for football prediction" rewards capturing draws and probability quality; "honesty"
rewards resistance to flattering a majority-class predictor.

### 6.1 Accuracy

**Description.** The fraction of matches whose predicted class equals the actual result.

**Pros.** Universally understood, trivial to compute, the expected headline number. Reproducible.

**Cons.** **Misleading under class imbalance** — a model that mostly predicts the majority (home) outcome
can post a respectable accuracy while ignoring draws and away wins entirely
([`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md), "Multiclass evaluation expectations"). Says nothing
about probability quality or per-class behaviour.

**Risks.** Over-claiming from a single flattering number; must always be paired with a per-class view and
the baseline comparison.

**Implementation effort.** **Trivial.**

**Portfolio suitability.** **Strong** — an expected, intuitive headline, but **only with explicit
caveats** and a baseline reference.

**Fit score: 81 / 100.**

### 6.2 Balanced Accuracy

**Description.** The average of per-class recall (recall for home, draw, and away, averaged equally).

**Pros.** **Corrects the majority-class flattery** of plain accuracy and surfaces the draw class; still
fairly intuitive ("how well does it do on each outcome, on average?"). Reproducible.

**Cons.** Slightly less familiar than accuracy; ignores probability quality; one more number to explain.

**Risks.** Minor — mainly that readers conflate it with plain accuracy without the explanation.

**Implementation effort.** **Trivial.**

**Portfolio suitability.** **Strong** — an honest companion that guards accuracy's blind spot.

**Fit score: 83 / 100.**

### 6.3 Log Loss (cross-entropy)

**Description.** A **proper scoring rule** that penalizes predicted class probabilities by how far they
are from the actual outcome; lower is better. It is essentially the objective logistic regression
optimizes.

**Pros.** **Honest and hard to game:** it rewards well-calibrated probabilities and punishes confident
wrong predictions, so it cannot be flattered by a majority-class strategy. Native multiclass, directly
comparable against the baseline's reference probabilities, and the natural fit for the probabilistic
selected model. The single best scalar for "did the model's *probabilities* improve over the baseline?"

**Cons.** **Less intuitive in absolute terms** to a lay reader (the raw value has no natural scale);
best reported *relative to the baseline* and explained in words.

**Risks.** Misreading the absolute number; mitigated by always presenting it as an improvement over the
baseline and explaining the direction.

**Implementation effort.** **Low** — one standard function on probabilities.

**Portfolio suitability.** **Strong** — a respected, rigorous, honest measure; the probabilistic
backbone of the comparison.

**Fit score: 90 / 100.**

### 6.4 Brier Score

**Description.** The mean squared error between predicted class probabilities and the one-hot actual
outcome; a second **proper scoring rule**, closely tied to calibration. Lower is better.

**Pros.** Honest like log loss but **more intuitive** ("average squared error of the probabilities"),
and it decomposes into calibration and refinement, supporting honest probability reporting. Comparable
against the baseline.

**Cons.** The multiclass form is slightly less standard than log loss; overlaps with log loss, so
reporting both adds little — one proper scoring rule usually suffices.

**Risks.** Minor redundancy with log loss; pick one as primary to keep the metric set small (§4).

**Implementation effort.** **Low–Medium** — straightforward; multiclass version needs a little care.

**Portfolio suitability.** **Strong** — a clean, honest probability metric; a good *optional* companion
to log loss.

**Fit score: 88 / 100.**

### 6.5 F1 Score

**Description.** The harmonic mean of precision and recall for a class; naturally a per-class (or binary)
metric.

**Pros.** Balances precision and recall in one number; well known; ideal for the **binary fallback**
(Home Win vs Not). Reproducible.

**Cons.** For the three-class target it must be **averaged** to give one number (see Macro-F1, §6.6);
raw F1 is per-class. The harmonic-mean idea needs a sentence of explanation; ignores probability quality.

**Risks.** Reporting a single un-averaged F1 for a multiclass problem is ambiguous; specify the averaging.

**Implementation effort.** **Low.**

**Portfolio suitability.** **Strong** for the binary fallback; for the 1X2 target, prefer its
macro-averaged form.

**Fit score: 82 / 100.**

### 6.6 Macro F1

**Description.** The unweighted average of the per-class F1 scores (home, draw, away counted equally).

**Pros.** **Treats the draw class as equally important** as home and away, so a model that neglects
draws is honestly penalized — directly serving the spec's draw-class and honest-reporting expectations.
The best single scalar for **per-class fairness** on this imbalanced target. Reproducible and standard.

**Cons.** One step removed from intuition (an average of harmonic means); ignores probability quality;
needs a short explanation.

**Risks.** Minor — readers may need the "why macro, not micro" point made explicitly.

**Implementation effort.** **Low.**

**Portfolio suitability.** **Excellent** — the honest, imbalance-aware companion to accuracy.

**Fit score: 92 / 100.**

### 6.7 Precision (per class)

**Description.** Of the matches predicted to be class X, the fraction that truly were X.

**Pros.** Intuitive ("when it says *draw*, how often is it right?"); reproducible; a natural component of
the per-class story and readable straight off the confusion matrix.

**Cons.** A **component, not a headline** — incomplete without recall; ignores probability quality.

**Risks.** Cherry-picking one class's precision could mislead; report all three together.

**Implementation effort.** **Trivial** (read from the confusion matrix / classification report).

**Portfolio suitability.** **Moderate–Strong** — valuable as part of the per-class breakdown, not as a
standalone headline.

**Fit score: 83 / 100.**

### 6.8 Recall (per class)

**Description.** Of the matches that truly were class X, the fraction the model identified.

**Pros.** Intuitive ("of the actual draws, how many did it catch?"); **draw recall is the single most
diagnostic number for the hard draw class**, directly serving the spec's draw-class expectation.
Reproducible; reads off the confusion matrix.

**Cons.** A component, not a headline; incomplete without precision; ignores probability quality.

**Risks.** As with precision, report the full set, not a favourable subset.

**Implementation effort.** **Trivial.**

**Portfolio suitability.** **Strong** — the clearest lens on draw-class difficulty.

**Fit score: 85 / 100.**

### 6.9 Confusion Matrix

**Description.** The full 3×3 table of predicted vs. actual outcomes (with a 2×2 form for the fallback).

**Pros.** **The most honest, reader-facing diagnostic available:** it shows everything at once — where
the model is right, and exactly how it confuses draws with home/away wins — with nowhere to hide. Per-class
precision and recall are read straight off it. An excellent, intuitive portfolio figure that
demonstrates per-class transparency. Reproducible and standard.

**Cons.** It is a **diagnostic artifact, not a single scalar**, so it complements (rather than replaces)
headline metrics and is not a one-number baseline comparison.

**Risks.** Essentially none; its only limit is that two matrices are compared visually, not by a single
difference.

**Implementation effort.** **Low** — standard to compute and plot.

**Portfolio suitability.** **Excellent** — the strongest reader-facing evaluation artifact for the
three-class target.

**Fit score: 98 / 100.**

### 6.10 Calibration assessment (reliability)

**Description.** A check of whether predicted probabilities match observed frequencies — e.g. a
reliability diagram, where "matches predicted 60% home win should be home wins ~60% of the time."

**Pros.** **Deeply honest** — it reveals over- or under-confidence that scalar accuracy hides, and
logistic regression tends to be reasonably calibrated, so it is a flattering-but-truthful thing to show.
A sophisticated, impressive-yet-honest portfolio extra; pairs naturally with log loss / Brier.

**Cons.** Less familiar to a lay reviewer; multiclass reliability is **fiddlier** than the binary case;
more effort than the core scalars, so it sits in the optional tier under the budget.

**Risks.** Over-investing time relative to its share of the budget; mitigated by keeping it a single,
simple reliability figure (the fallback's binary form is easiest).

**Implementation effort.** **Medium** — more work, especially multiclass.

**Portfolio suitability.** **Strong** — high-value polish if budget allows; optional, not core.

**Fit score: 83 / 100.**

### 6.11 Ranked Probability Score (other realistic metric)

**Description.** A proper scoring rule for **ordered** outcomes that accounts for the natural ordering
home > draw > away, penalizing predictions by how far off they are along that order. It is the metric of
choice in much of the football-forecasting literature.

**Pros.** **The most football-appropriate metric** — it respects the ordinal structure of 1X2 and is a
proper scoring rule, so it is honest and well-suited to the target and the probabilistic model.

**Cons.** **Obscure to a general reviewer** and not a one-line standard-library call, so it scores poorly
on reviewer comprehension and simplicity — and [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §2/§4
explicitly prefers *understandable* metrics over impressive-but-opaque ones. Overlaps with log loss /
Brier for everyday purposes.

**Risks.** Spending budget explaining an unfamiliar metric for marginal gain over log loss; better noted
as future work than adopted as core.

**Implementation effort.** **Medium** — must be implemented and explained.

**Portfolio suitability.** **Moderate** — excellent for a specialist audience, but at odds with the
reader-comprehension priority for *this* project.

**Fit score: 79 / 100.**

> **Other metrics considered and set aside.** **ROC-AUC / PR-AUC** are natural for the **binary
> fallback** (Home Win vs Not) and worth reporting *only if* that fallback is adopted; for the three-class
> target the one-vs-rest averaging is less intuitive than the confusion matrix and macro-F1. **Cohen's
> kappa** corrects accuracy for chance agreement but is less familiar than balanced accuracy.
> **Micro-F1** for a single-label multiclass problem collapses to accuracy and adds nothing. None
> displaces the eleven scored metrics.

---

## 7. Metric Comparison Table

Scores are 1–5 per criterion (see §2.1 rubric); the final column is the weighted Fit Score /100.
Abbreviations as in §4.

| Metric | Hon (×5) | PV (×5) | Rep (×5) | Ex (×4) | Rev (×4) | FB (×4) | Tgt (×4) | 40–60h (×4) | Mdl (×3) | Simp (×3) | **Fit /100** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Confusion Matrix** | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | **98** |
| **Macro F1** | 5 | 4 | 5 | 4 | 4 | 5 | 5 | 5 | 4 | 5 | **92** |
| **Log Loss** | 5 | 4 | 5 | 3 | 3 | 5 | 5 | 5 | 5 | 5 | **90** |
| **Brier Score** | 5 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 5 | 4 | **88** |
| **Recall (per class)** | 4 | 3 | 5 | 5 | 5 | 4 | 3 | 5 | 4 | 5 | **85** |
| **Balanced Accuracy** | 4 | 3 | 5 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | **83** |
| **Precision (per class)** | 4 | 3 | 5 | 5 | 5 | 3 | 3 | 5 | 4 | 5 | **83** |
| **Calibration assessment** | 5 | 4 | 5 | 4 | 3 | 5 | 4 | 3 | 5 | 3 | **83** |
| **F1 Score** | 4 | 4 | 5 | 4 | 3 | 4 | 3 | 5 | 4 | 5 | **82** |
| **Accuracy** | 2 | 4 | 5 | 5 | 5 | 3 | 3 | 5 | 4 | 5 | **81** |
| **Ranked Probability Score** | 5 | 3 | 5 | 3 | 2 | 5 | 5 | 3 | 5 | 3 | **79** |

> Weighted Fit = Σ(score × weight) ÷ 41 × 20, rounded to the nearest whole number.

---

## 8. Ranked Metric Recommendation

1. **Confusion Matrix** (98) — the indispensable reader-facing per-class diagnostic.
2. **Macro F1** (92) — the honest, imbalance-aware single scalar; surfaces the draw class.
3. **Log Loss** (90) — the primary proper scoring rule for probability quality vs. baseline.
4. **Brier Score** (88) — a second proper scoring rule; good optional companion to log loss.
5. **Recall (per class)** (85) — draw recall is the sharpest lens on the hard class.
6. **Balanced Accuracy** (83) · **Precision (per class)** (83) · **Calibration assessment** (83) —
   strong companions / optional polish.
9. **F1 Score** (82) — best reserved for the binary fallback.
10. **Accuracy** (81) — the intuitive headline, **only** when caveated and shown against the baseline.
11. **Ranked Probability Score** (79) — the football purist's metric, but too opaque for this audience.

> **Reading the ranking.** Probability-aware proper scoring rules (log loss, Brier) and per-class views
> (confusion matrix, macro-F1, per-class recall) rise to the top because they are **honest and
> imbalance-aware** — they cannot be flattered by a home-leaning predictor. Accuracy ranks lower *not*
> because it is useless but because, alone, it is the least honest on an imbalanced target; it earns its
> place only as a caveated, baseline-relative headline. RPS scores well on football fit but is held back
> by the reviewer-comprehension priority the spec sets above sophistication.

---

## 9. Recommendations

The recommendations below are **decision-support input** to
[`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §14 (final metrics, validation scheme, split
strategy, and success criteria), which remains the owning, deferred decision for the human to make.

### Recommended Train/Test Strategy

**A chronological hold-out split: train on the first four seasons (2020/21–2023/24) and test on the
held-out final season (2024/25).** (§3.2, fit 98)

- It is the **simplest scheme that respects chronological order** ([`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md)
  §7), so it is honest and leakage-free by construction.
- It mirrors the real prediction task ("use completed seasons to predict the next"), is trivially
  explained to any reviewer, and yields one clean baseline-vs-model comparison on genuinely unseen data.
- The final season is reserved as a **held-out test set touched once**, at the end, to avoid tuning to it.
- Its one weakness — a single test season is noisy — is addressed by the validation strategy below and by
  honestly stating the single-season caveat.

### Recommended Validation Strategy

**Season-blocked walk-forward (expanding-window) validation across the four training seasons**, used for
any model development, light regularization choices, coefficient-stability checks, and the
baseline-vs-model comparison *before* the final test. (§3.7 / §3.4, fits 97 / 91)

- Train on 2020/21 → validate on 2021/22; train on 2020/21–2021/22 → validate on 2022/23; train on
  2020/21–2022/23 → validate on 2023/24. The held-out 2024/25 season is **not** touched during
  development.
- This gives **several forward folds** for a stable, honest performance estimate on small data while
  never leaking the future, and reads as genuine ML judgment.
- Rolling features must be computed **within each fold's history only**, so no future match informs a
  prediction (leakage-avoidance, [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §6).
- **Budget fallback:** if walk-forward proves too costly, collapse to a **single chronological validation
  split** (hold out 2023/24 from training) — less precise, but still temporally honest and finishable.

### Recommended Metric Set

A **small, justified, understandable** set ([`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §4), all
reported **relative to the baseline** on the **same data and procedure** (§3), with per-class insight for
the draw class:

**Core (always reported):**

1. **Accuracy**, with an explicit home-bias caveat and a **balanced-accuracy** companion — the intuitive
   headline, kept honest. (§6.1, §6.2)
2. **Log Loss** — the primary proper scoring rule; the main "did the probabilities beat the baseline?"
   number, reported as an improvement over the baseline. (§6.3)
3. **Macro-F1** — per-class fairness; ensures the draw class is honestly weighed. (§6.6)
4. **Confusion Matrix** — the reader-facing per-class breakdown, with per-class **precision and recall**
   (especially **draw recall**) read off it. (§6.9, §6.7, §6.8)

**Optional (budget permitting, portfolio polish):**

5. **Brier Score** — a second proper scoring rule / calibration-adjacent check. (§6.4)
6. **Calibration (reliability) assessment** — a single reliability figure; easiest in the binary
   fallback's form. (§6.10)

**Deferred / situational:** **F1** and **ROC-AUC** become the natural headlines **only if the binary
fallback target is adopted**; **Ranked Probability Score** is noted as the football-purist's metric but
left to future work for being too opaque for this audience (§6.11).

> This is four core metrics plus one reader-facing diagnostic, with two optional extras — "few,
> justified, and clearly explained," honoring §4 and avoiding the "metric shopping" and "exhaustive
> benchmark suite" exclusions of §12.

### Recommended Success Criteria

Framed so that **honest evaluation, not a target number, defines success** — consistent with
[`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §3/§8 and the project's "honest > impressive"
operating principle ([`AGENTS.md`](../../AGENTS.md) §6). A null or marginal result is explicitly an
acceptable, publishable outcome.

**Primary (must-have) criteria — process and honesty:**

- The selected model is compared against the **home-advantage baseline** (and the majority-class floor)
  on the **same held-out data and procedure** (§3).
- The evaluation is **leakage-free and temporally honest** (chronological split + walk-forward
  validation; rolling features computed within-fold).
- Results are **reproducible** — deterministic with fixed seeds and a documented procedure
  ([`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md) §8).
- The **draw class is examined explicitly** (confusion matrix + draw recall), not hidden in an aggregate.
- Results are **interpreted in plain language** and **limitations/uncertainty are stated** (§8–§9), with
  no overclaiming.

**Secondary (target) criteria — performance, honestly framed:**

- The selected model **beats the home-advantage baseline on log loss** (better probabilities) **and on
  accuracy/macro-F1**, by a margin characterized honestly (stated as marginal if marginal).
- **Indicative, non-binding reference ranges** (to set expectations, *not* as pass/fail gates, and
  acknowledging no data has been inspected — §11): a home-advantage baseline accuracy in the low-to-mid
  **40s%** (the empty-stadium 2020/21 season likely lowers it), and a competent interpretable model in
  roughly the **high-40s to mid-50s%** — i.e. a **few points above the baseline**, not a dramatic leap.
  Published 1X2 models rarely exceed the mid-50s%; **this is the honest ceiling for the problem, not a
  shortfall of the project.**
- The model's probabilities are **reasonably calibrated** (if the optional calibration check is done).

**Explicitly acceptable outcomes (not failures):**

- A **weak or null improvement** over the baseline, reported honestly (§3) — football outcomes are
  genuinely hard, and an honest null is a credible portfolio result.
- **Poor draw-class performance**, reported as a valid finding rather than hidden
  ([`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md), "Draw-class considerations").

### Rationale (alignment with the specifications)

- **`PROJECT_OVERVIEW.md` — honesty & portfolio value.** A chronological hold-out plus walk-forward
  validation and a small, baseline-relative metric set is exactly the "honest comparison vs. baseline
  with a small, justified method set" the overview prizes, with no leaderboard chasing.
- **`EVALUATION_SPEC.md` — temporal integrity, small metric set, honest reporting.** The recommendation
  satisfies §3 (same data/procedure vs. baseline), §4 (few, understandable, target-matched metrics), §6
  (leakage avoidance), §7 (chronological order), §8–§9 (uncertainty, plain-language interpretation), and
  honors the §12 exclusions (no metric shopping, no exhaustive suites). It selects nothing the spec
  reserves — it **recommends**, leaving §14 to decide.
- **`MODELING_SPEC.md` — baseline-first, finishable.** Walk-forward validation supports an honest
  baseline → selected-model narrative (§4) within the complexity boundaries (§12); the metric set suits
  the multinomial logistic model's probabilistic outputs.
- **`EXPLAINABILITY_SPEC.md` — reader-first.** The confusion matrix, macro-F1, and a calibration figure
  are intuitive, reader-facing artifacts; the opaque RPS is down-ranked for failing the
  reviewer-comprehension priority.
- **`REPRODUCIBILITY_SPEC.md` — deterministic & laptop-friendly.** Every recommended scheme and metric is
  deterministic from the same data plus a fixed seed, documented, and re-runnable on a laptop across
  macOS and Windows 11, with no GPU/cloud dependency.
- **`PORTFOLIO_HANDOFF_SPEC.md` & `AGENTS.md` — finished, credible, honest.** The recommendation reads as
  competent, honest, and finishable, framing even a null result as a publishable outcome — protecting the
  three-project strategy and the "honest > impressive," "explainable > complex," "reproducible > clever"
  operating principles.

---

## 10. Risks Carried Into the Decision

| Risk | Affects | Mitigation at decision time |
|------|---------|------------------------------|
| Single test season is unrepresentative | Chronological hold-out | Pair with walk-forward validation; report the single-season caveat (§8 of the spec). |
| 2020/21 empty-stadium effect biases early folds | Walk-forward / training data | Report per-fold results; name the home-advantage anomaly explicitly. |
| Rolling-feature warm-up at season starts | All temporal schemes | Document the warm-up period; compute features within-fold to avoid leakage. |
| Temptation to peek at the held-out season | Train/test discipline | Touch 2024/25 once, at the end; do all development on the training seasons. |
| Metric set creep / metric shopping | Metric selection | Fix the small core set up front; treat extras as explicitly optional (§4, §12). |
| Accuracy over-claimed on an imbalanced target | Reporting | Always pair with macro-F1 + confusion matrix and the baseline reference. |
| Over-investing in calibration / RPS | Budget | Keep them optional; prefer understandable core metrics. |
| Reading log loss in absolute terms | Interpretation | Always report it as an improvement over the baseline, explained in words. |

---

## 11. Honest Limitations of This Analysis

- **No data was inspected or modelled** (per constraints); scores reflect each strategy's fit to the spec
  criteria and the known structure of the problem, not empirical results on the Bundesliga data. The
  indicative accuracy ranges in §9 are illustrative expectations, not measurements.
- **Fit scores are a structured judgment**, not a measurement; the **rankings and the explicit
  recommendations** are more meaningful than the exact decimals, and several mid-table candidates are
  deliberately close.
- **Reported-score maximization is intentionally under-weighted** — the rubric encodes the project's
  priorities (honesty, explainability, reproducibility, portfolio value), so schemes/metrics that could
  inflate a headline number (random split, k-fold, bare accuracy) rank low *for this project*, not in
  general.
- **No decision is finalized** — final metrics, the validation scheme, the split strategy, and
  target-specific success criteria remain deferred to
  [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) §14; this document changes no specification.

---

## 12. Next Natural Step

Review this analysis and **select the evaluation strategy** — recording the chosen train/test strategy,
validation strategy, metric set, and success criteria in
[`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md), per its deferred-decision table (§14). This document
is **non-binding input** to that decision; it makes no change to any spec, writes no code, and commits to
no implementation.

---

> **Conformance:** This research artifact respects the scope boundaries, non-goals, priorities, budget
> philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) and the
> downstream specifications. It introduces no new project requirements, modifies no specification,
> finalizes no evaluation decision, and commits to no implementation.
