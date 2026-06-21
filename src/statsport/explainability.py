"""Coefficient-based explainability artifacts for StatSport."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

from src.statsport.baseline import (
    CLASS_ORDER,
    TARGET_COLUMN,
    TEST_SEASON,
    TRAIN_SEASONS,
    rows_for_seasons,
)
from src.statsport.selected_model import FEATURE_COLUMNS


CLASS_NAMES = {"H": "Home", "D": "Draw", "A": "Away"}
INTERCEPT = "intercept"
DIFFERENCE_FEATURES: tuple[str, ...] = (
    "recent_form_points_diff",
    "goals_scored_diff",
    "goals_conceded_diff",
    "goal_difference_diff",
)
TOP_CONTRIBUTION_COUNT = 5

FEATURE_LABELS = {
    "home_advantage": "home advantage indicator",
    "home_recent_form_points_avg": "home recent points average",
    "away_recent_form_points_avg": "away recent points average",
    "recent_form_points_diff": "home-minus-away recent points difference",
    "home_goals_scored_avg": "home recent goals scored average",
    "away_goals_scored_avg": "away recent goals scored average",
    "goals_scored_diff": "home-minus-away goals scored difference",
    "home_goals_conceded_avg": "home recent goals conceded average",
    "away_goals_conceded_avg": "away recent goals conceded average",
    "goals_conceded_diff": "home-minus-away goals conceded difference",
    "home_goal_difference_avg": "home recent goal difference average",
    "away_goal_difference_avg": "away recent goal difference average",
    "goal_difference_diff": "home-minus-away goal difference difference",
}


@dataclass(frozen=True)
class FeatureStats:
    """Training-only standardization statistics for one feature."""

    mean: float
    scale: float


@dataclass(frozen=True)
class PredictionExplanation:
    """Local explanation for one selected test-season prediction."""

    category: str
    row: dict[str, str]
    predicted_class: str
    actual_class: str
    probabilities: dict[str, float]
    confidence: float
    margin: float
    logits: dict[str, float]
    contributions: dict[str, float]
    standardized_values: dict[str, float]
    top_contributions: list[dict[str, str]]
    difference_context: list[dict[str, str]]


def load_coefficients(path: Path) -> dict[str, dict[str, float]]:
    """Load standardized Logistic Regression coefficients in stable H/D/A order."""

    if not path.exists():
        raise FileNotFoundError(f"Missing coefficient report: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Coefficient report is empty: {path}")

    coefficients: dict[str, dict[str, float]] = {label: {} for label in CLASS_ORDER}
    for row in rows:
        class_label = row["class"]
        if class_label not in coefficients:
            raise ValueError(f"Unexpected coefficient class: {class_label}")
        coefficients[class_label][row["feature"]] = float(row["coefficient"])

    expected_features = (*FEATURE_COLUMNS, INTERCEPT)
    for class_label in CLASS_ORDER:
        missing = [feature for feature in expected_features if feature not in coefficients[class_label]]
        if missing:
            raise ValueError(
                f"Missing coefficient features for {class_label}: {', '.join(missing)}"
            )
    return coefficients


def rank_global_features(
    coefficients: dict[str, dict[str, float]],
) -> list[dict[str, str]]:
    """Return class-specific standardized coefficient rankings."""

    rows: list[dict[str, str]] = []
    for class_label in CLASS_ORDER:
        ranked = sorted(
            (
                (feature, coefficients[class_label][feature])
                for feature in FEATURE_COLUMNS
            ),
            key=lambda item: (-abs(item[1]), item[0]),
        )
        for index, (feature, coefficient) in enumerate(ranked, start=1):
            rows.append(
                {
                    "class": class_label,
                    "class_name": CLASS_NAMES[class_label],
                    "rank": str(index),
                    "feature": feature,
                    "feature_name": FEATURE_LABELS[feature],
                    "standardized_coefficient": _format_float(coefficient),
                    "absolute_coefficient": _format_float(abs(coefficient)),
                    "interpretation": interpret_coefficient(
                        feature,
                        class_label,
                        coefficient,
                    ),
                }
            )
    return rows


def training_feature_stats(
    rows: list[dict[str, str]],
    feature_columns: tuple[str, ...] = FEATURE_COLUMNS,
) -> dict[str, FeatureStats]:
    """Recreate the selected model's training-only StandardScaler statistics."""

    training_rows = rows_for_seasons(rows, TRAIN_SEASONS)
    if not training_rows:
        raise ValueError("Cannot compute explanation statistics without training rows")

    stats: dict[str, FeatureStats] = {}
    for feature in feature_columns:
        values = [float(row[feature]) for row in training_rows]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        scale = math.sqrt(variance)
        stats[feature] = FeatureStats(mean=mean, scale=scale if scale > 0.0 else 1.0)
    return stats


def explain_row(
    row: dict[str, str],
    coefficients: dict[str, dict[str, float]],
    stats: dict[str, FeatureStats],
    category: str = "example",
) -> PredictionExplanation:
    """Generate one coefficient-contribution local explanation."""

    standardized = {
        feature: (float(row[feature]) - stats[feature].mean) / stats[feature].scale
        for feature in FEATURE_COLUMNS
    }
    logits = {
        class_label: coefficients[class_label][INTERCEPT]
        + sum(
            coefficients[class_label][feature] * standardized[feature]
            for feature in FEATURE_COLUMNS
        )
        for class_label in CLASS_ORDER
    }
    probabilities = _softmax(logits)
    predicted_class = max(CLASS_ORDER, key=lambda label: probabilities[label])
    sorted_probabilities = sorted(
        probabilities.items(),
        key=lambda item: (-item[1], CLASS_ORDER.index(item[0])),
    )
    confidence = sorted_probabilities[0][1]
    margin = sorted_probabilities[0][1] - sorted_probabilities[1][1]
    contributions = {
        feature: coefficients[predicted_class][feature] * standardized[feature]
        for feature in FEATURE_COLUMNS
    }

    return PredictionExplanation(
        category=category,
        row=row,
        predicted_class=predicted_class,
        actual_class=row[TARGET_COLUMN],
        probabilities=probabilities,
        confidence=confidence,
        margin=margin,
        logits=logits,
        contributions=contributions,
        standardized_values=standardized,
        top_contributions=_top_contribution_rows_with_raw_values(
            _top_contribution_rows(contributions, standardized),
            row,
        ),
        difference_context=_difference_context_rows(row),
    )


def select_explanation_examples(
    rows: list[dict[str, str]],
    coefficients: dict[str, dict[str, float]],
    stats: dict[str, FeatureStats],
) -> list[PredictionExplanation]:
    """Select exactly three deterministic 2024/25 explanation examples."""

    test_rows = rows_for_seasons(rows, (TEST_SEASON,))
    if len(test_rows) < 3:
        raise ValueError("Need at least three test rows for explanation examples")

    explained = [
        explain_row(row, coefficients, stats)
        for row in test_rows
    ]

    selected: list[PredictionExplanation] = []
    used_keys: set[tuple[str, str, str, str]] = set()

    strong = _first_unused(
        sorted(
            [example for example in explained if example.predicted_class == example.actual_class],
            key=lambda example: (-example.confidence, _match_key(example.row)),
        ),
        used_keys,
    )
    selected.append(_with_category(strong, "strong_correct_prediction"))

    draw_pool = [
        example
        for example in explained
        if example.actual_class == "D" or example.predicted_class == "D"
    ]
    draw = _first_unused(
        sorted(
            draw_pool,
            key=lambda example: (
                example.actual_class != "D",
                -example.probabilities["D"],
                example.margin,
                _match_key(example.row),
            ),
        ),
        used_keys,
    )
    selected.append(_with_category(draw, "difficult_draw_or_draw_adjacent_prediction"))

    incorrect_pool = [
        example for example in explained if example.predicted_class != example.actual_class
    ]
    incorrect_or_low_confidence = _first_unused(
        sorted(
            incorrect_pool or explained,
            key=lambda example: (
                example.predicted_class == example.actual_class,
                example.confidence,
                example.margin,
                _match_key(example.row),
            ),
        ),
        used_keys,
    )
    selected.append(_with_category(incorrect_or_low_confidence, "incorrect_or_low_confidence_prediction"))

    return selected


def global_influence_markdown(rankings: list[dict[str, str]]) -> str:
    """Render global feature rankings as reader-facing markdown."""

    lines = [
        "# Global Feature Influence",
        "",
        (
            "The table ranks standardized Logistic Regression coefficients by "
            "absolute size within each class. Larger absolute values indicate "
            "stronger influence on that class logit, not a causal effect."
        ),
        "",
    ]
    for class_label in CLASS_ORDER:
        class_rows = [row for row in rankings if row["class"] == class_label]
        lines.extend(
            [
                f"## {CLASS_NAMES[class_label]} class",
                "",
                "| Rank | Feature | Standardized coefficient | Interpretation |",
                "|---:|---|---:|---|",
            ]
        )
        for row in class_rows:
            lines.append(
                "| {rank} | `{feature}` | {coefficient} | {interpretation} |".format(
                    rank=row["rank"],
                    feature=row["feature"],
                    coefficient=row["standardized_coefficient"],
                    interpretation=row["interpretation"],
                )
            )
        lines.append("")
    return "\n".join(lines)


def model_behaviour_summary_markdown(
    rankings: list[dict[str, str]],
    comparison_summary: str,
) -> str:
    """Render a concise model behaviour summary."""

    top_by_class = {
        class_label: [row for row in rankings if row["class"] == class_label][:3]
        for class_label in CLASS_ORDER
    }
    lines = [
        "# Model Behaviour Summary",
        "",
        (
            "The selected model is multinomial Logistic Regression. It uses "
            "standardized pre-match form, scoring, conceded-goal, and goal-difference "
            "features to assign probabilities to Home, Draw, and Away outcomes."
        ),
        "",
        "## Home predictions",
        "",
        _behaviour_sentence("H", top_by_class["H"]),
        "",
        "## Draw predictions",
        "",
        _behaviour_sentence("D", top_by_class["D"]),
        "",
        "## Away predictions",
        "",
        _behaviour_sentence("A", top_by_class["A"]),
        "",
        "## Evaluation context",
        "",
        _extract_evaluation_context(comparison_summary),
        "",
        "## Major limitations",
        "",
        (
            "The model improves over the home-advantage baseline in aggregate, "
            "but draw prediction remains weak. Coefficients describe associations "
            "in this Bundesliga sample and should not be read as causal claims."
        ),
        "",
    ]
    return "\n".join(lines)


def prediction_card_markdown(explanation: PredictionExplanation, card_number: int) -> str:
    """Render one local explanation card."""

    row = explanation.row
    lines = [
        f"# Prediction Explanation Card {card_number}",
        "",
        f"## Category",
        "",
        explanation.category.replace("_", " ").title(),
        "",
        "## Match context",
        "",
        (
            f"- Match: {row['home_team']} vs {row['away_team']}\n"
            f"- Season/date: {row['season']} on {row['match_date']}\n"
            f"- Final score: {row['full_time_home_goals']}-{row['full_time_away_goals']}\n"
            f"- Actual outcome: {CLASS_NAMES[explanation.actual_class]} ({explanation.actual_class})\n"
            f"- Predicted outcome: {CLASS_NAMES[explanation.predicted_class]} "
            f"({explanation.predicted_class})"
        ),
        "",
        "## Predicted probabilities",
        "",
        "| Class | Probability |",
        "|---|---:|",
    ]
    for class_label in CLASS_ORDER:
        lines.append(
            f"| {CLASS_NAMES[class_label]} ({class_label}) | "
            f"{_format_percent(explanation.probabilities[class_label])} |"
        )
    lines.extend(
        [
            "",
            "## Key contributing features",
            "",
            "| Feature | Raw value | Standardized value | Contribution to predicted class | Direction |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for contribution in explanation.top_contributions:
        lines.append(
            "| `{feature}` | {raw_value} | {standardized_value} | {contribution} | {direction} |".format(
                **contribution
            )
        )
    lines.extend(
        [
            "",
            "## Feature-difference context",
            "",
            "| Feature | Value | Plain-language reading |",
            "|---|---:|---|",
        ]
    )
    for context in explanation.difference_context:
        lines.append(
            "| `{feature}` | {value} | {interpretation} |".format(**context)
        )
    lines.extend(
        [
            "",
            "## Confidence discussion",
            "",
            _confidence_discussion(explanation),
            "",
        ]
    )
    return "\n".join(lines)


def limitations_markdown() -> str:
    """Render the approved limitations and uncertainty note."""

    return "\n".join(
        [
            "# Limitations and Uncertainty",
            "",
            "- Draw-class weakness: the selected model improves aggregate metrics but still struggles to identify draws in the held-out 2024/25 season.",
            "- Non-causality warning: coefficient signs and contributions describe model associations, not proof that a feature caused a result.",
            "- Bundesliga-only scope: these explanations are based only on Bundesliga seasons 2020/21 through 2024/25.",
            "- Small-data limitations: the test season contains 306 matches, so individual examples and class-specific behaviour should be interpreted cautiously.",
            "- Baseline comparison context: Logistic Regression beats the home-advantage baseline in the approved evaluation, but the improvement is modest and should not be overstated.",
            "",
        ]
    )


def interpret_coefficient(feature: str, class_label: str, coefficient: float) -> str:
    """Return a plain-language coefficient interpretation."""

    direction = "raises" if coefficient >= 0.0 else "lowers"
    return (
        f"Higher {FEATURE_LABELS[feature]} {direction} the model's "
        f"{CLASS_NAMES[class_label]} score, holding the other standardized "
        "features fixed."
    )


def global_csv_fieldnames() -> list[str]:
    """Return stable global influence CSV columns."""

    return [
        "class",
        "class_name",
        "rank",
        "feature",
        "feature_name",
        "standardized_coefficient",
        "absolute_coefficient",
        "interpretation",
    ]


def _softmax(logits: dict[str, float]) -> dict[str, float]:
    max_logit = max(logits.values())
    exp_values = {label: math.exp(logits[label] - max_logit) for label in CLASS_ORDER}
    total = sum(exp_values.values())
    probabilities = {label: exp_values[label] / total for label in CLASS_ORDER}
    if not math.isclose(sum(probabilities.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("Explanation probabilities must sum to 1")
    return probabilities


def _top_contribution_rows(
    contributions: dict[str, float],
    standardized: dict[str, float],
) -> list[dict[str, str]]:
    ranked = sorted(
        contributions.items(),
        key=lambda item: (-abs(item[1]), item[0]),
    )[:TOP_CONTRIBUTION_COUNT]
    rows: list[dict[str, str]] = []
    for feature, contribution in ranked:
        direction = "supports prediction" if contribution >= 0.0 else "pushes against prediction"
        rows.append(
            {
                "feature": feature,
                "raw_value": "",
                "standardized_value": _format_float(standardized[feature]),
                "contribution": _format_float(contribution),
                "direction": direction,
            }
        )
    return rows


def _difference_context_rows(row: dict[str, str]) -> list[dict[str, str]]:
    context: list[dict[str, str]] = []
    for feature in DIFFERENCE_FEATURES:
        value = float(row[feature])
        if feature == "goals_conceded_diff":
            positive = "home side has conceded more recently"
            negative = "away side has conceded more recently"
        else:
            positive = "home side has the recent edge"
            negative = "away side has the recent edge"
        if value > 0.0:
            interpretation = positive
        elif value < 0.0:
            interpretation = negative
        else:
            interpretation = "the recent values are level"
        context.append(
            {
                "feature": feature,
                "value": _format_float(value),
                "interpretation": interpretation,
            }
        )
    return context


def _first_unused(
    examples: list[PredictionExplanation],
    used_keys: set[tuple[str, str, str, str]],
) -> PredictionExplanation:
    for example in examples:
        key = _match_key(example.row)
        if key not in used_keys:
            used_keys.add(key)
            return example
    raise ValueError("Could not select a unique explanation example")


def _with_category(
    explanation: PredictionExplanation,
    category: str,
) -> PredictionExplanation:
    return PredictionExplanation(
        category=category,
        row=explanation.row,
        predicted_class=explanation.predicted_class,
        actual_class=explanation.actual_class,
        probabilities=explanation.probabilities,
        confidence=explanation.confidence,
        margin=explanation.margin,
        logits=explanation.logits,
        contributions=explanation.contributions,
        standardized_values=explanation.standardized_values,
        top_contributions=_top_contribution_rows_with_raw_values(
            explanation.top_contributions,
            explanation.row,
        ),
        difference_context=explanation.difference_context,
    )


def _top_contribution_rows_with_raw_values(
    rows: list[dict[str, str]],
    source_row: dict[str, str],
) -> list[dict[str, str]]:
    updated: list[dict[str, str]] = []
    for row in rows:
        copied = dict(row)
        copied["raw_value"] = _format_float(float(source_row[copied["feature"]]))
        updated.append(copied)
    return updated


def _match_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("match_date", ""),
        row.get("kickoff_time", ""),
        row.get("home_team", ""),
        row.get("away_team", ""),
    )


def _behaviour_sentence(class_label: str, rows: list[dict[str, str]]) -> str:
    feature_phrases = [
        f"`{row['feature']}` ({row['standardized_coefficient']})"
        for row in rows
    ]
    return (
        f"The largest {CLASS_NAMES[class_label]} coefficients are "
        + ", ".join(feature_phrases)
        + ". Positive coefficients raise that class score; negative coefficients lower it."
    )


def _extract_evaluation_context(comparison_summary: str) -> str:
    if "Draw-class performance remains a clear limitation" in comparison_summary:
        return (
            "Milestone 6 found that Logistic Regression improved over the baseline "
            "on the approved test metrics, while draw-class performance remained a "
            "clear limitation."
        )
    return (
        "Milestone 6 provides the baseline comparison context for interpreting "
        "these explanations."
    )


def _confidence_discussion(explanation: PredictionExplanation) -> str:
    correct = explanation.predicted_class == explanation.actual_class
    outcome = "correct" if correct else "incorrect"
    article = "a" if correct else "an"
    return (
        f"The model's top probability is {_format_percent(explanation.confidence)} "
        f"with a {_format_percent(explanation.margin)} gap over the next class. "
        f"This was {article} {outcome} prediction. The contribution table shows which "
        "standardized features most moved the predicted-class score up or down."
    )


def _format_float(value: float) -> str:
    return f"{value:.12f}"


def _format_percent(value: float) -> str:
    return f"{value:.2%}"
