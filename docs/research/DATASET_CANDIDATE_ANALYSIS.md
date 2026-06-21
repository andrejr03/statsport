# StatSport — Dataset Candidate Analysis

**Research / decision-support document**

> _A structured comparison of realistic public football datasets against the StatSport specifications — to inform, but not to make, the final dataset decision._

| | |
|---|---|
| **Status** | Research — for review |
| **Version** | 0.1 (draft) |
| **Author** | André |
| **Date** | 2026-06-20 |
| **Document type** | Research artifact (informs `DATA_SPEC.md`; conforms to all existing specifications) |
| **Parents** | [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) · [`DATA_SPEC.md`](../specs/DATA_SPEC.md) · [`MODELING_SPEC.md`](../specs/MODELING_SPEC.md) · [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md) · [`EXPLAINABILITY_SPEC.md`](../specs/EXPLAINABILITY_SPEC.md) · [`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md) · [`PORTFOLIO_HANDOFF_SPEC.md`](../specs/PORTFOLIO_HANDOFF_SPEC.md) · [`AGENTS.md`](../../AGENTS.md) |

> **What this document is:** a candidate analysis performed *before* dataset selection. It identifies
> and compares realistic public football datasets, scores each against the StatSport specifications,
> and produces a ranked recommendation with a primary choice and a fallback. **It does not select the
> final dataset, source, league, or season range** — that decision is deferred to `DATA_SPEC.md` and
> remains the human's to make. This document changes no specification and commits to no implementation.
>
> **Inherited priorities (in order):** 1. Portfolio value · 2. Reproducibility · 3. Explainability ·
> 4. Evaluation quality · 5. Presentation clarity. **Budget:** 40–60 hours total; one of three summer
> portfolio repositories.

---

## 1. Purpose and Scope

The StatSport specification suite is complete and approved. The next decision in dependency order is
**dataset selection** (owned by [`DATA_SPEC.md`](../specs/DATA_SPEC.md), per the deferred-decision
model in [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md)). Rather than pick a dataset by reflex,
this document performs a disciplined candidate analysis so that the eventual choice is defensible,
documented, and traceable — consistent with the project's honesty and reproducibility priorities.

**In scope:** identifying realistic candidate datasets, evaluating them against the specs, and ranking
them with a recommendation and a fallback.

**Out of scope (by constraint):** modifying any spec, writing code, downloading data, or committing to
a final implementation. The final selection is the **next** step (§12).

---

## 2. Method

Each candidate is evaluated in two passes:

1. **Hard gate** — Does it satisfy the mandatory eligibility rules in `DATA_SPEC.md`
   [§5 (Selection Criteria)](../specs/DATA_SPEC.md) and avoid every disqualifier in
   [§6 (Exclusion Criteria)](../specs/DATA_SPEC.md)? A candidate that fails the gate cannot be the
   primary recommendation regardless of how attractive it is otherwise.
2. **Weighted fit** — For candidates that pass (or nearly pass) the gate, score the twelve evaluation
   criteria below and compute an overall **Fit Score / 100**.

### 2.1 The hard gate (from `DATA_SPEC.md`)

A candidate must be **publicly obtainable**, **legally usable in a public repo**, **reasonably
documented**, **reproducibly re-acquirable**, and **sized for a 40–60 hour laptop project**
(§5). It is **disqualified** if it requires real-time feeds, paid/subscription data, proprietary
non-shareable data, massive multi-league archives, **complex/fragile scraping infrastructure**, or
cloud-scale processing (§6). Note that StatSport commits the *acquisition process and documentation*,
not the data itself (`DATA_SPEC.md` §8, §14), so a dataset whose terms forbid *redistribution* can
still qualify if its terms permit *use* and reproducible *re-acquisition*.

### 2.2 Evaluation criteria and scoring rubric

Each criterion is scored **1 (poor) – 5 (excellent)**. Weights reflect the inherited priority order
(portfolio value → reproducibility → explainability → evaluation quality → presentation clarity) and
the finishability mandate. The Fit Score is the weighted average rescaled to /100.

| # | Criterion | Weight | What a 5 looks like |
|---|-----------|:------:|---------------------|
| 1 | Public availability | 3 | Freely downloadable by anyone, no gatekeeping |
| 2 | Licensing clarity | 5 | Explicit, permissive, unambiguous terms for public-portfolio use |
| 3 | Reproducibility | 5 | Deterministic, stable, re-acquirable by a stranger years later |
| 4 | Data quality | 4 | Clean, consistent fields; manageable, documented missingness |
| 5 | Documentation quality | 3 | Fields and provenance clearly described |
| 6 | Ease of acquisition | 4 | One simple, non-fragile step; no scraping pipeline |
| 7 | Feature-engineering potential | 4 | Rich, interpretable signals beyond bare scores |
| 8 | Explainability suitability | 4 | Features map to plain-language football intuition |
| 9 | Portfolio value | 5 | Reads as competent, credible, recognizable to a reviewer |
| 10 | Fit for a 40–60 hour project | 5 | Comfortably finishable with room for two more projects |
| 11 | Laptop-friendliness | 3 | Loads/processes in memory on a typical laptop |
| 12 | Long-term maintainability | 3 | Source stable; unlikely to vanish or silently change |

> **Caveat (read before relying on the licensing column):** licensing notes below are a good-faith
> reading of publicly stated terms as understood on the document date, **not legal advice**. Per
> `DATA_SPEC.md` §8 and §16, the chosen source's license/terms must be **re-verified and recorded**
> at acquisition time. Where terms are ambiguous, the spec says to **exclude** — so ambiguity is
> scored harshly here on purpose.

---

## 3. Candidate Datasets

Five candidate families are assessed, covering the sources named in the task plus the strongest
"other realistic public" options.

### 3.1 Football-Data.co.uk

**Description.** Free, long-running archive of historical results for the major European leagues
(England, Spain, Italy, Germany, France, and more), distributed as small per-season, per-division CSV
files via a stable, predictable URL scheme (e.g., one CSV per division per season). Each match row
carries the result and a useful set of **match-level statistics** — full-time and half-time goals and
result (a clean home/draw/away label), plus shots, shots on target, corners, fouls, and yellow/red
cards — alongside extensive bookmaker odds columns (which StatSport can simply ignore to stay clear of
any betting framing per `PROJECT_OVERVIEW.md` non-goals).

**Pros.**
- Clean, bounded slice is trivial: pick one league + a handful of recent seasons.
- A ready-made, well-defined classification target (home/draw/away result).
- Match-level stats (shots, corners, cards) give genuinely **interpretable** features without scraping.
- Tiny CSVs — instantly laptop-friendly and cross-platform (plain download, no tooling).
- Stable, conventional URLs make deterministic re-acquisition straightforward.
- Widely recognized in football analytics — credible to a reviewer.

**Cons.**
- Per-match stats are basic (no xG/possession); richer "modern analytics" signals are absent.
- A short notes/column glossary exists but is terse; some columns need interpretation.
- No formal open-source license badge; terms are stated as free-to-use rather than a named license.

**Risks.**
- Licensing is *permissive but informal* — must be read and recorded at acquisition (mitigated by
  committing process, not data, per `DATA_SPEC.md` §8/§14).
- Column set has drifted slightly across older seasons; bounding to recent seasons mitigates this.
- Single-maintainer site — small long-term availability risk (mitigated by recording provenance and
  acquisition date per `DATA_SPEC.md` §16).

**Estimated implementation effort.** **Low.** ~6–10 hours for acquisition + cleaning to a tidy,
model-ready table, well inside budget.

**Fit score: 88 / 100.**

---

### 3.2 Kaggle football datasets (incl. the "European Soccer Database")

**Description.** A broad category rather than one dataset. The most prominent is the *European Soccer
Database* (a SQLite file covering ~25k matches across ~11 European countries for roughly 2008–2016,
with odds, lineups, and FIFA-derived player attributes). Many other community-uploaded football
datasets also exist with varying scope and quality.

**Pros.**
- Often pre-cleaned and convenient; the European Soccer Database is rich (player attributes, lineups).
- Kaggle's API enables deterministic acquisition by dataset slug **and version**.
- Large, varied selection — easy to find something close to a desired scope.

**Cons.**
- **Licensing varies per dataset and is frequently unclear** — many are re-uploads of scraped data
  with murky provenance (a direct tension with `DATA_SPEC.md` §8, which excludes ambiguous licensing).
- Acquisition requires a **Kaggle account/API token**, adding a gatekeeping step that slightly weakens
  "publicly obtainable without privileged access."
- The European Soccer Database is **stale** (ends ~2016) and effectively unmaintained.
- Player-attribute richness invites scope creep beyond the bounded plan.

**Risks.**
- Datasets can be removed or re-versioned by uploaders — a real maintainability/reproducibility risk.
- Unclear provenance can mean undocumented quality issues (conflicts with the honesty priority).
- Account requirement complicates a "stranger can reproduce this" story.

**Estimated implementation effort.** **Low–Medium.** ~8–14 hours; SQLite extraction and scope trimming
add modest overhead, and license due-diligence is non-trivial.

**Fit score: 66 / 100** (European Soccer Database specifically; the broader category varies widely).

---

### 3.3 Understat-derived datasets (xG data)

**Description.** Understat publishes expected-goals (xG) data for the top European leagues. It has no
official public API or stated data license; data is typically obtained by scraping the site or via
community packages, or via second-hand Kaggle dumps.

**Pros.**
- **xG is a superb explainability and feature-engineering signal** — directly interpretable as
  "chance quality," ideal for the reader-first narrative in `EXPLAINABILITY_SPEC.md`.
- Bounded by league/season, so scope control is feasible.

**Cons.**
- **No stated license** → licensing ambiguity, which `DATA_SPEC.md` §8 treats as grounds to exclude.
- Primary acquisition is **scraping** (or wrapper libraries around scraping), colliding with the
  exclusion of "complex/fragile scraping infrastructure" (`DATA_SPEC.md` §6).
- Second-hand Kaggle dumps inherit both the licensing ambiguity and staleness problems of §3.2.

**Risks.**
- Site structure or terms can change, breaking reproducibility (`DATA_SPEC.md` §17 reproducibility drift).
- Legal/terms ambiguity is a credibility risk for a public portfolio repo.

**Estimated implementation effort.** **Medium–High.** ~12–20 hours including building and hardening a
scrape, with ongoing fragility — and it still doesn't resolve the licensing gate.

**Fit score: 52 / 100** (gated down hard by licensing ambiguity + scraping).

---

### 3.4 FBref-derived datasets (Sports Reference / StatsBomb-powered)

**Description.** FBref (Sports Reference) hosts very rich modern football statistics — xG, possession,
passing, defensive actions — for many competitions. Programmatic access is via community scraping
packages subject to rate limits.

**Pros.**
- The **richest interpretable feature set** of any candidate — excellent in principle for explainability.
- Broad competition/season coverage.

**Cons.**
- Sports Reference's terms **restrict bulk scraping and redistribution**; bulk use is discouraged
  (a direct tension with `DATA_SPEC.md` §6/§8).
- Access is **rate-limited scraping** — a fragile, multi-step pipeline the data spec explicitly excludes.
- The wealth of tables invites scope creep beyond a 40–60 hour budget.

**Risks.**
- Terms changes or rate-limit tightening can break acquisition and reproducibility.
- Redistribution constraints complicate even the "commit the process" model.

**Estimated implementation effort.** **High.** ~16–24 hours to build a polite, rate-limited, resumable
scraper — and it still fails the scraping/licensing gate.

**Fit score: 50 / 100** (gated down by licensing posture + fragile scraping).

---

### 3.5 Other realistic public datasets

#### 3.5a openfootball / football.db
**Description.** A community, **public-domain (CC0-style)** collection of football *results* across many
leagues and seasons, distributed via a public Git repository in plain-text/structured formats.

**Pros.**
- **Best-in-class licensing and reproducibility** — public domain, version-controlled, re-acquirable by
  cloning a stable repo. No account, no scraping.
- Trivially laptop-friendly and cross-platform.

**Cons.**
- **Results-only** (scores/fixtures); little or no per-match shot/card data, so rich features must be
  **engineered** (rolling form, goal difference, simple Elo-style ratings) rather than ingested.
- Field richness is the lowest of the strong candidates.

**Risks.**
- Thinner raw signal can cap the modelling/explainability ceiling — though engineered features remain
  fully interpretable and on-spec.

**Estimated implementation effort.** **Low.** ~6–10 hours; more time shifts into (interpretable) feature
engineering rather than acquisition.

**Fit score: 80 / 100.**

#### 3.5b StatsBomb Open Data
**Description.** Free **event-level** data for selected competitions, under a non-commercial license with
attribution conditions.

**Pros.** Extremely rich; outstanding for deep analysis and explainability in principle.

**Cons.** **Event-level volume and complexity** push parsing/aggregation effort toward (or past) the
budget ceiling; **non-commercial** terms and competition-specific coverage make it a poor fit for a
bounded league-season "match outcome" framing. Risks budget overrun (`MODELING_SPEC.md` §15).

**Estimated implementation effort.** **High.** ~18–28 hours just to wrangle event data into a tidy
match-level table.

**Fit score: 58 / 100** (great data, wrong shape/effort for this budget).

#### 3.5c Results-only packages (e.g., engsoccerdata) / CC0 international-results sets
**Description.** Clean, permissively licensed historical **results** (club or international) shipped via
packages or single CSVs.

**Pros.** Clean and permissively licensed; easy.
**Cons.** Results-only (like openfootball); international-results variants aren't club-league-bounded.

**Estimated implementation effort.** **Low.** ~5–9 hours.

**Fit score: 74 / 100.**

---

## 4. Candidate Comparison Table

Scores are 1–5 per criterion (see §2.2 rubric); the final column is the weighted Fit Score /100.

| Candidate | Avail. (×3) | License (×5) | Reprod. (×5) | Quality (×4) | Docs (×3) | Acquis. (×4) | Feat.Eng (×4) | Explain (×4) | Portfolio (×5) | 40–60h Fit (×5) | Laptop (×3) | Maint. (×3) | **Fit /100** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Football-Data.co.uk** | 5 | 4 | 5 | 4 | 3 | 5 | 4 | 4 | 5 | 5 | 5 | 4 | **88** |
| **openfootball / football.db** | 5 | 5 | 5 | 4 | 3 | 5 | 3 | 4 | 4 | 5 | 5 | 4 | **80** |
| Results-only packages (CC0) | 5 | 5 | 4 | 4 | 3 | 4 | 2 | 3 | 4 | 5 | 5 | 4 | **74** |
| Kaggle European Soccer DB | 4 | 2 | 3 | 4 | 3 | 4 | 4 | 4 | 4 | 3 | 4 | 2 | **66** |
| StatsBomb Open Data | 4 | 3 | 4 | 5 | 4 | 3 | 5 | 5 | 4 | 2 | 3 | 4 | **58** |
| Understat-derived (xG) | 4 | 2 | 2 | 4 | 3 | 2 | 5 | 5 | 4 | 3 | 4 | 2 | **52** |
| FBref-derived | 4 | 2 | 2 | 5 | 4 | 1 | 5 | 5 | 4 | 2 | 3 | 2 | **50** |

> Weighted Fit = Σ(score × weight) ÷ Σ(weight) × 20, where Σ(weight) = 48. Values rounded to the
> nearest whole number.

---

## 5. Hard-Gate Summary

| Candidate | Passes `DATA_SPEC.md` §5/§6 gate? | Decisive factor |
|---|:--:|---|
| Football-Data.co.uk | ✅ Yes | Free, stable, no scraping; informal-but-permissive terms to record at acquisition |
| openfootball / football.db | ✅ Yes | Public domain + Git = cleanest gate pass |
| Results-only packages (CC0) | ✅ Yes | Permissive license, simple acquisition |
| Kaggle European Soccer DB | ⚠️ Marginal | Licensing/provenance ambiguity + account gate + staleness |
| StatsBomb Open Data | ⚠️ Marginal | Non-commercial terms OK-ish, but effort shape risks the budget gate |
| Understat-derived (xG) | ❌ No | Licensing ambiguity **and** scraping dependency |
| FBref-derived | ❌ No | Redistribution/scraping posture + fragile rate-limited pipeline |

---

## 6. Ranked Recommendation

1. **Football-Data.co.uk** — best overall balance; clears the gate and tops the weighted score.
2. **openfootball / football.db** — strongest licensing/reproducibility; the safest fallback.
3. **Results-only CC0 packages** — clean and easy, but the thinnest feature ceiling.
4. **Kaggle European Soccer Database** — rich but licensing-ambiguous, account-gated, and stale.
5. **StatsBomb Open Data** — superb data, wrong shape and effort profile for this budget.
6. **Understat-derived (xG)** — excellent signal, blocked by licensing + scraping.
7. **FBref-derived** — richest data, blocked hardest by licensing posture + fragile scraping.

---

## 7. Recommended Dataset

**Football-Data.co.uk — a single league across a bounded set of recent seasons** (the exact league and
season range to be fixed in `DATA_SPEC.md`).

It is the only candidate that simultaneously: (a) passes the hard gate cleanly without scraping,
(b) ships a ready-made, well-defined classification target (home/draw/away), (c) carries
**interpretable** match-level features (shots, shots on target, corners, cards) that suit the
explainability mandate, and (d) is small enough to finish comfortably inside 40–60 hours with room for
two further projects. Its only material weakness — informal (rather than badged) licensing — is
manageable because StatSport commits the *acquisition process and documentation*, not the data, and
records the terms at acquisition time.

---

## 8. Recommended Fallback Dataset

**openfootball / football.db** (public-domain, Git-distributed results).

It is the most bulletproof candidate on the two highest-weighted gate concerns — **licensing clarity**
and **reproducibility** — and requires no account and no scraping. Its trade-off is that it is
results-only, so the modelling layer leans on **engineered** features (rolling form, goal difference,
simple rating systems). Those features are themselves fully interpretable and on-spec, so the fallback
preserves the explainability and honesty priorities even though its raw signal is thinner. It is the
right safety net if Football-Data.co.uk's terms, column drift, or availability prove problematic.

---

## 9. Rationale

- **Priority alignment.** The inherited order is portfolio value → reproducibility → explainability →
  evaluation quality → presentation clarity. Football-Data.co.uk scores at or near the top on every
  one of these while clearing the hard gate; openfootball wins outright on reproducibility/licensing,
  making the pair complementary.
- **Gate discipline.** `DATA_SPEC.md` §6 excludes fragile scraping and ambiguous licensing. That alone
  removes the two richest sources (Understat, FBref) from primary contention despite their analytic
  appeal — exactly the kind of honest trade-off the specs ask for.
- **Budget realism.** `PROJECT_OVERVIEW.md` makes 40–60 hours a first-class constraint. The recommended
  pair are both **low-effort** to acquire (~6–10 hours), leaving the budget for modelling, honest
  evaluation, and reader-facing explanation rather than data plumbing. StatsBomb's event data, by
  contrast, would spend much of the budget before any modelling begins.
- **Explainability fit.** Both recommendations yield features a non-expert can understand — raw
  match stats (Football-Data) or transparent engineered features (openfootball) — satisfying
  `EXPLAINABILITY_SPEC.md`'s reader-first principle without exotic signals.
- **Maintainability and honesty.** Recording provenance, license, scope, and acquisition date
  (`DATA_SPEC.md` §16) mitigates the single-maintainer availability risk of Football-Data.co.uk and
  keeps the project re-creatable by a stranger, as `REPRODUCIBILITY_SPEC.md` §4 requires.

---

## 10. Risks Carried Into Selection

| Risk | Affects | Mitigation at selection time |
|------|---------|------------------------------|
| Informal licensing terms | Football-Data.co.uk | Read and record terms verbatim; rely on the commit-process-not-data model (`DATA_SPEC.md` §8/§14). |
| Source availability over time | Football-Data.co.uk | Record acquisition date + provenance; keep openfootball as the documented fallback. |
| Thin raw features | openfootball fallback | Pre-plan interpretable engineered features; keep them modest (`MODELING_SPEC.md` §9). |
| Column drift across seasons | Football-Data.co.uk | Bound to recent seasons with a consistent schema. |
| Scope creep via richer sources | xG/FBref/StatsBomb | Hold the line on the bounded plan; park richer data in "future work." |

---

## 11. Honest Limitations of This Analysis

- **No data was downloaded or inspected** (per task constraints); scores reflect documented public
  characteristics and the spec criteria, not hands-on profiling.
- **Licensing notes are good-faith readings, not legal advice**, and must be re-verified at acquisition
  (`DATA_SPEC.md` §8/§16).
- **Fit scores are a structured judgment**, not a precise measurement; the weighting encodes the
  inherited priorities but other defensible weightings exist.
- **Kaggle is a category, not a single dataset**; its score reflects the representative European Soccer
  Database and the category's general licensing/account caveats.

---

## 12. Next Natural Step

Review this analysis and **select the dataset** — recording the choice, source, league, season range,
license, and acquisition method in [`DATA_SPEC.md`](../specs/DATA_SPEC.md), per its deferred-decision
table. This document is **non-binding input** to that decision; it makes no change to any spec and
commits to no implementation.

---

> **Conformance:** This research artifact respects the scope boundaries, non-goals, priorities, budget
> philosophy, and deferred-decision model of [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) and
> the rules of [`DATA_SPEC.md`](../specs/DATA_SPEC.md). It introduces no new project requirements,
> modifies no specification, and does not finalize the dataset decision.
