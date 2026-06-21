"""Read-only Match Prediction Center showcase for StatSport."""

from __future__ import annotations

import csv
import base64
import html
import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

import streamlit as st


ROOT = Path(os.environ.get("STATSPORT_SHOWCASE_ROOT", Path(__file__).resolve().parent))

ASSET_IMAGE = Path("assets/STATSPORT_AI_POWERED_FOOTBALL_ANALYTICS_AND_PREDICTION_SHOWCASE.png")
EXPLANATION_CARD_PATHS = [
    Path("outputs/reports/prediction_explanation_card_1.md"),
    Path("outputs/reports/prediction_explanation_card_2.md"),
    Path("outputs/reports/prediction_explanation_card_3.md"),
]

REQUIRED_ARTIFACTS = [
    ASSET_IMAGE,
    Path("data/processed/bundesliga_2020_2025_matches_processed.csv"),
    Path("data/processed/bundesliga_2020_2025_features.csv"),
    Path("outputs/reports/model_comparison_test_metrics.csv"),
    Path("outputs/reports/model_comparison_walk_forward_metrics.csv"),
    Path("outputs/reports/logistic_regression_test_confusion_matrix.csv"),
    Path("outputs/reports/global_feature_influence.csv"),
    Path("outputs/reports/model_behaviour_summary.md"),
    Path("outputs/reports/limitations_and_uncertainty.md"),
    *EXPLANATION_CARD_PATHS,
]

METRIC_LABELS = [
    ("Accuracy", "baseline_accuracy", "logistic_regression_accuracy", "accuracy_delta", "Higher"),
    (
        "Balanced Accuracy",
        "baseline_balanced_accuracy",
        "logistic_regression_balanced_accuracy",
        "balanced_accuracy_delta",
        "Higher",
    ),
    ("Log Loss", "baseline_log_loss", "logistic_regression_log_loss", "log_loss_delta", "Lower"),
    ("Macro-F1", "baseline_macro_f1", "logistic_regression_macro_f1", "macro_f1_delta", "Higher"),
]

CLASS_META = {
    "H": ("Home", "Home win"),
    "D": ("Draw", "Draw"),
    "A": ("Away", "Away win"),
}

CLASS_COLORS = {
    "H": "#4fe3c1",
    "D": "#f2cc60",
    "A": "#79a8ff",
    "Home": "#4fe3c1",
    "Draw": "#f2cc60",
    "Away": "#79a8ff",
}

NARRATIVE_LABELS = {
    "Strong Correct Prediction": ("Strong Correct Prediction", "Confident hit"),
    "Difficult Draw Or Draw Adjacent Prediction": ("Draw Failure", "Known blind spot"),
    "Incorrect Or Low Confidence Prediction": ("Unexpected Miss", "Low-confidence miss"),
}

SHOWCASE_SCENARIO_DATES = {
    "Strong Correct Prediction": "2027-05-20",
    "Difficult Draw Or Draw Adjacent Prediction": "2027-05-21",
    "Incorrect Or Low Confidence Prediction": "2027-05-22",
}


@dataclass(frozen=True)
class Contribution:
    feature: str
    raw_value: float
    standardized_value: float
    contribution: float
    direction: str


@dataclass(frozen=True)
class FeatureContext:
    feature: str
    value: float
    reading: str


@dataclass(frozen=True)
class PredictionFixture:
    category: str
    match: str
    match_date: str
    score: str
    actual: str
    predicted: str
    probabilities: dict[str, float]
    contributions: list[Contribution]
    contexts: list[FeatureContext]
    confidence_text: str

    @property
    def home_team(self) -> str:
        return self.match.split(" vs ", 1)[0]

    @property
    def away_team(self) -> str:
        return self.match.split(" vs ", 1)[1]

    @property
    def confidence(self) -> float:
        return self.probabilities[self.predicted]

    @property
    def margin(self) -> float:
        values = sorted(self.probabilities.values(), reverse=True)
        return values[0] - values[1]

    @property
    def confidence_level(self) -> str:
        if self.confidence >= 0.65 and self.margin >= 0.20:
            return "High"
        if self.confidence >= 0.45 and self.margin >= 0.07:
            return "Medium"
        return "Low"

    @property
    def is_correct(self) -> bool:
        return self.actual == self.predicted

    @property
    def narrative_label(self) -> str:
        return NARRATIVE_LABELS.get(self.category, (self.category, "Held-out example"))[0]

    @property
    def narrative_subtitle(self) -> str:
        return NARRATIVE_LABELS.get(self.category, (self.category, "Held-out example"))[1]

    @property
    def scenario_date(self) -> str:
        return SHOWCASE_SCENARIO_DATES.get(self.category, "2027-05-20")


def artifact_path(relative_path: Path) -> Path:
    return ROOT / relative_path


def missing_artifacts() -> list[Path]:
    return [path for path in REQUIRED_ARTIFACTS if not artifact_path(path).exists()]


def read_csv_rows(relative_path: str | Path) -> list[dict[str, str]]:
    with artifact_path(Path(relative_path)).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_markdown(relative_path: str | Path) -> str:
    return artifact_path(Path(relative_path)).read_text(encoding="utf-8")


def read_image_data_uri(relative_path: Path) -> str:
    data = artifact_path(relative_path).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def read_csv_count(relative_path: str | Path) -> int:
    with artifact_path(Path(relative_path)).open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for _ in reader)


def fmt_number(value: str | float, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}"


def fmt_delta(value: str | float, digits: int = 3) -> str:
    return f"{float(value):+.{digits}f}"


def fmt_probability(value: float) -> str:
    return f"{value * 100:.2f}%"


def clean_label(value: str) -> str:
    return html.escape(value.replace("_", " ").replace("avg", "average").title())


def chip(label: str, class_name: str = "") -> str:
    return f"<span class='chip {class_name}'>{html.escape(label)}</span>"


def section_anchor(section_id: str, title: str, kicker: str | None = None) -> None:
    kicker_html = f"<p class='section-kicker'>{html.escape(kicker)}</p>" if kicker else ""
    st.markdown(
        f"""
        <section id="{section_id}" class="section-anchor">
            {kicker_html}
            <h2>{html.escape(title)}</h2>
        </section>
        """,
        unsafe_allow_html=True,
    )


def html_table(headers: Iterable[str], rows: Iterable[Iterable[str]], class_name: str = "") -> str:
    header_html = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    row_html = ""
    for row in rows:
        row_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    return f"<table class='data-table {class_name}'><thead><tr>{header_html}</tr></thead><tbody>{row_html}</tbody></table>"


def _extract_required(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Could not parse {label} from explanation card")
    return match.group(1).strip()


def _extract_table(text: str, heading: str) -> list[list[str]]:
    pattern = rf"## {re.escape(heading)}\n\n((?:\|.*\n)+)"
    table_match = re.search(pattern, text)
    if not table_match:
        raise ValueError(f"Could not parse table: {heading}")
    lines = [line.strip() for line in table_match.group(1).strip().splitlines()]
    body_lines = lines[2:]
    rows: list[list[str]] = []
    for line in body_lines:
        rows.append([cell.strip().strip("`") for cell in line.strip("|").split("|")])
    return rows


def parse_prediction_fixture(path: Path) -> PredictionFixture:
    text = read_markdown(path)
    category = _extract_required(r"## Category\n\n(.+)", text, "category")
    match = _extract_required(r"- Match: (.+)", text, "match")
    match_date = _extract_required(r"- Season/date: 2024/25 on (.+)", text, "date")
    score = _extract_required(r"- Final score: (.+)", text, "score")
    actual = _extract_required(r"- Actual outcome: .+\(([HDA])\)", text, "actual outcome")
    predicted = _extract_required(r"- Predicted outcome: .+\(([HDA])\)", text, "predicted outcome")
    confidence_text = _extract_required(r"## Confidence discussion\n\n(.+)", text, "confidence discussion")

    probability_rows = _extract_table(text, "Predicted probabilities")
    probabilities = {
        _extract_required(r"\(([HDA])\)", row[0], "probability class"): float(row[1].rstrip("%")) / 100
        for row in probability_rows
    }

    contribution_rows = _extract_table(text, "Key contributing features")
    contributions = [
        Contribution(
            feature=row[0],
            raw_value=float(row[1]),
            standardized_value=float(row[2]),
            contribution=float(row[3]),
            direction=row[4],
        )
        for row in contribution_rows
    ]

    context_rows = _extract_table(text, "Feature-difference context")
    contexts = [
        FeatureContext(feature=row[0], value=float(row[1]), reading=row[2])
        for row in context_rows
    ]

    return PredictionFixture(
        category=category,
        match=match,
        match_date=match_date,
        score=score,
        actual=actual,
        predicted=predicted,
        probabilities=probabilities,
        contributions=contributions,
        contexts=contexts,
        confidence_text=confidence_text,
    )


def load_prediction_fixtures() -> list[PredictionFixture]:
    return [parse_prediction_fixture(path) for path in EXPLANATION_CARD_PATHS]


def daily_featured_fixture_index(fixtures: list[PredictionFixture], today: date | None = None) -> int:
    if not fixtures:
        raise ValueError("At least one prediction fixture is required")
    current_date = today or date.today()
    return current_date.timetuple().tm_yday % len(fixtures)


def plain_language_reason(fixture: PredictionFixture) -> str:
    supportive = [row for row in fixture.contributions if row.direction == "supports prediction"]
    opposing = [row for row in fixture.contributions if row.direction != "supports prediction"]
    top_support = supportive[0] if supportive else fixture.contributions[0]
    context = fixture.contexts[0] if fixture.contexts else None
    class_name = CLASS_META[fixture.predicted][1].lower()
    reason = (
        f"The model called a {class_name} because {clean_label(top_support.feature).lower()} "
        f"most supported the predicted class."
    )
    if context:
        reason += f" The feature-difference context says {html.escape(context.reading)}."
    if opposing:
        reason += (
            f" The main counter-signal was {clean_label(opposing[0].feature).lower()}, "
            "which pushed against the prediction."
        )
    return reason


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #050911;
            --panel: #0d1722;
            --panel-2: #121f2d;
            --panel-3: #172838;
            --text: #f3f8fb;
            --muted: #a9b7c4;
            --line: rgba(255,255,255,.12);
            --accent: #4fe3c1;
            --accent-2: #79a8ff;
            --warning: #f2cc60;
            --danger: #ff7f72;
            --ok: #4fe3c1;
        }

        .stApp {
            background:
                radial-gradient(circle at 80% 0%, rgba(79,227,193,.16), transparent 30rem),
                radial-gradient(circle at 18% 18%, rgba(121,168,255,.18), transparent 34rem),
                linear-gradient(180deg, #06111c 0%, #050911 52%, #04070c 100%);
            color: var(--text);
        }

        [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="StyledFullScreenButton"], footer, #MainMenu {
            visibility: hidden;
            height: 0;
        }

        button[title="View fullscreen"], button[aria-label="Fullscreen"] {
            display: none !important;
        }

        .block-container {
            padding-top: 1.25rem;
            max-width: 1320px;
        }

        [data-testid="stSidebar"] {
            background: #06101a;
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] a {
            color: var(--muted);
            text-decoration: none;
        }

        h1, h2, h3, p, li, span, div {
            letter-spacing: 0;
        }

        .brand-band {
            position: relative;
            min-height: 330px;
            border: 1px solid rgba(255,255,255,.14);
            border-radius: 8px;
            overflow: hidden;
            background:
                radial-gradient(circle at 82% 42%, rgba(79,227,193,.18), transparent 14rem),
                linear-gradient(90deg, rgba(5,9,17,.97) 0%, rgba(5,9,17,.80) 43%, rgba(5,9,17,.16) 100%),
                var(--hero-image);
            background-size: cover;
            background-position: center right;
            padding: 2.35rem 2.45rem;
            box-shadow: 0 24px 70px rgba(0,0,0,.34);
        }

        .brand-band::before {
            content: "";
            position: absolute;
            right: 3rem;
            top: 2.2rem;
            width: 19rem;
            height: 19rem;
            border: 1px solid rgba(79,227,193,.28);
            border-radius: 50%;
            background:
                radial-gradient(circle at 50% 50%, rgba(79,227,193,.18) 0 .35rem, transparent .42rem),
                radial-gradient(circle at 28% 30%, rgba(121,168,255,.46) 0 .28rem, transparent .34rem),
                radial-gradient(circle at 68% 25%, rgba(79,227,193,.42) 0 .24rem, transparent .31rem),
                radial-gradient(circle at 74% 68%, rgba(121,168,255,.40) 0 .28rem, transparent .34rem),
                linear-gradient(35deg, transparent 48%, rgba(79,227,193,.24) 49%, rgba(79,227,193,.24) 51%, transparent 52%),
                linear-gradient(128deg, transparent 48%, rgba(121,168,255,.20) 49%, rgba(121,168,255,.20) 51%, transparent 52%);
            opacity: .78;
        }

        .brand-band::after {
            content: "";
            position: absolute;
            right: 7.1rem;
            bottom: 2.4rem;
            width: 10.5rem;
            height: 6.3rem;
            border: 1px solid rgba(255,255,255,.18);
            border-radius: 50%;
            box-shadow: inset 0 0 0 1px rgba(79,227,193,.12);
            opacity: .7;
        }

        .brand-content {
            position: relative;
            z-index: 1;
        }

        .wordmark {
            font-size: clamp(4.8rem, 10.6vw, 9.4rem);
            line-height: .9;
            font-weight: 950;
            margin: .05rem 0 .7rem;
        }

        .wordmark span {
            color: var(--accent-2);
        }

        .brand-subtitle {
            max-width: 35rem;
            font-size: 1.16rem;
            color: #d9e7ef;
            margin: 0 0 1.25rem;
        }

        .chip {
            display: inline-block;
            border: 1px solid rgba(79,227,193,.38);
            color: #e8fffb;
            background: rgba(79,227,193,.10);
            padding: .34rem .58rem;
            border-radius: 999px;
            margin: .16rem .18rem .16rem 0;
            font-size: .78rem;
            font-weight: 760;
        }

        .chip.warning {
            border-color: rgba(242,204,96,.44);
            background: rgba(242,204,96,.12);
            color: #fff3c6;
        }

        .section-anchor {
            padding-top: 1.15rem;
            margin-top: 1.8rem;
            border-top: 1px solid var(--line);
        }

        .section-anchor h2 {
            margin: 0 0 .75rem;
            font-size: 1.75rem;
        }

        .section-kicker {
            color: var(--accent);
            text-transform: uppercase;
            font-size: .74rem;
            font-weight: 800;
            margin-bottom: .3rem;
        }

        .prediction-shell {
            border: 1px solid rgba(79,227,193,.24);
            border-radius: 8px;
            padding: 1.15rem;
            background:
                linear-gradient(135deg, rgba(18,31,45,.96), rgba(8,14,23,.98)),
                radial-gradient(circle at top right, rgba(79,227,193,.16), transparent 22rem);
            box-shadow: 0 20px 70px rgba(0,0,0,.28);
        }

        .narrative-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .7rem;
            margin: .75rem 0 .9rem;
        }

        .narrative-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .85rem;
            background: rgba(255,255,255,.035);
        }

        .narrative-card.active {
            border-color: var(--prediction-color);
            background: linear-gradient(180deg, rgba(79,227,193,.12), rgba(255,255,255,.035));
        }

        .narrative-card small {
            color: var(--muted);
            display: block;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: .2rem;
        }

        .narrative-card strong {
            display: block;
            font-size: 1.02rem;
        }

        div[data-testid="stRadio"] label p {
            font-weight: 800;
            color: #dce8f0 !important;
        }

        div[data-testid="stButton"] button {
            border: 1px solid rgba(79,227,193,.56);
            background: linear-gradient(90deg, rgba(79,227,193,.22), rgba(121,168,255,.18));
            color: var(--text);
            font-weight: 850;
            border-radius: 8px;
        }

        div[data-testid="stButton"] button:hover {
            border-color: rgba(79,227,193,.92);
            color: var(--text);
        }

        .fixture-card, .panel-card, .metric-card {
            background: linear-gradient(180deg, rgba(18,31,45,.94), rgba(13,23,34,.96));
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            margin: .55rem 0;
        }

        .fixture-card h3, .panel-card h3, .metric-card h3 {
            margin: 0 0 .5rem;
            font-size: 1.02rem;
        }

        .fixture-teams {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: .8rem;
            margin: .6rem 0 .35rem;
        }

        .team-name {
            font-size: clamp(1.55rem, 3vw, 2.35rem);
            font-weight: 900;
            line-height: 1.02;
        }

        .team-name.away {
            text-align: right;
        }

        .versus {
            color: var(--muted);
            font-weight: 900;
            border: 1px solid var(--line);
            padding: .35rem .5rem;
            border-radius: 7px;
        }

        .fixture-meta {
            color: var(--muted);
            font-size: .9rem;
        }

        .prob-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .62rem;
            margin: .8rem 0;
        }

        .prob-card {
            border: 1px solid var(--line);
            background: rgba(255,255,255,.045);
            border-radius: 8px;
            padding: .9rem;
            min-height: 8.8rem;
            min-width: 0;
            overflow: hidden;
        }

        .prob-card.predicted {
            border-color: var(--prediction-color);
            box-shadow: inset 0 0 0 1px var(--prediction-color), 0 0 34px rgba(79,227,193,.12);
            background: linear-gradient(180deg, rgba(79,227,193,.13), rgba(255,255,255,.045));
        }

        .prob-label {
            color: var(--muted);
            font-size: .78rem;
            text-transform: uppercase;
            font-weight: 850;
        }

        .prob-value {
            font-size: clamp(2rem, 3.1vw, 3.65rem);
            font-weight: 950;
            line-height: 1;
            margin-top: .35rem;
        }

        .prediction-call {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .7rem;
        }

        .call-tile {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .8rem;
            background: rgba(255,255,255,.04);
        }

        .call-tile small {
            color: var(--muted);
            display: block;
            font-weight: 800;
            text-transform: uppercase;
            font-size: .72rem;
            margin-bottom: .25rem;
        }

        .call-tile strong {
            font-size: 1.35rem;
        }

        .reality.correct {
            border-color: rgba(79,227,193,.46);
            background: rgba(79,227,193,.11);
        }

        .reality.incorrect {
            border-color: rgba(255,127,114,.48);
            background: rgba(255,127,114,.10);
        }

        .reveal-card {
            margin-top: .7rem;
            border: 1px dashed rgba(242,204,96,.50);
            border-radius: 8px;
            padding: .95rem;
            background: rgba(242,204,96,.07);
        }

        .reveal-card small {
            color: var(--warning);
            display: block;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: .25rem;
        }

        .reveal-card strong {
            font-size: 1.25rem;
        }

        .reason-box {
            border-left: 3px solid var(--prediction-color);
            background: rgba(255,255,255,.05);
            padding: .8rem .95rem;
            border-radius: 7px;
            color: #e3eef4;
            margin: .7rem 0;
        }

        .driver-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .55rem;
            margin: .75rem 0 .85rem;
        }

        .driver-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .72rem;
            background: rgba(255,255,255,.04);
        }

        .driver-card small {
            color: var(--muted);
            display: block;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: .24rem;
        }

        .driver-card strong {
            display: block;
            font-size: .96rem;
        }

        .driver-card code {
            display: inline-block;
            margin-top: .36rem;
        }

        .feature-row {
            display: grid;
            grid-template-columns: minmax(13rem, 19rem) 1fr 5.6rem;
            gap: .75rem;
            align-items: center;
            margin: .64rem 0;
            color: var(--muted);
        }

        .feature-row strong {
            color: var(--text);
            display: block;
        }

        .feature-row small {
            color: var(--muted);
        }

        .bar-track {
            height: .72rem;
            background: rgba(255,255,255,.08);
            border-radius: 999px;
            overflow: hidden;
        }

        .bar-fill.positive {
            height: 100%;
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            border-radius: 999px;
        }

        .bar-fill.negative {
            height: 100%;
            background: linear-gradient(90deg, var(--danger), var(--warning));
            border-radius: 999px;
        }

        .context-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: .55rem;
            margin-top: .8rem;
        }

        .context-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .7rem;
            background: rgba(255,255,255,.035);
        }

        .context-card strong {
            display: block;
        }

        .context-card span {
            color: var(--muted);
            font-size: .88rem;
        }

        .metric-label {
            color: var(--muted);
            font-size: .76rem;
            text-transform: uppercase;
            font-weight: 800;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 920;
            margin: .12rem 0 .55rem;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: .32rem .72rem;
            color: var(--muted);
            font-size: .9rem;
        }

        .metric-grid strong {
            color: var(--text);
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            overflow: hidden;
            border-radius: 8px;
            border: 1px solid var(--line);
            margin: .8rem 0 1rem;
        }

        .data-table th, .data-table td {
            padding: .7rem .78rem;
            border-bottom: 1px solid var(--line);
            text-align: left;
            vertical-align: middle;
        }

        .data-table th {
            color: var(--muted);
            background: rgba(255,255,255,.045);
            font-size: .78rem;
        }

        .matrix-cell {
            display: block;
            text-align: center;
            border-radius: 6px;
            padding: .52rem .65rem;
            color: #f7fffd;
            font-weight: 850;
        }

        .draw-warning {
            border-color: rgba(242,204,96,.66);
            background: linear-gradient(180deg, rgba(52,42,17,.82), rgba(24,22,17,.94));
        }

        .draw-warning strong {
            color: var(--warning);
            font-size: 1.38rem;
        }

        .pipeline {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: .7rem;
        }

        .pipeline-step {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .85rem;
            background: rgba(255,255,255,.04);
        }

        .pipeline-step strong {
            display: block;
            margin-bottom: .35rem;
        }

        .pipeline-step span, .panel-card p, .metric-card p {
            color: var(--muted);
        }

        code {
            color: #dff8f3;
        }

        @media (max-width: 900px) {
            .prob-grid, .prediction-call, .context-grid, .pipeline, .narrative-grid, .driver-grid {
                grid-template-columns: 1fr;
            }
            .feature-row {
                grid-template-columns: 1fr;
            }
            .fixture-teams {
                grid-template-columns: 1fr;
            }
            .team-name.away {
                text-align: left;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_missing_artifacts(missing: list[Path]) -> None:
    st.set_page_config(page_title="StatSport Match Prediction Center", page_icon="SS", layout="wide")
    inject_css()
    st.title("StatSport Match Prediction Center")
    st.error(
        "Showcase artifacts not found.\n\n"
        "Run the reproduction workflow documented in docs/guides/STATSPORT_REPRODUCTION_GUIDE.md."
    )
    with st.expander("Missing files"):
        for path in missing:
            st.code(str(path))


def render_sidebar() -> None:
    st.sidebar.title("StatSport")
    st.sidebar.caption("Local portfolio showcase")
    links = [
        ("Prediction Center", "prediction-center"),
        ("Track Record", "track-record"),
        ("Explainability", "explainability"),
        ("Draw Limitation", "draw-limitation"),
        ("Reproducibility", "reproducibility"),
    ]
    for label, target in links:
        st.sidebar.markdown(f"[{label}](#{target})")
    st.sidebar.markdown("---")
    st.sidebar.caption("Read-only portfolio replay based on held-out model artifacts. No live data, odds, accounts, APIs, or training flow.")


def render_hero() -> None:
    image_url = read_image_data_uri(ASSET_IMAGE)
    st.markdown(
        f"""
        <div id="hero" class="brand-band" style="--hero-image: url('{image_url}')">
            <div class="brand-content">
                <div class="wordmark">STAT<span>SPORT</span></div>
                <p class="brand-subtitle">Match Prediction Center for 2027 showcase replay scenarios.</p>
                <div>
                    {chip("AI + football")}
                    {chip("2027 showcase replay")}
                    {chip("Local replay, not live odds", "warning")}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_probability_cards(fixture: PredictionFixture) -> None:
    cards = ""
    for class_label in ("H", "D", "A"):
        class_name, display_name = CLASS_META[class_label]
        predicted = " predicted" if class_label == fixture.predicted else ""
        color = CLASS_COLORS[class_label]
        cards += (
            f"<div class='prob-card{predicted}' style='--prediction-color:{color}'>"
            f"<div class='prob-label'>{html.escape(display_name)}</div>"
            f"<div class='prob-value' style='color:{color}'>{fmt_probability(fixture.probabilities[class_label])}</div>"
            f"<span class='chip'>{html.escape(class_name)}</span>"
            "</div>"
        )
    st.markdown(f"<div class='prob-grid'>{cards}</div>", unsafe_allow_html=True)


def render_prediction_summary(fixture: PredictionFixture) -> None:
    predicted_name = CLASS_META[fixture.predicted][1]
    st.markdown(
        f"""
        <div class="prediction-call">
            <div class="call-tile">
                <small>Predicted outcome</small>
                <strong>{html.escape(predicted_name)}</strong>
            </div>
            <div class="call-tile">
                <small>Confidence level</small>
                <strong>{html.escape(fixture.confidence_level)} · {fmt_probability(fixture.confidence)}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_reveal_panel(fixture: PredictionFixture) -> None:
    reveal_key = f"show_actual_{fixture.match_date}_{fixture.home_team}_{fixture.away_team}"
    actual_name = CLASS_META[fixture.actual][1]
    correctness = "Correct" if fixture.is_correct else "Incorrect"
    reality_class = "correct" if fixture.is_correct else "incorrect"

    if st.button("Reveal actual result", key=f"button_{reveal_key}", use_container_width=True):
        st.session_state[reveal_key] = True

    if st.session_state.get(reveal_key, False):
        st.markdown(
            f"""
            <div class="call-tile reality {reality_class}">
                <small>Actual Result</small>
                <strong>{html.escape(correctness)} · {html.escape(actual_name)} ({html.escape(fixture.score)})</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="reveal-card">
                <small>Result hidden</small>
                <strong>Let the model commit first, then reveal what happened.</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_local_explanation(fixture: PredictionFixture) -> None:
    max_abs = max(abs(row.contribution) for row in fixture.contributions) or 1.0
    top_drivers = sorted(fixture.contributions, key=lambda row: abs(row.contribution), reverse=True)[:3]
    driver_cards = ""
    for index, row in enumerate(top_drivers, start=1):
        driver_cards += (
            "<div class='driver-card'>"
            f"<small>Driver {index}</small>"
            f"<strong>{clean_label(row.feature)}</strong>"
            f"<code>{row.contribution:+.3f}</code>"
            "</div>"
        )
    rows = ""
    for row in fixture.contributions:
        width = abs(row.contribution) / max_abs * 100
        direction = "positive" if row.contribution >= 0 else "negative"
        rows += (
            "<div class='feature-row'>"
            "<div>"
            f"<strong>{clean_label(row.feature)}</strong>"
            f"<small>{html.escape(row.direction)} · raw {row.raw_value:.2f} · standardized {row.standardized_value:+.2f}</small>"
            "</div>"
            "<div class='bar-track'>"
            f"<div class='bar-fill {direction}' style='width:{width:.1f}%'></div>"
            "</div>"
            f"<code>{row.contribution:+.3f}</code>"
            "</div>"
        )
    contexts = ""
    for context in fixture.contexts:
        contexts += (
            "<div class='context-card'>"
            f"<strong>{clean_label(context.feature)} · {context.value:+.2f}</strong>"
            f"<span>{html.escape(context.reading)}</span>"
            "</div>"
        )
    st.markdown(
        f"""
        <div class="panel-card">
            <h3>Why This Prediction?</h3>
            <div class="reason-box">{plain_language_reason(fixture)}</div>
            <div class="driver-grid">{driver_cards}</div>
            {rows}
            <div class="context-grid">{contexts}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_center(fixtures: list[PredictionFixture]) -> None:
    section_anchor("prediction-center", "Match Prediction Center", "Primary feature")
    labels = [fixture.narrative_label for fixture in fixtures]
    featured_index = daily_featured_fixture_index(fixtures)
    selected_label = st.radio(
        "Featured held-out prediction",
        labels,
        index=featured_index,
        horizontal=True,
        label_visibility="visible",
        help="Rotates daily across showcase replay scenarios based on held-out Bundesliga test predictions.",
    )
    st.caption("Rotates daily across 2027 showcase replay scenarios based on held-out Bundesliga test predictions. Select another curated case to inspect.")
    fixture = fixtures[labels.index(selected_label)]
    prediction_color = CLASS_COLORS[fixture.predicted]
    narrative_cards = ""
    for item in fixtures:
        active = " active" if item == fixture else ""
        narrative_cards += (
            f"<div class='narrative-card{active}' style='--prediction-color:{prediction_color}'>"
            f"<small>{html.escape(item.narrative_subtitle)}</small>"
            f"<strong>{html.escape(item.narrative_label)}</strong>"
            f"<span>{html.escape(item.match)}</span>"
            "</div>"
        )

    st.markdown(f"<div class='narrative-grid'>{narrative_cards}</div>", unsafe_allow_html=True)
    left, right = st.columns([1.2, 0.8], gap="large")
    with left:
        st.markdown(
            f"""
            <div class="fixture-card">
                <div class="fixture-meta">Scenario date: {html.escape(fixture.scenario_date)} · 2027 showcase replay · Based on a held-out Bundesliga test prediction</div>
                <div class="fixture-teams">
                    <div class="team-name">{html.escape(fixture.home_team)}</div>
                    <div class="versus">VS</div>
                    <div class="team-name away">{html.escape(fixture.away_team)}</div>
                </div>
                <div>{chip(fixture.narrative_label)} {chip(fixture.narrative_subtitle, "warning")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_probability_cards(fixture)
        render_prediction_summary(fixture)
        render_reveal_panel(fixture)
    with right:
        render_local_explanation(fixture)


def render_metric_cards(test_row: dict[str, str]) -> None:
    cols = st.columns(4)
    interpretations = {
        "Accuracy": "Share of held-out test matches classified correctly.",
        "Balanced Accuracy": "Class-aware accuracy so draws stay visible.",
        "Log Loss": "Probability quality; lower is better.",
        "Macro-F1": "Average class-level precision/recall balance.",
    }

    for col, (label, baseline_key, model_key, delta_key, direction) in zip(cols, METRIC_LABELS):
        delta = float(test_row[delta_key])
        improved = delta < 0 if direction == "Lower" else delta > 0
        accent = "var(--accent)" if improved else "var(--danger)"
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{html.escape(label)}</div>
                    <div class="metric-value" style="color:{accent}">{fmt_number(test_row[model_key])}</div>
                    <div class="metric-grid">
                        <span>Baseline</span><strong>{fmt_number(test_row[baseline_key])}</strong>
                        <span>Logistic Regression</span><strong>{fmt_number(test_row[model_key])}</strong>
                        <span>Delta</span><strong>{fmt_delta(test_row[delta_key])}</strong>
                    </div>
                    <p>{html.escape(interpretations[label])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_walk_forward(rows: list[dict[str, str]]) -> None:
    table_rows = []
    max_abs = max(abs(float(row["macro_f1_delta"])) for row in rows) or 1.0
    bars = ""
    for row in rows:
        width = abs(float(row["macro_f1_delta"])) / max_abs * 100
        table_rows.append(
            [
                html.escape(row["split"].replace("_", " ").title()),
                html.escape(row["evaluation_season"]),
                fmt_delta(row["accuracy_delta"]),
                fmt_delta(row["balanced_accuracy_delta"]),
                fmt_delta(row["log_loss_delta"]),
                fmt_delta(row["macro_f1_delta"]),
            ]
        )
        bars += (
            "<div class='feature-row'>"
            f"<strong>{html.escape(row['split'].replace('_', ' ').title())}</strong>"
            "<div class='bar-track'>"
            f"<div class='bar-fill positive' style='width:{width:.1f}%'></div>"
            "</div>"
            f"<code>{fmt_delta(row['macro_f1_delta'])}</code>"
            "</div>"
        )
    st.markdown(
        html_table(
            ["Fold", "Validation season", "Accuracy delta", "Balanced Acc delta", "Log Loss delta", "Macro-F1 delta"],
            table_rows,
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='panel-card'><h3>Walk-forward Macro-F1 delta</h3>{bars}</div>",
        unsafe_allow_html=True,
    )


def render_track_record() -> None:
    section_anchor("track-record", "Track Record", "Evidence behind the Prediction Center")
    test_row = read_csv_rows("outputs/reports/model_comparison_test_metrics.csv")[0]
    render_metric_cards(test_row)
    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        st.markdown(
            """
            <div class="panel-card">
                <h3>Baseline vs selected model</h3>
                <p>Home-advantage baseline always predicts Home. Multinomial Logistic Regression is the selected
                interpretable model and improves the approved metrics on the same held-out 2024/25 test split.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="panel-card">
                <h3>Validation discipline</h3>
                <p>Walk-forward validation uses season-blocked expanding windows, so later seasons are never used
                to evaluate earlier predictions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    render_walk_forward(read_csv_rows("outputs/reports/model_comparison_walk_forward_metrics.csv"))


def render_feature_tab(rows: list[dict[str, str]], class_name: str) -> None:
    class_rows = [row for row in rows if row["class_name"] == class_name]
    max_abs = max(float(row["absolute_coefficient"]) for row in class_rows) or 1.0
    bars = ""
    for row in class_rows[:8]:
        coefficient = float(row["standardized_coefficient"])
        width = float(row["absolute_coefficient"]) / max_abs * 100
        direction = "positive" if coefficient >= 0 else "negative"
        bars += (
            "<div class='feature-row'>"
            "<div>"
            f"<strong>{html.escape(row['feature_name'])}</strong>"
            f"<small>{html.escape(row['feature'])}</small>"
            "</div>"
            "<div class='bar-track'>"
            f"<div class='bar-fill {direction}' style='width:{width:.1f}%'></div>"
            "</div>"
            f"<code>{coefficient:+.3f}</code>"
            "</div>"
        )
    st.markdown(
        f"""
        <div class="panel-card">
            <h3>{html.escape(class_name)} feature influence</h3>
            {bars}
            <p>Ranked by absolute standardized Logistic Regression coefficient. These are associations, not causal claims.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_explainability() -> None:
    section_anchor("explainability", "Explainability", "Global model behaviour")
    rows = read_csv_rows("outputs/reports/global_feature_influence.csv")
    home_tab, draw_tab, away_tab = st.tabs(["Home", "Draw", "Away"])
    with home_tab:
        render_feature_tab(rows, "Home")
    with draw_tab:
        render_feature_tab(rows, "Draw")
    with away_tab:
        render_feature_tab(rows, "Away")
    with st.expander("Model behaviour summary"):
        st.markdown(read_markdown("outputs/reports/model_behaviour_summary.md"))


def render_confusion_matrix(rows: list[dict[str, str]]) -> tuple[int, int]:
    headers = ["Actual", "Predicted H", "Predicted D", "Predicted A"]
    table_rows = []
    actual_draws = 0
    correct_draws = 0
    for row in rows:
        actual = row["actual"]
        values = [int(row["predicted_H"]), int(row["predicted_D"]), int(row["predicted_A"])]
        if actual == "D":
            actual_draws = sum(values)
            correct_draws = int(row["predicted_D"])
        cells = [f"<strong>{html.escape(actual)}</strong>"]
        max_value = max(values) or 1
        for value in values:
            intensity = 0.18 + (value / max_value) * 0.56
            cells.append(
                f"<span class='matrix-cell' style='background: rgba(79, 227, 193, {intensity:.2f})'>{value}</span>"
            )
        table_rows.append(cells)
    st.markdown(html_table(headers, table_rows, "matrix-table"), unsafe_allow_html=True)
    return correct_draws, actual_draws


def render_draw_limitation() -> None:
    section_anchor("draw-limitation", "Draw Limitation", "Trust feature")
    rows = read_csv_rows("outputs/reports/logistic_regression_test_confusion_matrix.csv")
    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        correct_draws, actual_draws = render_confusion_matrix(rows)
    with right:
        st.markdown(
            f"""
            <div class="panel-card draw-warning">
                <h3>Draws remain hard</h3>
                <p><strong>{correct_draws} correct draw predictions out of {actual_draws} actual draws</strong></p>
                <p>The selected model improves aggregate metrics over the baseline, but it still missed every
                actual draw in the held-out 2024/25 test season.</p>
                {chip("Reported, not hidden", "warning")}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(read_markdown("outputs/reports/limitations_and_uncertainty.md"))


def render_reproducibility() -> None:
    section_anchor("reproducibility", "Reproducibility", "Credibility footer")
    match_count = read_csv_count("data/processed/bundesliga_2020_2025_matches_processed.csv")
    feature_count = read_csv_count("data/processed/bundesliga_2020_2025_features.csv")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card'><div class='metric-label'>Matches</div><div class='metric-value'>{match_count}</div><p>Bundesliga 2020/21-2024/25.</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div class='metric-label'>Feature rows</div><div class='metric-value'>{feature_count}</div><p>Rolling pre-match features.</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='metric-card'><div class='metric-label'>Test season</div><div class='metric-value'>306</div><p>Held-out 2024/25 matches.</p></div>", unsafe_allow_html=True)
    c4.markdown("<div class='metric-card'><div class='metric-label'>Mode</div><div class='metric-value'>Local</div><p>No external APIs or live inference.</p></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="pipeline">
            <div class="pipeline-step"><strong>Process data</strong><span>Football-Data.co.uk Bundesliga CSVs.</span></div>
            <div class="pipeline-step"><strong>Build features</strong><span>Prior-match rolling form, goals, conceded goals, and differences.</span></div>
            <div class="pipeline-step"><strong>Evaluate models</strong><span>Baseline and Logistic Regression on chronological splits.</span></div>
            <div class="pipeline-step"><strong>Explain predictions</strong><span>Coefficient-based global and local artifacts.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.code(
        "\n".join(
            [
                "python3 scripts/process_bundesliga_raw_data.py",
                "python3 scripts/build_bundesliga_features.py",
                "python3 scripts/evaluate_baseline_model.py",
                "python3 scripts/evaluate_logistic_regression_model.py",
                "python3 scripts/build_model_comparison_reports.py",
                "python3 scripts/build_explainability_artifacts.py",
                "python3 -m unittest tests/test_data_processing.py tests/test_feature_engineering.py tests/test_baseline.py tests/test_selected_model.py tests/test_evaluation.py tests/test_explainability.py -v",
            ]
        ),
        language="bash",
    )
    st.caption("Portfolio showcase only. No betting, odds advice, accounts, uploads, live prediction service, SaaS flow, or training interface.")


def render_app() -> None:
    st.set_page_config(page_title="StatSport Match Prediction Center", page_icon="SS", layout="wide")
    inject_css()
    render_sidebar()
    fixtures = load_prediction_fixtures()
    render_hero()
    render_prediction_center(fixtures)
    render_track_record()
    render_explainability()
    render_draw_limitation()
    render_reproducibility()


def main() -> None:
    missing = missing_artifacts()
    if missing:
        render_missing_artifacts(missing)
        return
    render_app()


if __name__ == "__main__":
    main()
