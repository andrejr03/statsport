# StatSport — Feature Engineering Analysis

**Research / decision-support document**

> _A structured comparison of realistic Bundesliga feature groups against the StatSport specifications — to inform, but not to make, the final feature-engineering decision._

| | |
|---|---|
| **Status** | Research — for review |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Research artifact (informs `MODELING_SPEC.md`; conforms to all existing specifications) |
| **Parents** | [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](../specs/DATA_SPEC.md) · [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) · [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) · [`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md) · [`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md) · [`PORTFOLIO_HANDOFF_SPEC.md`](../specs/PORTFOLIO_HANDOFF_SPEC.md) · [`AGENTS.md`](../../AGENTS.md) |
| **Related** | [`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md) · [`PREDICTION_TARGET_ANALYSIS.md`](./PREDICTION_TARGET_ANALYSIS.md) |

> **What this document is:** a feature-engineering analysis performed *before* the feature decision. It
> identifies realistic feature groups achievable from the selected dataset, scores each against the
> StatSport specifications, and produces a ranked recommendation with explicit **core**, **optional**,
> and **excluded** sets. **It does not select the final feature set** — that decision is owned by
> [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) (its "Final feature set" remains a deferred decision)
> and is the human's to make. This document is **decision-support only**: it changes no specification
> and commits to no implementation.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total; one of three summer
> portfolio repositories.

---

## 1. Context and Scope

The dataset and prediction-target decisions are approved (see
[`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md),
[`PREDICTION_TARGET_ANALYSIS.md`](./PREDICTION_TARGET_ANALYSIS.md), and the corresponding decisions in
[`DATA_SPEC.md`](../specs/DATA_SPEC.md) and [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md)):

- **Source:** Football-Data.co.uk
- **League:** Bundesliga
- **Seasons:** 2020/21–2024/25 (five completed seasons)
- **Prediction target:** Home / Draw / Away (1X2), three-class classification
- **Fallback target:** Home Win vs Not Home Win, binary classification

The next major decision is the **feature-engineering strategy** — which derived inputs the model will
use. The final feature set is a deferred decision in [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md)
§9/§16. This document evaluates the candidate feature groups so the eventual choice is defensible,
documented, and traceable.

**Out of scope (by constraint):** modifying any spec, writing code, creating datasets/notebooks/scripts,
or committing to implementation. Selecting the feature set is the **next** step (§9).

### 1.1 What the selected data supports

Football-Data.co.uk Bundesliga rows provide, **per completed match**: the full-time result (H/D/A) and
half-time result; full-time and half-time goals for each side; and match-level event statistics —
shots (`HS`/`AS`), shots on target (`HST`/`AST`), corners (`HC`/`AC`), fouls (`HF`/`AF`), yellow cards
(`HY`/`AY`), and red cards (`HR`/`AR`) — plus the referee and bookmaker odds columns. The dataset
carries **no expected-goals (xG), possession, lineup, or player-level fields** (a known trade-off of
the dataset decision; see [`DATASET_CANDIDATE_ANALYSIS.md`](./DATASET_CANDIDATE_ANALYSIS.md)). Odds
columns will **not** be used as features or framing, consistent with the betting non-goal
(`PROJECT_OVERVIEW.md`, `AGENTS.md` §8).

### 1.2 The single most important constraint: pre-match only, no leakage

Every match-level statistic above (goals, shots, corners, cards, the result itself) is only known
**after** the match has been played. A feature for predicting a match may therefore use those values
**only from prior matches** — typically as a **rolling aggregate over a team's previous N fixtures**,
computed strictly from games that finished before the match being predicted. Using a match's own
post-match statistics as inputs would be **target/temporal leakage**, prohibited by
[`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) §11 and [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md)
§6–§7.

**Consequence:** almost every viable feature is some form of *rolling, pre-match, team-level history*.
This shapes the analysis below: data availability and reproducibility are high and broadly similar
across candidates (all derive deterministically from documented fields), so differentiation comes from
**portfolio value, explainability, modelling usefulness, feature stability, and implementation
effort** — and from how much **leakage discipline** each group demands.

---

## 2. Method

### 2.1 Scoring rubric

Each candidate feature group is scored **1 (poor) – 5 (excellent)** on the ten evaluation criteria.
Weights encode the inherited priority order (portfolio value → reproducibility → explainability →
evaluation quality → presentation clarity) and the finishability mandate. The **Fit Score /100** is the
weighted average rescaled: `Fit = Σ(score × weight) ÷ Σ(weight) × 20`, with `Σ(weight) = 39`.

| # | Criterion | Weight | What a 5 looks like |
|---|-----------|:------:|---------------------|
| 1 | Portfolio value | 5 | A recognizable, credible signal a reviewer respects |
| 2 | Explainability | 5 | Maps cleanly to plain-language football intuition |
| 3 | Reproducibility | 5 | Derived deterministically from documented fields |
| 4 | Modelling usefulness | 4 | Carries genuine predictive signal for the 1X2 target |
| 5 | Reviewer comprehension | 4 | A non-expert instantly grasps what the feature means |
| 6 | Data availability | 4 | Directly and cleanly available from the selected dataset |
| 7 | Fit for a 40–60 hour project | 4 | Cheap to build, leaving room for two more projects |
| 8 | Feature stability | 3 | Numerically stable; not dominated by noise or small samples |
| 9 | Implementation simplicity | 3 | Few moving parts; low leakage/edge-case risk |
| 10 | Long-term maintainability | 2 | Stable definition unlikely to need rework |

> **Note on criterion 9.** The brief lists "implementation complexity"; it is scored here as
> **implementation simplicity** (5 = simplest) so that, consistently with every other criterion, a
> higher score is better. Lower-effort groups score higher.

> **Caveat:** fit scores are a structured judgment encoding the inherited priorities, not a precise
> measurement. Other defensible weightings exist; the **ranking and the core/optional/excluded split**,
> not the decimal, are the point.

---

## 3. Candidate Feature Groups

> Throughout, "rolling" means *computed from a team's previous N completed matches only* (§1.2). A
> sensible default window (e.g. last 5 matches), season-boundary handling, and early-season warm-up are
> implementation details deferred to `MODELING_SPEC.md`; they are noted here only where they affect a
> group's score.

### 3.1 Home advantage features

**Description.** Encode the well-established home edge: a home/away indicator intrinsic to each fixture,
plus split histories such as the home team's record *at home* and the away team's record *away*.

**Pros.** The single most intuitive concept in football; immediately credible to any reviewer. Trivially
reproducible from results. Already the natural basis for the project's honest baseline (a home-advantage
/ majority-class prior, per `MODELING_SPEC.md` §4), so it ties the feature story directly to the
baseline narrative.

**Cons.** On its own it is low-dimensional and largely *already captured* by a home-advantage baseline,
so its marginal lift over that baseline is modest.

**Risks.** Minimal. The main caveat is not over-claiming novelty for what the baseline already encodes.

**Implementation effort.** **Very low** — an indicator plus simple home/away result splits.

**Explainability suitability.** **Excellent** — "home teams win more often" needs no explanation.

**Portfolio suitability.** **Excellent** — the canonical, recognizable football effect; anchors the
narrative.

**Fit score: 98 / 100.**

---

### 3.2 Recent form features

**Description.** A team's recent results expressed as form over its last N matches — e.g. points,
win/draw/loss counts, or an unbeaten run — for both the home and away side, pre-match.

**Pros.** Strong, intuitive predictor ("are they on a good run?") that every reader understands.
Deterministically derived from results. Pairs naturally with home advantage to tell most of the
match-outcome story.

**Cons.** Window length is a design choice; early-season rows have few prior matches (warm-up handling
needed). Overlaps heavily with **rolling points** (§3.7) — they are essentially the same family.

**Risks.** Small-sample noise early in each season; mild redundancy if combined naively with rolling
points and goal difference.

**Implementation effort.** **Low** — a rolling window over results, with season-boundary care.

**Explainability suitability.** **Excellent** — recent form is a household football concept.

**Portfolio suitability.** **Excellent** — a clear, expected, credible feature.

**Fit score: 96 / 100.**

---

### 3.3 Goals scored features

**Description.** Rolling average goals **scored** per match (attacking strength), pre-match, for each
side.

**Pros.** Direct, interpretable measure of attacking quality from the cleanest available field (goals).
Strong, well-behaved modelling signal. Fully reproducible.

**Cons.** Slightly noisier than results-based form over short windows; partially correlated with form
and goal difference.

**Risks.** Short-window volatility; redundancy with goals-conceded/goal-difference if all are included
without thought.

**Implementation effort.** **Low** — a rolling mean of a single clean column.

**Explainability suitability.** **Excellent** — "how many goals they usually score" is plain.

**Portfolio suitability.** **Strong** — expected and credible attacking signal.

**Fit score: 93 / 100.**

---

### 3.4 Goals conceded features

**Description.** Rolling average goals **conceded** per match (defensive strength), pre-match, for each
side.

**Pros.** The defensive counterpart to §3.3; together they summarize a team's two-way strength in
plain terms. Clean field, strong signal, fully reproducible.

**Cons.** Same short-window noise and correlation caveats as goals scored; combined with goals scored it
re-expresses much of goal difference.

**Risks.** Redundancy if goals scored, conceded, **and** goal difference are all added uncritically.

**Implementation effort.** **Low** — rolling mean of a single clean column.

**Explainability suitability.** **Excellent** — "how leaky their defence is" is intuitive.

**Portfolio suitability.** **Strong** — the natural defensive complement.

**Fit score: 93 / 100.**

---

### 3.5 Goal-difference features

**Description.** Rolling **net** goal difference (goals scored minus conceded) over the last N matches,
pre-match — a compact two-way strength summary.

**Pros.** Captures attack and defence in one interpretable number; correlates well with overall team
quality. Deterministic and cheap.

**Cons.** Largely a **combination of §3.3 and §3.4**; including all three adds little beyond what two of
them already say.

**Risks.** Redundancy/collinearity if used alongside both goals scored and goals conceded.

**Implementation effort.** **Low** — a subtraction over the two rolling means.

**Explainability suitability.** **Excellent** — net goals is widely understood (it is a league-table
tiebreaker).

**Portfolio suitability.** **Strong** — a tidy, recognizable strength proxy.

**Fit score: 91 / 100.**

---

### 3.6 League-position features

**Description.** Each team's current league-table position (and/or points total) **before** the match,
reconstructed from cumulative season results up to that matchday.

**Pros.** Highly intuitive standings context a reviewer instantly grasps ("3rd vs 17th"). Derived from
the same result data.

**Cons.** Requires **reconstructing the standings as of each matchday** (more steps and more edge cases
than a simple rolling window). Position **resets every season** and is noisy/uninformative in the first
few matchdays. As a coarse rank, it partly re-encodes accumulated form/points.

**Risks.** Early-season instability; off-by-one errors in "position *before* this match"; mild
redundancy with rolling points.

**Implementation effort.** **Medium** — cumulative standings per matchday, computed leak-free.

**Explainability suitability.** **Excellent** — table position is universally understood.

**Portfolio suitability.** **Strong** — recognizable, adds clear context.

**Fit score: 84 / 100.**

---

### 3.7 Rolling-points features

**Description.** Points accumulated over the last N matches (3 for a win, 1 for a draw), pre-match — a
numeric form measure.

**Pros.** Clean, numeric, strongly predictive form signal that feeds classical models well. Fully
reproducible and very intuitive.

**Cons.** **Essentially the same construct as recent form (§3.2)** and closely related to league points;
including both form and rolling points is double-counting.

**Risks.** Redundancy with §3.2/§3.6 if all are added; early-season small samples.

**Implementation effort.** **Low** — rolling sum of points from results.

**Explainability suitability.** **Excellent** — "points from the last five games" is plain.

**Portfolio suitability.** **Strong** — a standard, credible form encoding.

**Fit score: 93 / 100.**

> **Form vs rolling points:** §3.2 and §3.7 are two encodings of the same idea. Treat them as **one
> feature family** and implement a single, well-chosen version rather than both.

---

### 3.8 Shots features

**Description.** Rolling average shots **for** and **against** per match (`HS`/`AS`), pre-match — a proxy
for territorial/chance dominance.

**Pros.** Available directly from the dataset; interpretable as "how much a team tends to attack."
Reproducible. Adds an event-level dimension beyond pure results.

**Cons.** **Must be used as rolling pre-match aggregates** (leakage discipline, §1.2). Total shots are a
**noisy** proxy — many are low quality — so the marginal signal over goals/form is modest. More
volatile than results.

**Risks.** Leakage if a match's own shots leak in; over-weighting a noisy volume metric.

**Implementation effort.** **Medium** — rolling windows over event columns, with leakage care.

**Explainability suitability.** **Good** — shots are understandable but a coarser story than goals.

**Portfolio suitability.** **Strong** — shows use of richer match statistics.

**Fit score: 82 / 100.**

---

### 3.9 Shots-on-target features

**Description.** Rolling average shots **on target** for and against (`HST`/`AST`), pre-match — a
shot-**quality** proxy.

**Pros.** Better signal-to-noise than total shots; "shots on target" is an intuitive quality measure and
the strongest of the event-statistic groups. Available directly; reproducible.

**Cons.** Same rolling/leakage requirement as shots (§1.2); still noisier than goals; partially
correlated with goals scored.

**Risks.** Leakage discipline required; redundancy with goals scored.

**Implementation effort.** **Medium** — rolling windows over event columns, with leakage care.

**Explainability suitability.** **Excellent** — "how often they hit the target" is a clean quality story.

**Portfolio suitability.** **Strong** — the most defensible richer-statistic feature; shows judgment in
preferring quality over volume.

**Fit score: 86 / 100.**

---

### 3.10 Corner features

**Description.** Rolling average corners for and against (`HC`/`AC`), pre-match — a weak territorial
proxy.

**Pros.** Available; reproducible; cheap to compute alongside other rolling stats.

**Cons.** **Weak predictive value** and a tenuous link to winning; more corners ≠ better outcomes.
Somewhat betting-market flavored as a standalone metric. Adds dimensionality for little explanatory
payoff.

**Risks.** Noise; spurious importance; mild betting-framing optics (`AGENTS.md` §8).

**Implementation effort.** **Medium** — rolling windows over event columns, with leakage care.

**Explainability suitability.** **Moderate** — corners are familiar but only loosely tied to the result.

**Portfolio suitability.** **Weak** — adds little a reviewer would value.

**Fit score: 70 / 100.**

---

### 3.11 Card features

**Description.** Rolling average yellow/red cards (`HY`/`AY`/`HR`/`AR`), pre-match — a discipline proxy.

**Pros.** Available; reproducible.

**Cons.** **Weak, noisy** predictor that reflects refereeing and playing style as much as team quality;
red cards are rare and erratic over short windows. Little intuitive link to predicting the *next*
result. Poor signal for the budget it consumes.

**Risks.** High noise; very low marginal value; risk of reading importance into randomness.

**Implementation effort.** **Medium** — rolling windows over event columns, with leakage care.

**Explainability suitability.** **Moderate** — discipline is understandable but weakly tied to outcomes.

**Portfolio suitability.** **Weak** — not a signal a reviewer expects to matter.

**Fit score: 66 / 100.**

---

### 3.12 Elo-style rating features

**Description.** A running team-strength rating updated after each match by the result (and optionally
margin), carried across the season(s) — a single interpretable "strength" number per team, pre-match.

**Pros.** **High portfolio value** — Elo is a recognized, respected method and a strong "judgment"
signal. Compresses history into one intuitive strength figure with good explanatory power ("the stronger
side by rating"). Strong modelling signal that often rivals hand-built form features.

**Cons.** The **most complex** group here: requires an iterative update rule, a chosen K-factor and
initial ratings, and decisions on cross-season carry-over and promoted-team initialization. More design
surface means more places for subtle bugs and reproducibility slips.

**Risks.** Parameter/initialization choices must be fixed and documented for determinism
(`REPRODUCIBILITY_SPEC.md`); complexity can creep toward over-engineering (`MODELING_SPEC.md` §12).

**Implementation effort.** **Medium–High** — a deterministic but multi-step rating pipeline.

**Explainability suitability.** **Good** — a single strength number is intuitive, though the *update
mechanism* needs a sentence or two to explain.

**Portfolio suitability.** **Excellent** — the highest-value *optional* feature; demonstrates method
awareness.

**Fit score: 81 / 100.**

---

### 3.13 Strength-of-schedule features

**Description.** Adjust a team's form/goals for the quality of opponents faced — e.g. weighting recent
results by opponent strength.

**Pros.** Conceptually sound (form against strong teams means more) and analytically sophisticated.

**Cons.** Requires an **opponent-strength estimate first** (itself Elo- or position-derived), making it
**circular and the most complex** group; harder to explain plainly; more edge cases and a real
**complexity-creep risk** for limited marginal gain in a 40–60h budget.

**Risks.** Over-engineering (`MODELING_SPEC.md` §12); reproducibility and explainability both suffer as
complexity grows; weak payoff relative to effort.

**Implementation effort.** **High** — depends on a separate strength model and careful leak-free joins.

**Explainability suitability.** **Moderate** — the idea is intuitive but the construction is not.

**Portfolio suitability.** **Moderate** — impressive in principle, but its cost endangers finish.

**Fit score: 61 / 100.**

---

### 3.14 Other realistic Bundesliga features

A grab-bag of further features the dataset *could* support, assessed individually rather than as a
single block. The bundle's representative score reflects its mix.

- **Days of rest / fixture congestion** (from match dates): cheap, interpretable, mildly useful —
  **optional, if trivial.**
- **Season phase / matchday index** (early vs late season): cheap context that can stabilize
  early-season features — **optional, if trivial.**
- **Newly-promoted-team flag** (derivable from season-to-season participation): cheap, intuitive, modest
  value — **optional, if trivial.**
- **Head-to-head record** (this fixture's recent meetings): intuitive but **very small samples** per
  pairing, so noisy and of limited value — **lean exclude.**
- **Fouls** (`HF`/`AF`): similar to cards — weak, noisy — **lean exclude.**
- **Referee identity**: high-cardinality, weak link to outcomes, and invites bias framing — **exclude.**
- **Half-time result / half-time goals as features**: only legitimately usable from *prior* matches
  (post-match within a fixture); marginal over full-time form — **lean exclude.**
- **xG / possession / player-level features**: **not available** in the selected dataset — **excluded by
  data availability.**
- **Bookmaker odds as features**: available but **off-limits** under the betting non-goal
  (`PROJECT_OVERVIEW.md`, `AGENTS.md` §8) — **excluded by principle.**

**Pros.** A few items (rest days, season phase, promoted flag) are cheap and add light, interpretable
context.

**Cons.** Most items are noisy, niche, unavailable, or principle-excluded; collectively they risk scope
creep for little gain.

**Risks.** Dimensionality and complexity creep; betting-framing optics for odds; bias optics for
referee.

**Implementation effort.** **Low–Medium** for the cheap items; higher for head-to-head joins.

**Explainability suitability.** **Good** for the cheap contextual items; weaker elsewhere.

**Portfolio suitability.** **Moderate** — minor polish at best.

**Fit score: 69 / 100** *(bundle average; the cheap contextual items score higher individually than the
noisy/excluded ones).*

---

## 4. Feature Comparison Table

Scores are 1–5 per criterion (see §2.1 rubric); the final column is the weighted Fit Score /100.
Abbreviations: **PV** portfolio value, **Ex** explainability, **Rep** reproducibility, **Mod** modelling
usefulness, **Rev** reviewer comprehension, **Data** data availability, **40–60h** budget fit, **Stab**
feature stability, **Simp** implementation simplicity, **Maint** maintainability.

| Feature group | PV (×5) | Ex (×5) | Rep (×5) | Mod (×4) | Rev (×4) | Data (×4) | 40–60h (×4) | Stab (×3) | Simp (×3) | Maint (×2) | **Fit /100** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Home advantage** | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | **98** |
| **Recent form** | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 4 | **96** |
| **Goals scored** | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 4 | **93** |
| **Goals conceded** | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 4 | **93** |
| **Rolling points** | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 4 | **93** |
| **Goal difference** | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 4 | **91** |
| **Shots on target** | 4 | 5 | 5 | 4 | 5 | 5 | 4 | 3 | 3 | 4 | **86** |
| **League position** | 5 | 5 | 4 | 4 | 5 | 4 | 4 | 3 | 3 | 4 | **84** |
| **Shots** | 4 | 4 | 5 | 4 | 4 | 5 | 4 | 3 | 3 | 4 | **82** |
| **Elo-style rating** | 5 | 4 | 4 | 5 | 4 | 5 | 3 | 4 | 2 | 3 | **81** |
| **Corners** | 2 | 3 | 5 | 3 | 3 | 5 | 4 | 3 | 3 | 4 | **70** |
| **Other (bundle)** | 3 | 4 | 4 | 3 | 4 | 4 | 3 | 3 | 3 | 3 | **69** |
| **Cards** | 2 | 3 | 5 | 2 | 3 | 5 | 4 | 2 | 3 | 4 | **66** |
| **Strength of schedule** | 3 | 3 | 3 | 4 | 3 | 4 | 2 | 3 | 2 | 3 | **61** |

> Weighted Fit = Σ(score × weight) ÷ 39 × 20, rounded to the nearest whole number.

---

## 5. Ranked Recommendation

1. **Home advantage** (98) — the canonical, baseline-anchoring effect.
2. **Recent form** (96) — the strongest intuitive results-based signal.
3. **Goals scored** (93) — clean attacking strength.
3. **Goals conceded** (93) — clean defensive strength.
3. **Rolling points** (93) — numeric form *(same family as recent form)*.
6. **Goal difference** (91) — compact two-way strength summary.
7. **Shots on target** (86) — best event-statistic feature (shot quality).
8. **League position** (84) — intuitive standings context (reconstruction cost).
9. **Shots** (82) — territorial proxy, noisier than SOT.
10. **Elo-style rating** (81) — highest-value optional; higher complexity.
11. **Corners** (70) — weak link to outcomes.
12. **Other (bundle)** (69) — a few cheap items; mostly noisy/excluded.
13. **Cards** (66) — noisy discipline proxy.
14. **Strength of schedule** (61) — sophisticated but circular and costly.

> **Reading the ranking.** The top six are all **result-derived, leakage-trivial, and maximally
> interpretable** — they cluster tightly because they best satisfy the highest-weighted criteria. Below
> them sit features that are valuable but cost more in either **leakage discipline** (event statistics)
> or **complexity** (Elo, league position), and then the weak/noisy/principle-excluded tail.

---

## 6. Recommended Core Feature Set

**Features that should almost certainly be included.** All are result-derived, deterministic, trivially
leakage-safe, and maximally interpretable — the spine of the model and the explainability narrative.

- **Home advantage** (§3.1) — fixture home/away encoding plus home/away result splits.
- **Recent form** (§3.2) — rolling results form over the last N matches. *(Implement the form / rolling-
  points family **once**; see §3.7.)*
- **Goals scored** (§3.3) — rolling attacking rate.
- **Goals conceded** (§3.4) — rolling defensive rate.
- **Goal difference** (§3.5) — rolling net strength, as a compact summary.

> **Manage redundancy deliberately.** Form, rolling points, and goal difference overlap with goals
> scored/conceded. A defensible compact core is *home advantage + a single form encoding + goals
> scored + goals conceded*, optionally adding goal difference as a tidy summary. The point is a
> **small, coherent, non-redundant** set (`MODELING_SPEC.md` §9), not "all six regardless."

---

## 7. Recommended Optional Feature Set

**Features worth considering if implementation remains simple** — they add genuine value but cost more
in leakage discipline, reconstruction, or complexity. Add in this order, only while the budget and
simplicity mandate hold.

- **Shots on target** (§3.9) — the strongest event-statistic feature; preferred over raw shots. Requires
  rolling, pre-match aggregation (§1.2).
- **League position** (§3.6) — intuitive standings context; include if the leak-free standings
  reconstruction stays cheap.
- **Elo-style rating** (§3.12) — the single highest-value *impressive* optional; include **one**
  well-documented, deterministic rating if budget allows, and skip it the moment it threatens finish.
- **Shots (total)** (§3.8) — only if shots-on-target is insufficient and a volume proxy is wanted.
- **Cheap contextual items from §3.14** — days of rest, season phase/matchday, newly-promoted flag —
  each added only if genuinely trivial.

> **Guardrail.** These are *additions to* a working core, not prerequisites. Each must earn its place
> against the baseline (`MODELING_SPEC.md` §4; `EVALUATION_SPEC.md` §3) and must not push the project
> past the budget or into complexity creep (`MODELING_SPEC.md` §12).

---

## 8. Recommended Excluded Feature Set

**Features that should probably be avoided** — they increase complexity, dimensionality, or noise
without enough portfolio value, or are excluded by data/principle.

- **Corner features** (§3.10) — weak link to outcomes; betting-flavored as a standalone.
- **Card features** (§3.11) — noisy discipline proxy; reflects style/refereeing more than quality.
- **Strength-of-schedule features** (§3.13) — circular, complex, and a real complexity-creep risk for
  limited gain (`MODELING_SPEC.md` §12).
- **Fouls, referee identity, head-to-head, half-time-as-feature** (§3.14) — noisy, niche, high-cardinality,
  or marginal over full-time form.
- **Bookmaker odds as features** — excluded by the betting non-goal (`PROJECT_OVERVIEW.md`, `AGENTS.md` §8).
- **xG, possession, player-level features** — **not available** in the selected dataset.

> Exclusion here means *out of the default plan*, not "never." Any excluded item could be revisited as
> explicit "future work," but none earns a place in a finishable 40–60h portfolio build.

---

## 9. Rationale (alignment with the specifications)

- **`PROJECT_OVERVIEW.md` — portfolio value & scope.** The core set is the recognizable, expected feature
  spine of a football predictor — the strongest, cleanest signal to reviewers — while staying bounded
  and clear of the betting non-goal (so corners/cards/odds are
  down-weighted or excluded). A modest, justified feature set respects the scope-creep guardrails.
- **`DATA_SPEC.md` — available, deterministic, laptop-friendly.** Every recommended feature derives
  deterministically from documented Football-Data.co.uk fields; nothing requires scraping, external
  data, or unavailable signals (xG/possession), consistent with the dataset decision.
- **`MODELING_SPEC.md` — interpretable, baseline-first, finishable.** The core features are exactly the
  inputs that suit classical, interpretable families (logistic/tree models) and that a home-advantage /
  majority-class baseline naturally extends. Feature work stays "modest and justified" (§9) and clear of
  the complexity boundaries (§12); Elo and strength-of-schedule are correctly sorted into *optional* and
  *excluded* on those grounds.
- **`EVALUATION_SPEC.md` — leakage-safe and honest.** §1.2 makes the pre-match, rolling-only discipline
  explicit, directly satisfying the leakage-avoidance and temporal-integrity rules (§6–§7). Keeping the
  set small supports honest, baseline-relative evaluation rather than feature-driven overfitting.
- **`EXPLAINABILITY_SPEC.md` — reader-first.** Each core feature maps to a plain-language driver (home
  edge, recent form, attacking/defensive strength), enabling intuitive local and global explanations for
  a non-expert reader; noisy features that explain poorly (corners, cards) are excluded.
- **`REPRODUCIBILITY_SPEC.md` — deterministic & traceable.** All recommended features are regenerable
  from raw data via documented rolling computations; the one stateful optional (Elo) is flagged as
  needing fixed, documented parameters to stay deterministic.
- **`PORTFOLIO_HANDOFF_SPEC.md` & `AGENTS.md` — finished, credible, in-scope.** A compact, well-chosen
  feature set reads as competent and finished, tells a coherent narrative, and protects finishability —
  the skill the portfolio is meant to demonstrate.

---

## 10. Risks Carried Into the Decision

| Risk | Affects | Mitigation at decision time |
|------|---------|------------------------------|
| Target/temporal leakage | All event & result features | Use rolling, pre-match-only aggregates (§1.2); review feature provenance (`EVALUATION_SPEC.md` §6–§7). |
| Feature redundancy / collinearity | Form, rolling points, goal difference, goals scored/conceded | Pick a single form encoding; treat goal difference as a summary, not an addition; keep the set compact. |
| Complexity creep | Elo, strength of schedule | Keep Elo optional with fixed documented params; exclude strength of schedule (`MODELING_SPEC.md` §12). |
| Early-season small samples | Form, rolling points, league position | Define window warm-up and season-boundary handling; document it. |
| Noisy low-value features | Corners, cards, fouls | Exclude by default; revisit only as future work. |
| Betting-framing optics | Odds, corners | Never use odds as features; down-weight betting-flavored metrics (`AGENTS.md` §8). |
| Scope creep toward richer signals | xG, possession, player data | Not supported by the selected data; hold the bounded plan. |

---

## 11. Honest Limitations of This Analysis

- **No data was inspected or modelled** (per constraints); scores reflect feature characteristics and the
  spec criteria, not empirical predictive importance measured on the Bundesliga data.
- **Fit scores are a structured judgment**, not a measurement; the **ranking and the
  core/optional/excluded split** are more meaningful than the exact number, and the top cluster is
  deliberately close.
- **Excluded features are penalized on value/complexity/optics, not on legality** — corners, cards, and
  the like remain computable; the penalty reflects weak signal and portfolio/budget fit under the
  project's priorities.
- **Redundancy is a judgment call** — the overlapping result-based features could be consolidated
  differently; the recommendation favors a compact, non-redundant core over maximal coverage.

---

## 12. Next Natural Step

Review this analysis and **select the feature strategy** — recording the chosen core/optional set (and
the leakage-safe rolling definitions) in [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md), per its
deferred-decision table (§16, "Final feature set"). This document is **non-binding input** to that
decision; it makes no change to any spec and commits to no implementation.

---

> **Conformance:** This research artifact respects the scope boundaries, non-goals, priorities, budget
> philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) and
> the downstream specifications. It introduces no new project requirements, modifies no specification,
> and does not finalize the feature-engineering decision.
