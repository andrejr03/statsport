"""Selected multinomial Logistic Regression model for StatSport."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from src.statsport.baseline import (
    CLASS_ORDER,
    TEST_SEASON,
    TARGET_COLUMN,
    TRAIN_SEASONS,
    EvaluationResult,
    build_walk_forward_splits,
    calculate_metrics,
    confusion_matrix,
    split_train_test,
)


FEATURE_COLUMNS: tuple[str, ...] = (
    "home_advantage",
    "home_recent_form_points_avg",
    "away_recent_form_points_avg",
    "recent_form_points_diff",
    "home_goals_scored_avg",
    "away_goals_scored_avg",
    "goals_scored_diff",
    "home_goals_conceded_avg",
    "away_goals_conceded_avg",
    "goals_conceded_diff",
    "home_goal_difference_avg",
    "away_goal_difference_avg",
    "goal_difference_diff",
)

MODEL_RANDOM_STATE = 42
MODEL_MAX_ITER = 1000


@dataclass(frozen=True)
class SelectedModelFit:
    """Fitted selected-model artifacts for one train/evaluation split."""

    scaler: StandardScaler
    model: LogisticRegression
    training_row_count: int
    feature_columns: tuple[str, ...]


@dataclass(frozen=True)
class SelectedModelResult:
    """Evaluation result plus fitted selected-model artifacts."""

    evaluation: EvaluationResult
    fit: SelectedModelFit


def select_feature_columns(rows: list[dict[str, str]]) -> tuple[str, ...]:
    """Return approved core feature columns after validating they exist."""

    if not rows:
        raise ValueError("Cannot select features from an empty dataset")
    columns = set(rows[0])
    missing = [column for column in FEATURE_COLUMNS if column not in columns]
    if missing:
        raise ValueError(f"Missing selected-model feature columns: {', '.join(missing)}")
    return FEATURE_COLUMNS


def fit_selected_model(training_rows: list[dict[str, str]]) -> SelectedModelFit:
    """Fit training-only preprocessing and multinomial Logistic Regression."""

    feature_columns = select_feature_columns(training_rows)
    x_train = build_feature_matrix(training_rows, feature_columns)
    y_train = [row[TARGET_COLUMN] for row in training_rows]

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)

    model = LogisticRegression(
        solver="lbfgs",
        max_iter=MODEL_MAX_ITER,
        random_state=MODEL_RANDOM_STATE,
    )
    model.fit(x_train_scaled, y_train)
    _validate_model_class_set(model)

    return SelectedModelFit(
        scaler=scaler,
        model=model,
        training_row_count=len(training_rows),
        feature_columns=feature_columns,
    )


def evaluate_selected_split(
    split: str,
    train_seasons: tuple[str, ...],
    evaluation_season: str,
    training_rows: list[dict[str, str]],
    evaluation_rows: list[dict[str, str]],
) -> SelectedModelResult:
    """Fit and evaluate Logistic Regression for one approved split."""

    fit = fit_selected_model(training_rows)
    y_true = [row[TARGET_COLUMN] for row in evaluation_rows]
    y_pred = predict_classes(fit, evaluation_rows)
    probability_rows = predict_probabilities(fit, evaluation_rows)
    metrics = calculate_metrics_from_rows(y_true, y_pred, probability_rows)

    evaluation = EvaluationResult(
        split=split,
        train_seasons=train_seasons,
        evaluation_season=evaluation_season,
        row_count=len(evaluation_rows),
        probabilities=mean_probabilities(probability_rows),
        metrics=metrics,
        confusion_matrix=confusion_matrix(y_true, y_pred),
    )
    return SelectedModelResult(evaluation=evaluation, fit=fit)


def evaluate_selected_model(
    rows: list[dict[str, str]],
) -> tuple[SelectedModelResult, list[SelectedModelResult]]:
    """Evaluate Logistic Regression on the approved test split and validation folds."""

    training_rows, test_rows = split_train_test(rows)
    test_result = evaluate_selected_split(
        "test",
        TRAIN_SEASONS,
        TEST_SEASON,
        training_rows,
        test_rows,
    )
    fold_results = [
        evaluate_selected_split(
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


def build_feature_matrix(
    rows: list[dict[str, str]],
    feature_columns: tuple[str, ...] = FEATURE_COLUMNS,
) -> np.ndarray:
    """Return a numeric feature matrix for approved columns."""

    return np.array(
        [[float(row[column]) for column in feature_columns] for row in rows],
        dtype=float,
    )


def transform_features(fit: SelectedModelFit, rows: list[dict[str, str]]) -> np.ndarray:
    """Apply training-fitted preprocessing to evaluation rows."""

    return fit.scaler.transform(build_feature_matrix(rows, fit.feature_columns))


def predict_classes(fit: SelectedModelFit, rows: list[dict[str, str]]) -> list[str]:
    """Predict H/D/A classes for rows."""

    return [str(label) for label in fit.model.predict(transform_features(fit, rows))]


def predict_probabilities(
    fit: SelectedModelFit,
    rows: list[dict[str, str]],
) -> list[dict[str, float]]:
    """Predict H/D/A probability rows in stable StatSport class order."""

    raw_probabilities = fit.model.predict_proba(transform_features(fit, rows))
    class_indexes = {str(label): index for index, label in enumerate(fit.model.classes_)}
    probability_rows: list[dict[str, float]] = []
    for row in raw_probabilities:
        probabilities = {label: float(row[class_indexes[label]]) for label in CLASS_ORDER}
        _assert_probability_row_valid(probabilities)
        probability_rows.append(probabilities)
    return probability_rows


def calculate_metrics_from_rows(
    y_true: list[str],
    y_pred: list[str],
    probability_rows: list[dict[str, float]],
) -> dict[str, float]:
    """Calculate approved metrics for per-row selected-model probabilities."""

    if len(y_true) != len(probability_rows):
        raise ValueError("y_true and probability_rows must have the same length")
    averaged_for_non_probability_metrics = mean_probabilities(probability_rows)
    metrics = calculate_metrics(y_true, y_pred, averaged_for_non_probability_metrics)
    metrics["log_loss"] = _per_row_log_loss(y_true, probability_rows)
    return metrics


def mean_probabilities(probability_rows: list[dict[str, float]]) -> dict[str, float]:
    """Return mean predicted probabilities by class for reporting."""

    if not probability_rows:
        raise ValueError("Cannot summarize empty probability rows")
    return {
        label: sum(row[label] for row in probability_rows) / len(probability_rows)
        for label in CLASS_ORDER
    }


def coefficient_rows(fit: SelectedModelFit) -> list[dict[str, str]]:
    """Return class-specific standardized coefficients for report writing."""

    _validate_model_class_set(fit.model)
    class_indexes = {str(label): index for index, label in enumerate(fit.model.classes_)}
    rows: list[dict[str, str]] = []
    for class_label in CLASS_ORDER:
        class_index = class_indexes[class_label]
        for feature_index, feature in enumerate(fit.feature_columns):
            rows.append(
                {
                    "class": class_label,
                    "feature": feature,
                    "coefficient": f"{fit.model.coef_[class_index][feature_index]:.12f}",
                }
            )
        rows.append(
            {
                "class": class_label,
                "feature": "intercept",
                "coefficient": f"{fit.model.intercept_[class_index]:.12f}",
            }
        )
    return rows


def _validate_model_class_set(model: LogisticRegression) -> None:
    if set(str(label) for label in model.classes_) != set(CLASS_ORDER):
        raise ValueError("Logistic Regression classes must be exactly H, D, A")


def _per_row_log_loss(
    y_true: list[str],
    probability_rows: list[dict[str, float]],
) -> float:
    epsilon = 1e-15
    total = 0.0
    for actual, probabilities in zip(y_true, probability_rows):
        probability = min(max(probabilities[actual], epsilon), 1.0 - epsilon)
        total -= float(np.log(probability))
    return total / len(y_true)


def _assert_probability_row_valid(probabilities: dict[str, float]) -> None:
    if tuple(probabilities.keys()) != CLASS_ORDER:
        raise ValueError("Probability class order must be H, D, A")
    total = sum(probabilities.values())
    if not np.isclose(total, 1.0, rtol=0.0, atol=1e-12):
        raise ValueError(f"Probability row must sum to 1, observed {total}")
    for label, value in probabilities.items():
        if not np.isfinite(value) or value < 0.0 or value > 1.0:
            raise ValueError(f"Invalid probability for {label}: {value}")
