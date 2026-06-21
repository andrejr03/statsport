"""Home-advantage baseline modelling and evaluation for StatSport."""

from __future__ import annotations

import csv
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


CLASS_ORDER: tuple[str, ...] = ("H", "D", "A")
"""Stable 1X2 class order used for all probabilities and confusion matrices."""

BASELINE_PREDICTION = "H"
TRAIN_SEASONS: tuple[str, ...] = ("2020/21", "2021/22", "2022/23", "2023/24")
TEST_SEASON = "2024/25"
WALK_FORWARD_FOLDS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("2020/21",), "2021/22"),
    (("2020/21", "2021/22"), "2022/23"),
    (("2020/21", "2021/22", "2022/23"), "2023/24"),
)
TARGET_COLUMN = "target_1x2"


@dataclass(frozen=True)
class EvaluationResult:
    """Metric result for one evaluated split or validation fold."""

    split: str
    train_seasons: tuple[str, ...]
    evaluation_season: str
    row_count: int
    probabilities: dict[str, float]
    metrics: dict[str, float]
    confusion_matrix: dict[str, dict[str, int]]


def load_feature_rows(path: Path) -> list[dict[str, str]]:
    """Load the Milestone 3 feature CSV."""

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    validate_feature_rows(rows)
    return rows


def validate_feature_rows(rows: list[dict[str, str]]) -> None:
    """Validate the minimal columns needed for baseline evaluation."""

    if not rows:
        raise ValueError("Feature dataset is empty")
    columns = set(rows[0])
    missing = [column for column in ("season", TARGET_COLUMN) if column not in columns]
    if missing:
        raise ValueError(f"Missing baseline input columns: {', '.join(missing)}")
    invalid_targets = sorted({row[TARGET_COLUMN] for row in rows} - set(CLASS_ORDER))
    if invalid_targets:
        raise ValueError(f"Unexpected target labels: {', '.join(invalid_targets)}")


def split_train_test(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Return the approved train/test split."""

    return rows_for_seasons(rows, TRAIN_SEASONS), rows_for_seasons(rows, (TEST_SEASON,))


def build_walk_forward_splits(
    rows: list[dict[str, str]],
) -> list[tuple[tuple[str, ...], str, list[dict[str, str]], list[dict[str, str]]]]:
    """Return the approved expanding-window validation splits."""

    return [
        (
            train_seasons,
            validation_season,
            rows_for_seasons(rows, train_seasons),
            rows_for_seasons(rows, (validation_season,)),
        )
        for train_seasons, validation_season in WALK_FORWARD_FOLDS
    ]


def rows_for_seasons(rows: list[dict[str, str]], seasons: tuple[str, ...]) -> list[dict[str, str]]:
    """Filter rows by season while preserving input order."""

    season_set = set(seasons)
    return [row for row in rows if row["season"] in season_set]


def predict_home_win(rows: list[dict[str, str]]) -> list[str]:
    """Return the deterministic home-advantage class prediction for each row."""

    return [BASELINE_PREDICTION for _ in rows]


def derive_class_probabilities(training_rows: list[dict[str, str]]) -> dict[str, float]:
    """Derive H/D/A probabilities from training labels only, in CLASS_ORDER."""

    if not training_rows:
        raise ValueError("Cannot derive baseline probabilities from an empty training split")
    counts = Counter(row[TARGET_COLUMN] for row in training_rows)
    total = float(len(training_rows))
    probabilities = {label: counts[label] / total for label in CLASS_ORDER}
    assert_probabilities_valid(probabilities)
    return probabilities


def assert_probabilities_valid(probabilities: dict[str, float]) -> None:
    """Validate stable class keys, finite values, bounds, and sum."""

    if tuple(probabilities.keys()) != CLASS_ORDER:
        raise ValueError("Probability class order must be H, D, A")
    for label, value in probabilities.items():
        if not math.isfinite(value) or value < 0.0 or value > 1.0:
            raise ValueError(f"Invalid probability for {label}: {value}")
    if not math.isclose(sum(probabilities.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("Probabilities must sum to 1")


def calculate_metrics(
    y_true: list[str],
    y_pred: list[str],
    probabilities: dict[str, float],
) -> dict[str, float]:
    """Calculate the approved baseline metrics except the confusion matrix."""

    if not y_true:
        raise ValueError("Cannot calculate metrics for an empty evaluation split")
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    assert_probabilities_valid(probabilities)
    return {
        "accuracy": accuracy(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy(y_true, y_pred),
        "log_loss": log_loss(y_true, probabilities),
        "macro_f1": macro_f1(y_true, y_pred),
    }


def accuracy(y_true: list[str], y_pred: list[str]) -> float:
    """Return classification accuracy."""

    return sum(
        1 for actual, predicted in zip(y_true, y_pred) if actual == predicted
    ) / len(y_true)


def balanced_accuracy(y_true: list[str], y_pred: list[str]) -> float:
    """Return mean per-class recall across the stable H/D/A classes."""

    recalls: list[float] = []
    for label in CLASS_ORDER:
        actual_count = sum(1 for actual in y_true if actual == label)
        if actual_count == 0:
            recalls.append(0.0)
            continue
        correct = sum(
            1
            for actual, predicted in zip(y_true, y_pred)
            if actual == label and predicted == label
        )
        recalls.append(correct / actual_count)
    return sum(recalls) / len(recalls)


def log_loss(y_true: list[str], probabilities: dict[str, float]) -> float:
    """Return multiclass log loss for a constant probability distribution."""

    epsilon = 1e-15
    total = 0.0
    for actual in y_true:
        probability = min(max(probabilities[actual], epsilon), 1.0 - epsilon)
        total -= math.log(probability)
    return total / len(y_true)


def macro_f1(y_true: list[str], y_pred: list[str]) -> float:
    """Return unweighted mean F1 across the stable H/D/A classes."""

    scores: list[float] = []
    for label in CLASS_ORDER:
        true_positive = sum(
            1
            for actual, predicted in zip(y_true, y_pred)
            if actual == label and predicted == label
        )
        false_positive = sum(
            1
            for actual, predicted in zip(y_true, y_pred)
            if actual != label and predicted == label
        )
        false_negative = sum(
            1
            for actual, predicted in zip(y_true, y_pred)
            if actual == label and predicted != label
        )
        denominator = (2 * true_positive) + false_positive + false_negative
        scores.append(0.0 if denominator == 0 else (2 * true_positive) / denominator)
    return sum(scores) / len(scores)


def confusion_matrix(y_true: list[str], y_pred: list[str]) -> dict[str, dict[str, int]]:
    """Return actual-by-predicted confusion matrix in stable H/D/A order."""

    matrix = {actual: {predicted: 0 for predicted in CLASS_ORDER} for actual in CLASS_ORDER}
    for actual, predicted in zip(y_true, y_pred):
        matrix[actual][predicted] += 1
    return matrix


def evaluate_split(
    split: str,
    train_seasons: tuple[str, ...],
    evaluation_season: str,
    training_rows: list[dict[str, str]],
    evaluation_rows: list[dict[str, str]],
) -> EvaluationResult:
    """Evaluate the baseline on one split using probabilities from training rows only."""

    probabilities = derive_class_probabilities(training_rows)
    y_true = [row[TARGET_COLUMN] for row in evaluation_rows]
    y_pred = predict_home_win(evaluation_rows)
    return EvaluationResult(
        split=split,
        train_seasons=train_seasons,
        evaluation_season=evaluation_season,
        row_count=len(evaluation_rows),
        probabilities=probabilities,
        metrics=calculate_metrics(y_true, y_pred, probabilities),
        confusion_matrix=confusion_matrix(y_true, y_pred),
    )


def evaluate_baseline(
    rows: list[dict[str, str]],
) -> tuple[EvaluationResult, list[EvaluationResult]]:
    """Evaluate the approved test split and walk-forward validation folds."""

    training_rows, test_rows = split_train_test(rows)
    test_result = evaluate_split("test", TRAIN_SEASONS, TEST_SEASON, training_rows, test_rows)
    fold_results = [
        evaluate_split(
            f"walk_forward_{index}",
            train_seasons,
            validation_season,
            fold_training_rows,
            validation_rows,
        )
        for index, (train_seasons, validation_season, fold_training_rows, validation_rows)
        in enumerate(build_walk_forward_splits(rows), start=1)
    ]
    return test_result, fold_results
