#!/usr/bin/env python3
"""Build final baseline-vs-Logistic-Regression evaluation reports."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.statsport.evaluation import (
    compare_metric_reports,
    comparison_csv_fieldnames,
    comparison_to_csv_rows,
    draw_class_summary,
    generate_summary_markdown,
    load_confusion_matrix,
    load_metric_rows,
)


REPORT_DIR = REPO_ROOT / "outputs" / "reports"

BASELINE_TEST_METRICS_PATH = REPORT_DIR / "baseline_test_metrics.csv"
BASELINE_WALK_FORWARD_METRICS_PATH = REPORT_DIR / "baseline_walk_forward_metrics.csv"
BASELINE_TEST_CONFUSION_MATRIX_PATH = REPORT_DIR / "baseline_test_confusion_matrix.csv"

LOGISTIC_TEST_METRICS_PATH = REPORT_DIR / "logistic_regression_test_metrics.csv"
LOGISTIC_WALK_FORWARD_METRICS_PATH = REPORT_DIR / "logistic_regression_walk_forward_metrics.csv"
LOGISTIC_TEST_CONFUSION_MATRIX_PATH = REPORT_DIR / "logistic_regression_test_confusion_matrix.csv"

TEST_COMPARISON_PATH = REPORT_DIR / "model_comparison_test_metrics.csv"
WALK_FORWARD_COMPARISON_PATH = REPORT_DIR / "model_comparison_walk_forward_metrics.csv"
SUMMARY_PATH = REPORT_DIR / "model_comparison_summary.md"


def main() -> int:
    test_comparisons = compare_metric_reports(
        load_metric_rows(BASELINE_TEST_METRICS_PATH),
        load_metric_rows(LOGISTIC_TEST_METRICS_PATH),
    )
    walk_forward_comparisons = compare_metric_reports(
        load_metric_rows(BASELINE_WALK_FORWARD_METRICS_PATH),
        load_metric_rows(LOGISTIC_WALK_FORWARD_METRICS_PATH),
    )

    baseline_draw_summary = draw_class_summary(
        load_confusion_matrix(BASELINE_TEST_CONFUSION_MATRIX_PATH)
    )
    logistic_draw_summary = draw_class_summary(
        load_confusion_matrix(LOGISTIC_TEST_CONFUSION_MATRIX_PATH)
    )

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _write_comparison_csv(TEST_COMPARISON_PATH, test_comparisons, "test")
    _write_comparison_csv(
        WALK_FORWARD_COMPARISON_PATH,
        walk_forward_comparisons,
        "walk_forward",
    )
    SUMMARY_PATH.write_text(
        generate_summary_markdown(
            test_comparisons[0],
            walk_forward_comparisons,
            baseline_draw_summary,
            logistic_draw_summary,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "test_comparison_path": str(TEST_COMPARISON_PATH.relative_to(REPO_ROOT)),
                "walk_forward_comparison_path": str(
                    WALK_FORWARD_COMPARISON_PATH.relative_to(REPO_ROOT)
                ),
                "summary_path": str(SUMMARY_PATH.relative_to(REPO_ROOT)),
                "test_row_count": test_comparisons[0].row_count,
                "test_deltas": test_comparisons[0].deltas,
                "walk_forward_rows": [
                    comparison.row_count for comparison in walk_forward_comparisons
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _write_comparison_csv(path: Path, comparisons, scope: str) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=comparison_csv_fieldnames())
        writer.writeheader()
        writer.writerows(comparison_to_csv_rows(comparisons, scope))


if __name__ == "__main__":
    raise SystemExit(main())
