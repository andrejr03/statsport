# StatSport — Developer Guide (Beginner-Friendly)

**A practical, step-by-step guide for working on StatSport**

> _Everything André needs to take ownership of the repository and work confidently on macOS or Windows 11._

| | |
|---|---|
| **Status** | Specification Phase |
| **Audience** | André — beginner-to-intermediate Git user, comfortable with VS Code |
| **Platforms** | macOS and Windows 11 |
| **Companion docs** | The authoritative specs in [`docs/specs/`](../specs) |

> **How to read this guide:** You don't need to memorize it. Skim it once, then come back to the
> section you need when you need it. Every section is written so you can follow it step by step.
> When this guide and a spec ever disagree, **the specs win** — they are the source of truth.

---

## 1. Purpose of the Guide

This guide helps you **own and run the StatSport project independently**. It explains how to set up
your computer, use Git and GitHub, work with Codex, handle data, run and reproduce results, and keep
the project on track to become a finished portfolio piece.

It is deliberately **beginner-friendly**. You are **not** expected to know advanced MLOps, DevOps,
Git internals, or ML infrastructure. If a section feels like too much, do the **Quick-Start
Checklist** (§18) first and return to the details later.

What this guide is **not**: it is not a replacement for the specifications. The specs in
[`docs/specs/`](../specs) define *what* the project must be; this guide explains *how* to work on it.

---

## 2. Understanding the StatSport Project

**StatSport** is a university-level AI portfolio project: it takes historical football data and
produces **explainable analytics and match predictions**. It exists to show that you can carry a
machine-learning project from raw data all the way to honest, well-explained results.

It is one of **three** portfolio repositories you are building this summer, with a total budget of
**40–60 hours** for StatSport. That budget is a feature, not a limitation — it keeps the project
finishable so the other two can happen.

**What StatSport is NOT** (keep this list in mind whenever you're tempted to add "just one more
thing"):

- **Not a SaaS product.**
- **Not a commercial football platform.**
- **Not a betting or odds product.**
- **Not a research programme.**
- **Not a large-scale MLOps project.**

If an idea pushes the project toward any of those, it belongs in "future work," not in StatSport.

For the full picture, read [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md) first — it's the
anchor document everything else follows.

---

## 3. Repository Structure Overview

You don't need to touch every folder. Here's what each one is for:

```
statsport/
├── assets/        # Images and static assets (e.g., the showcase image)
├── data/
│   ├── raw/       # Original downloaded data — NEVER committed
│   ├── processed/ # Cleaned data you generate — NOT committed (regenerable)
│   └── external/  # Third-party/reference data — NOT committed
├── docs/
│   ├── specs/     # The authoritative specifications (read these!)
│   ├── guides/    # This guide lives here
│   ├── research/  # Background notes
│   ├── evidence/  # Supporting evidence
│   ├── reviews/   # Reviews
│   └── plans/     # Planning documents
├── notebooks/     # Exploratory Jupyter notebooks
├── outputs/
│   ├── figures/   # Generated plots — NOT committed (regenerable)
│   ├── reports/   # Generated reports — NOT committed
│   └── exports/   # Exported artifacts — NOT committed
├── src/           # Source code (analysis, features, models)
├── tests/         # Automated tests
├── scripts/       # Utility scripts
├── README.md
├── LICENSE
└── .gitignore     # Tells Git what to ignore (data, outputs, etc.)
```

**Key idea:** the `data/` and `outputs/` folders keep their *structure* in Git (via small `.gitkeep`
files) but their *contents* are ignored. You commit the **process**, not the **data**. (See §10.)

---

## 4. macOS Setup Guidance

> _The project is expected to work on macOS and Windows 11 (see §5). Both setups are
> supported, and the goal is to keep everything working the same way on both._

1. **Install Homebrew** (the macOS package manager) — visit [brew.sh](https://brew.sh) and follow the
   one-line install command.
2. **Install Git:**
   ```bash
   brew install git
   ```
3. **Install the GitHub CLI:**
   ```bash
   brew install gh
   ```
4. **Install VS Code** — download from [code.visualstudio.com](https://code.visualstudio.com) or:
   ```bash
   brew install --cask visual-studio-code
   ```
5. **Install Python** — a recent Python 3 is recommended (the exact version and environment tool are
   intentionally not fixed yet by the specs — see [`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md)).
   A simple option:
   ```bash
   brew install python
   ```
6. **Verify** everything is installed:
   ```bash
   git --version
   gh --version
   python3 --version
   ```

---

## 5. Windows 11 Setup Guidance

> _This is André's primary environment. Everything below mirrors the macOS steps so the project stays
> cross-platform._

1. **Install Git for Windows** — download from [git-scm.com](https://git-scm.com/download/win). During
   setup, the defaults are fine. This also gives you **Git Bash**, a terminal where the `git` commands
   in this guide work just like on macOS.
2. **Install the GitHub CLI** — download from [cli.github.com](https://cli.github.com), or via winget
   in PowerShell:
   ```powershell
   winget install --id GitHub.cli
   ```
3. **Install VS Code** — from [code.visualstudio.com](https://code.visualstudio.com), or:
   ```powershell
   winget install --id Microsoft.VisualStudioCode
   ```
4. **Install Python** — from [python.org](https://www.python.org/downloads/windows/) or:
   ```powershell
   winget install --id Python.Python.3
   ```
   ✅ On the python.org installer, **check "Add Python to PATH"** on the first screen.
5. **Verify** in PowerShell (or Git Bash):
   ```powershell
   git --version
   gh --version
   python --version
   ```

> **Tip:** When you run terminal commands from this guide, use **Git Bash** or the **VS Code
> integrated terminal** on Windows — the commands then look the same as the macOS ones. On Windows the
> Python command is usually `python`; on macOS it's usually `python3`.

---

## 6. Recommended Tools

| Tool | What it's for | Both platforms? |
|------|---------------|-----------------|
| **Git** | Version control | ✅ |
| **GitHub CLI (`gh`)** | Logging in to GitHub, cloning, PRs | ✅ |
| **VS Code** | Editing code, notebooks, and docs | ✅ |
| **Python 3** | Running the analysis/modelling | ✅ |
| **Jupyter** (via VS Code) | Exploratory notebooks | ✅ |
| **Codex** | Your AI pair-programmer (see §8) | ✅ |

Recommended VS Code extensions: **Python**, **Jupyter**, and **GitLens** (optional, makes Git easier
to see). Keep the toolset small — the project values **simplicity over infrastructure**.

---

## 7. Git and GitHub Workflow

Git tracks the history of your project; GitHub stores it online. Here's the beginner path.

### Logging in (one time)

Use the GitHub CLI — it's the easiest way to authenticate:
```bash
gh auth login
```
Follow the prompts (choose **GitHub.com**, **HTTPS**, and **log in with a browser**). This works the
same on macOS and Windows 11.

### Repository ownership — in plain terms

- The **repository** is the project's home — its files plus full history.
- **You own StatSport.** That means you decide what goes in and you make the commits.
- Cloning makes a **local copy** on your computer. Pushing sends your changes **back to GitHub**.
- Owning it also means keeping it tidy and honest — future-you and reviewers will read it.

### The four commands you'll use most

```bash
# 1. Clone (download) the repo once:
gh repo clone <your-username>/statsport
# or:  git clone https://github.com/<your-username>/statsport.git

# 2. Pull (get the latest changes) before you start working:
git pull

# 3. Commit (save a snapshot of your changes):
git add <files you changed>
git commit -m "Short, clear message about what you did"

# 4. Push (upload your commits to GitHub):
git push
```

**Golden rules:**
- **Pull before you start.** Commit **small and often** with clear messages.
- **Never commit data or large outputs** — `.gitignore` already blocks them; don't force them in.
- If you're unsure what changed, run `git status` — it's safe and just shows you the state.

---

## 8. Working with Codex

Codex is your AI assistant for building StatSport. Think of it as a **careful junior pair-programmer**:
helpful and fast, but you are the owner who reviews and approves everything.

**How to work with Codex well:**

- **Give small, focused tasks.** "Add a function that loads the processed match data and returns a
  table" is good. "Build the whole project" is not.
- **One step at a time.** Finish and check a task before starting the next.
- **Always review before you commit.** Read what Codex produced, make sure you understand it, and only
  then commit. If you can't explain it, don't ship it — ask Codex to explain or simplify.
- **Ask for explanations.** Codex can teach you *why* it did something. Use that to learn.
- **Keep it honest and in scope.** If Codex suggests something that breaks the scope boundaries or
  non-goals (see §2), say no.

> A good loop: **describe a small task → review the result → test it → commit → repeat.**

---

## 9. Daily Development Workflow

A simple routine that keeps things safe and reproducible:

1. **Open the project** in VS Code.
2. **Pull** the latest: `git pull`.
3. **Pick one small task** (yours or one you give Codex).
4. **Do the work** — edit code/notebooks, or have Codex draft it.
5. **Run it** and check the result.
6. **Review** the changes (`git status`, read the diff).
7. **Commit** with a clear message.
8. **Push** when you've finished a meaningful chunk: `git push`.
9. **Stop at a clean point** — don't leave the repo half-broken.

Repeat. Small steps add up to a finished project.

---

## 10. Working with Datasets

Data handling follows [`DATA_SPEC.md`](../specs/DATA_SPEC.md). The rules are simple and important:

- **Raw data must NOT be committed.** It lives in `data/raw/` and stays out of Git (the `.gitignore`
  already handles this). The same goes for `data/processed/` and `data/external/`.
- **Commit the process, not the data.** What you *do* commit is the **documented steps** to obtain and
  process the data, so anyone can recreate it.
- **Reproducibility:** write down where the data came from (source, license, date) and how to get it
  again. Someone else should be able to re-download and re-process it without asking you.
- **Traceability:** any result, table, or figure should be traceable back to the data and steps that
  produced it. No mystery numbers.

> If you're ever unsure whether a file should be committed, ask: *"Is this raw/processed data or a
> large generated output?"* If yes, it stays out of Git.

---

## 11. Working with Notebooks and Scripts

The project lets you use **notebooks, scripts, or both** for exploration — there is no requirement to
use one or the other (see [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md)).

- **Notebooks** (`notebooks/`) are great for **exploring and explaining** — trying ideas, plotting,
  and telling a story step by step.
- **Scripts / source code** (`src/`, `scripts/`) are great for **reusable, repeatable** logic that you
  run the same way every time.
- A common pattern: explore in a notebook, then move the stable, important logic into `src/` so it's
  clean and reproducible.
- Keep notebooks **tidy and runnable top-to-bottom** — a notebook that only works if you run cells out
  of order is hard for a reviewer (and future-you) to trust.

Whatever you choose, keep it **cross-platform**: avoid hard-coded `C:\...` or `/Users/...` paths; use
relative paths within the repo so it runs on both macOS and Windows 11.

---

## 12. Reproducing Results

Reproducibility is a **first-class requirement** (see
[`REPRODUCIBILITY_SPEC.md`](../specs/REPRODUCIBILITY_SPEC.md)). The test is simple: *could someone
else recreate your results from the repository and its documentation alone?*

To make that true:

- **Document the steps** from raw data → processed data → model → evaluation → explanation.
- **Control randomness** where it matters (e.g., fixed random seeds) so results repeat.
- **No hidden manual steps.** If you did something by hand, write it down.
- **Stay laptop-friendly and cross-platform** — no cloud, GPU, or paid services required, and it
  should run on both macOS and Windows 11.
- **Re-run from scratch occasionally** to make sure it still works. If it doesn't, fix the gap now.

---

## 13. Reviewing Outputs and Figures

Generated artifacts live under `outputs/` (`figures/`, `reports/`, `exports/`) and are **not
committed** — they should be **regenerable** from your code.

When you produce figures or reports:

- **Make them regenerable.** A reader should be able to run your workflow and get the same outputs.
- **Make them traceable.** Each figure/report ties back to the data and steps behind it.
- **Make them clear.** Figures should help a non-expert understand the result, not just look busy.
- **Check them honestly.** Do the visuals actually support the claim you're making? If not, fix the
  claim, not the chart (see [`EVALUATION_SPEC.md`](../specs/EVALUATION_SPEC.md)).

---

## 14. Common Mistakes

Avoid these — they're the usual beginner traps:

- ❌ **Committing data or large outputs.** Let `.gitignore` do its job; never force-add them.
- ❌ **Giant commits.** Many small commits beat one huge one.
- ❌ **Unclear commit messages** like "stuff" or "fixes." Say what changed and why.
- ❌ **Running notebook cells out of order** so results can't be reproduced.
- ❌ **Hard-coded absolute paths** that break on the other operating system.
- ❌ **Committing code you don't understand** (from Codex or anywhere). Review first.
- ❌ **Chasing accuracy** instead of finishing. A clear, honest result beats a fragile better score.
- ❌ **Scope creep** — adding features that push past the 40–60 hour budget.

---

## 15. Safety Rules

A few simple rules keep the project (and you) safe:

- 🔒 **Never commit secrets** — API keys, passwords, tokens. If in doubt, don't commit it.
- 🔒 **Never commit raw/processed data or large outputs.** (Covered by `.gitignore`.)
- 🧭 **Pull before you work, push when you finish** a clean chunk.
- 👀 **Review before you commit.** Understand every change.
- 💾 **Stop at clean points.** Don't leave the repo broken between sessions.
- 🙋 **When unsure, ask Codex to explain** rather than guessing.
- 📜 **The specs win.** If something conflicts with `docs/specs/`, follow the specs.

---

## 16. Portfolio Mindset

StatSport is a **portfolio piece** — its job is to show clear, honest competence to a reviewer. Keep
these four reminders in front of you (from [`PORTFOLIO_HANDOFF_SPEC.md`](../specs/PORTFOLIO_HANDOFF_SPEC.md)):

- **Finished > ambitious** — a completed project beats a grand unfinished one.
- **Explainable > complex** — a reviewer should understand *why* a prediction was made.
- **Reproducible > clever** — results others can recreate beat impressive one-offs.
- **Honest > impressive** — state limitations openly; never inflate claims.

A reviewer or future collaborator should understand the project in minutes.
Write for that reader.

---

## 17. Project Completion Mindset

Know what "done" means so you can actually get there:

- The goal is a **strong, finished portfolio project within 40–60 hours**.
- The goal is **not** maximum predictive performance — a clear, honest, well-explained result is the
  win.
- StatSport is **one of three** completed portfolio repositories — finishing it on budget is what lets
  the other two happen.
- "Complete" means: coherent specs, a baseline + selected model compared honestly, explainable
  predictions, reproducible results, and a clear README — see the completion criteria in
  [`PORTFOLIO_HANDOFF_SPEC.md`](../specs/PORTFOLIO_HANDOFF_SPEC.md).

When you hit those criteria, **stop polishing and ship it.** Finishing is the skill being
demonstrated.

---

## 18. Quick-Start Checklist

Use this the first time, and as a refresher:

**Setup (once):**
- [ ] Install Git, GitHub CLI (`gh`), VS Code, and Python 3 (§4 macOS / §5 Windows 11).
- [ ] `gh auth login` to connect to GitHub.
- [ ] Clone the repo: `gh repo clone <your-username>/statsport`.
- [ ] Open the folder in VS Code; install the **Python** and **Jupyter** extensions.
- [ ] Read [`PROJECT_OVERVIEW.md`](../specs/PROJECT_OVERVIEW.md).

**Every working session:**
- [ ] `git pull` to get the latest.
- [ ] Pick **one small task**.
- [ ] Do the work (you or Codex), then **run and check** it.
- [ ] `git status` and review the changes.
- [ ] `git commit -m "clear message"`.
- [ ] `git push` when you finish a clean chunk.
- [ ] Stop at a clean point.

**Always remember:**
- [ ] No data or large outputs in Git.
- [ ] Keep it reproducible and cross-platform (macOS + Windows 11).
- [ ] Review before you commit.
- [ ] Finished > ambitious · Explainable > complex · Reproducible > clever · Honest > impressive.

---

> **Remember:** This guide tells you *how* to work. The authoritative *what* lives in
> [`docs/specs/`](../specs). When in doubt, read the spec — and keep the project simple, honest, and
> finished.
