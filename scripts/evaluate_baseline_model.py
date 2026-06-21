#!/usr/bin/env python3
"""Evaluate the StatSport home-advantage baseline model."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.statsport.baseline import CLASS_ORDER, evaluate_baseline, load_feature_rows


FEATURE_PATH = REPO_ROOT / "data" / "processed" / "bundesliga_2020_2025_features.csv"
REPORT_DIR = REPO_ROOT / "outputs" / "reports"
TEST_METRICS_PATH = REPORT_DIR / "baseline_test_metrics.csv"
WALK_FORWARD_METRICS_PATH = REPORT_DIR / "baseline_walk_forward_metrics.csv"
TEST_CONFUSION_MATRIX_PATH = REPORT_DIR / "baseline_test_confusion_matrix.csv"


def main() -> int:
    rows = load_feature_rows(FEATURE_PATH)
    test_result, fold_results = evaluate_baseline(rows)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _write_metrics(TEST_METRICS_PATH, [test_result])
    _write_metrics(WALK_FORWARD_METRICS_PATH, fold_results)
    _write_confusion_matrix(TEST_CONFUSION_MATRIX_PATH, test_result.confusion_matrix)

    print(
        json.dumps(
            {
                "test_metrics_path": str(TEST_METRICS_PATH.relative_to(REPO_ROOT)),
                "walk_forward_metrics_path": str(
                    WALK_FORWARD_METRICS_PATH.relative_to(REPO_ROOT)
                ),
                "test_confusion_matrix_path": str(
                    TEST_CONFUSION_MATRIX_PATH.relative_to(REPO_ROOT)
                ),
                "test_row_count": test_result.row_count,
                "test_metrics": test_result.metrics,
                "walk_forward_rows": [result.row_count for result in fold_results],
                "class_order": list(CLASS_ORDER),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _write_metrics(path: Path, results) -> None:
    fieldnames = [
        "split",
        "train_seasons",
        "evaluation_season",
        "row_count",
        "probability_H",
        "probability_D",
        "probability_A",
        "accuracy",
        "balanced_accuracy",
        "log_loss",
        "macro_f1",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "split": result.split,
                    "train_seasons": ";".join(result.train_seasons),
                    "evaluation_season": result.evaluation_season,
                    "row_count": result.row_count,
                    "probability_H": _format_float(result.probabilities["H"]),
                    "probability_D": _format_float(result.probabilities["D"]),
                    "probability_A": _format_float(result.probabilities["A"]),
                    "accuracy": _format_float(result.metrics["accuracy"]),
                    "balanced_accuracy": _format_float(result.metrics["balanced_accuracy"]),
                    "log_loss": _format_float(result.metrics["log_loss"]),
                    "macro_f1": _format_float(result.metrics["macro_f1"]),
                }
            )


def _write_confusion_matrix(path: Path, matrix: dict[str, dict[str, int]]) -> None:
    fieldnames = ["actual"] + [f"predicted_{label}" for label in CLASS_ORDER]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for actual in CLASS_ORDER:
            row = {"actual": actual}
            row.update({f"predicted_{label}": matrix[actual][label] for label in CLASS_ORDER})
            writer.writerow(row)


def _format_float(value: float) -> str:
    return f"{value:.12f}"


if __name__ == "__main__":
    raise SystemExit(main())
