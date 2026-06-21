"""Final baseline-vs-selected-model evaluation comparison for StatSport."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


CORE_METRICS: tuple[str, ...] = (
    "accuracy",
    "balanced_accuracy",
    "log_loss",
    "macro_f1",
)
HIGHER_IS_BETTER_METRICS = {"accuracy", "balanced_accuracy", "macro_f1"}
LOWER_IS_BETTER_METRICS = {"log_loss"}
BASELINE_MODEL_NAME = "baseline"
SELECTED_MODEL_NAME = "logistic_regression"


@dataclass(frozen=True)
class ReportMetricRow:
    """One metrics row loaded from a model report CSV."""

    split: str
    train_seasons: str
    evaluation_season: str
    row_count: int
    metrics: dict[str, float]


@dataclass(frozen=True)
class MetricComparison:
    """Baseline-vs-selected-model comparison for one split or fold."""

    split: str
    train_seasons: str
    evaluation_season: str
    row_count: int
    baseline_metrics: dict[str, float]
    selected_metrics: dict[str, float]
    deltas: dict[str, float]
    improved: dict[str, bool]


@dataclass(frozen=True)
class ConfusionMatrixSummary:
    """Small draw-class summary from a confusion matrix report."""

    actual_draws: int
    correct_draw_predictions: int
    predicted_draw_total: int


def load_metric_rows(path: Path) -> list[ReportMetricRow]:
    """Load model metrics rows from a report CSV."""

    if not path.exists():
        raise FileNotFoundError(f"Missing required report file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Report file is empty: {path}")
    return [_parse_metric_row(row, path) for row in rows]


def compare_metric_rows(
    baseline: ReportMetricRow,
    selected: ReportMetricRow,
) -> MetricComparison:
    """Compare one baseline row with one selected-model row."""

    _validate_same_evaluation_row(baseline, selected)
    deltas = {
        metric: selected.metrics[metric] - baseline.metrics[metric]
        for metric in CORE_METRICS
    }
    improved = {
        metric: _metric_improved(metric, baseline.metrics[metric], selected.metrics[metric])
        for metric in CORE_METRICS
    }
    return MetricComparison(
        split=baseline.split,
        train_seasons=baseline.train_seasons,
        evaluation_season=baseline.evaluation_season,
        row_count=baseline.row_count,
        baseline_metrics=baseline.metrics,
        selected_metrics=selected.metrics,
        deltas=deltas,
        improved=improved,
    )


def compare_metric_reports(
    baseline_rows: list[ReportMetricRow],
    selected_rows: list[ReportMetricRow],
) -> list[MetricComparison]:
    """Compare full baseline and selected-model metric reports."""

    if len(baseline_rows) != len(selected_rows):
        raise ValueError("Baseline and selected-model reports have different row counts")
    return [
        compare_metric_rows(baseline, selected)
        for baseline, selected in zip(baseline_rows, selected_rows)
    ]


def load_confusion_matrix(path: Path) -> dict[str, dict[str, int]]:
    """Load an actual-by-predicted confusion matrix report."""

    if not path.exists():
        raise FileNotFoundError(f"Missing required confusion matrix file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Confusion matrix file is empty: {path}")

    matrix: dict[str, dict[str, int]] = {}
    for row in rows:
        actual = row["actual"]
        matrix[actual] = {
            "H": int(row["predicted_H"]),
            "D": int(row["predicted_D"]),
            "A": int(row["predicted_A"]),
        }
    return matrix


def draw_class_summary(matrix: dict[str, dict[str, int]]) -> ConfusionMatrixSummary:
    """Summarize draw-class recall and draw prediction volume."""

    draw_row = matrix["D"]
    return ConfusionMatrixSummary(
        actual_draws=sum(draw_row.values()),
        correct_draw_predictions=draw_row["D"],
        predicted_draw_total=sum(row["D"] for row in matrix.values()),
    )


def comparison_to_csv_rows(
    comparisons: list[MetricComparison],
    scope: str,
) -> list[dict[str, str]]:
    """Convert comparisons to deterministic report rows."""

    rows: list[dict[str, str]] = []
    for comparison in comparisons:
        row = {
            "scope": scope,
            "split": comparison.split,
            "train_seasons": comparison.train_seasons,
            "evaluation_season": comparison.evaluation_season,
            "row_count": str(comparison.row_count),
        }
        for metric in CORE_METRICS:
            row[f"baseline_{metric}"] = _format_float(comparison.baseline_metrics[metric])
            row[f"logistic_regression_{metric}"] = _format_float(
                comparison.selected_metrics[metric]
            )
            row[f"{metric}_delta"] = _format_float(comparison.deltas[metric])
            row[f"{metric}_improved"] = str(comparison.improved[metric])
        rows.append(row)
    return rows


def comparison_csv_fieldnames() -> list[str]:
    """Return comparison report CSV column order."""

    fieldnames = ["scope", "split", "train_seasons", "evaluation_season", "row_count"]
    for metric in CORE_METRICS:
        fieldnames.extend(
            [
                f"baseline_{metric}",
                f"logistic_regression_{metric}",
                f"{metric}_delta",
                f"{metric}_improved",
            ]
        )
    return fieldnames


def generate_summary_markdown(
    test_comparison: MetricComparison,
    walk_forward_comparisons: list[MetricComparison],
    baseline_draw_summary: ConfusionMatrixSummary,
    selected_draw_summary: ConfusionMatrixSummary,
) -> str:
    """Generate a concise portfolio-ready evaluation summary."""

    lines = [
        "# StatSport Model Comparison Summary",
        "",
        "## Scope",
        "",
        (
            "This summary compares the home-advantage baseline with multinomial "
            "Logistic Regression using the approved chronological 2024/25 test "
            "season and season-blocked walk-forward validation folds."
        ),
        "",
        (
            "Lower Log Loss is better. For Accuracy, Balanced Accuracy, and "
            "Macro-F1, higher values are better."
        ),
        "",
        "## Test Season Comparison",
        "",
        _markdown_table([test_comparison]),
        "",
        "## Walk-Forward Comparison",
        "",
        _markdown_table(walk_forward_comparisons),
        "",
        "## Interpretation",
        "",
        _interpretation_sentence(test_comparison),
        "",
        (
            "Draw-class performance remains a clear limitation. On the 2024/25 "
            "test season, the baseline correctly predicted 0 of "
            f"{baseline_draw_summary.actual_draws} actual draws and made "
            f"{baseline_draw_summary.predicted_draw_total} draw predictions. "
            "Logistic Regression correctly predicted "
            f"{selected_draw_summary.correct_draw_predictions} of "
            f"{selected_draw_summary.actual_draws} actual draws and made "
            f"{selected_draw_summary.predicted_draw_total} draw predictions."
        ),
        "",
        (
            "Optional Brier Score and calibration assessment were not "
            "implemented in this milestone; the approved core metrics were "
            "sufficient for the final baseline-versus-selected-model comparison."
        ),
        "",
    ]
    return "\n".join(lines)


def _parse_metric_row(row: dict[str, str], path: Path) -> ReportMetricRow:
    missing = [
        column
        for column in ("split", "train_seasons", "evaluation_season", "row_count", *CORE_METRICS)
        if column not in row
    ]
    if missing:
        raise ValueError(f"Missing columns in {path}: {', '.join(missing)}")
    return ReportMetricRow(
        split=row["split"],
        train_seasons=row["train_seasons"],
        evaluation_season=row["evaluation_season"],
        row_count=int(row["row_count"]),
        metrics={metric: float(row[metric]) for metric in CORE_METRICS},
    )


def _validate_same_evaluation_row(
    baseline: ReportMetricRow,
    selected: ReportMetricRow,
) -> None:
    checks = (
        ("split", baseline.split, selected.split),
        ("train_seasons", baseline.train_seasons, selected.train_seasons),
        ("evaluation_season", baseline.evaluation_season, selected.evaluation_season),
        ("row_count", baseline.row_count, selected.row_count),
    )
    mismatches = [
        f"{name}: baseline={baseline_value!r}, selected={selected_value!r}"
        for name, baseline_value, selected_value in checks
        if baseline_value != selected_value
    ]
    if mismatches:
        raise ValueError(
            "Reports do not describe identical evaluation rows: "
            + "; ".join(mismatches)
        )


def _metric_improved(metric: str, baseline: float, selected: float) -> bool:
    if metric in HIGHER_IS_BETTER_METRICS:
        return selected > baseline
    if metric in LOWER_IS_BETTER_METRICS:
        return selected < baseline
    raise ValueError(f"Unknown metric direction: {metric}")


def _markdown_table(comparisons: list[MetricComparison]) -> str:
    header = (
        "| Split | Rows | Accuracy Delta | Balanced Accuracy Delta | "
        "Log Loss Delta | Macro-F1 Delta |"
    )
    separator = "|---|---:|---:|---:|---:|---:|"
    rows = [
        "| {split} | {rows} | {accuracy} | {balanced_accuracy} | {log_loss} | {macro_f1} |".format(
            split=comparison.split,
            rows=comparison.row_count,
            accuracy=_format_signed(comparison.deltas["accuracy"]),
            balanced_accuracy=_format_signed(comparison.deltas["balanced_accuracy"]),
            log_loss=_format_signed(comparison.deltas["log_loss"]),
            macro_f1=_format_signed(comparison.deltas["macro_f1"]),
        )
        for comparison in comparisons
    ]
    return "\n".join([header, separator, *rows])


def _interpretation_sentence(comparison: MetricComparison) -> str:
    improved_metrics = [
        metric.replace("_", " ").title()
        for metric in CORE_METRICS
        if comparison.improved[metric]
    ]
    if len(improved_metrics) == len(CORE_METRICS):
        return (
            "Logistic Regression improved over the baseline on all approved core "
            "test metrics, while the confusion matrix still shows weak draw-class "
            "performance."
        )
    if improved_metrics:
        return (
            "Logistic Regression improved over the baseline on "
            + ", ".join(improved_metrics)
            + ", but not on every approved core test metric."
        )
    return (
        "Logistic Regression did not improve over the baseline on the approved "
        "core test metrics."
    )


def _format_float(value: float) -> str:
    return f"{value:.12f}"


def _format_signed(value: float) -> str:
    return f"{value:+.12f}"
