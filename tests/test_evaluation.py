import csv
import tempfile
import unittest
from pathlib import Path

from src.statsport.evaluation import (
    CORE_METRICS,
    ReportMetricRow,
    compare_metric_reports,
    compare_metric_rows,
    comparison_csv_fieldnames,
    comparison_to_csv_rows,
    draw_class_summary,
    generate_summary_markdown,
    load_metric_rows,
)


class EvaluationComparisonTests(unittest.TestCase):
    def test_metric_delta_calculations(self):
        comparison = compare_metric_rows(_baseline_row(), _selected_row())

        self.assertAlmostEqual(comparison.deltas["accuracy"], 0.1)
        self.assertAlmostEqual(comparison.deltas["balanced_accuracy"], 0.05)
        self.assertAlmostEqual(comparison.deltas["log_loss"], -0.2)
        self.assertAlmostEqual(comparison.deltas["macro_f1"], 0.2)

    def test_lower_log_loss_is_handled_as_improvement(self):
        comparison = compare_metric_rows(_baseline_row(), _selected_row())

        self.assertTrue(comparison.improved["log_loss"])
        self.assertTrue(comparison.improved["accuracy"])

    def test_identical_test_split_validation(self):
        selected = _selected_row(evaluation_season="2023/24")

        with self.assertRaisesRegex(ValueError, "evaluation_season"):
            compare_metric_rows(_baseline_row(), selected)

    def test_identical_walk_forward_fold_validation(self):
        baseline_rows = [
            _baseline_row(split="walk_forward_1", evaluation_season="2021/22"),
            _baseline_row(split="walk_forward_2", evaluation_season="2022/23"),
        ]
        selected_rows = [
            _selected_row(split="walk_forward_1", evaluation_season="2021/22"),
            _selected_row(split="walk_forward_3", evaluation_season="2023/24"),
        ]

        with self.assertRaisesRegex(ValueError, "split"):
            compare_metric_reports(baseline_rows, selected_rows)

    def test_missing_report_file_handling(self):
        with self.assertRaises(FileNotFoundError):
            load_metric_rows(Path("does-not-exist.csv"))

    def test_summary_structure_mentions_core_interpretation(self):
        comparison = compare_metric_rows(_baseline_row(), _selected_row())
        baseline_draw = draw_class_summary(_matrix(correct_draws=0, predicted_draw_total=0))
        selected_draw = draw_class_summary(_matrix(correct_draws=1, predicted_draw_total=2))

        summary = generate_summary_markdown(
            comparison,
            [comparison],
            baseline_draw,
            selected_draw,
        )

        self.assertIn("# StatSport Model Comparison Summary", summary)
        self.assertIn("Lower Log Loss is better", summary)
        self.assertIn("Draw-class performance remains a clear limitation", summary)
        self.assertIn(
            "Optional Brier Score and calibration assessment were not implemented",
            summary,
        )

    def test_deterministic_output_generation(self):
        comparison = compare_metric_rows(_baseline_row(), _selected_row())

        first_rows = comparison_to_csv_rows([comparison], "test")
        second_rows = comparison_to_csv_rows([comparison], "test")

        self.assertEqual(first_rows, second_rows)
        self.assertEqual(comparison_csv_fieldnames(), comparison_csv_fieldnames())

    def test_loading_metric_rows_from_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "metrics.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "split",
                        "train_seasons",
                        "evaluation_season",
                        "row_count",
                        *CORE_METRICS,
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "split": "test",
                        "train_seasons": "2020/21",
                        "evaluation_season": "2021/22",
                        "row_count": "306",
                        "accuracy": "0.4",
                        "balanced_accuracy": "0.3",
                        "log_loss": "1.1",
                        "macro_f1": "0.2",
                    }
                )

            rows = load_metric_rows(path)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].row_count, 306)
        self.assertEqual(rows[0].metrics["log_loss"], 1.1)


def _baseline_row(**overrides) -> ReportMetricRow:
    values = {
        "split": "test",
        "train_seasons": "2020/21;2021/22",
        "evaluation_season": "2022/23",
        "row_count": 306,
        "metrics": {
            "accuracy": 0.4,
            "balanced_accuracy": 0.3,
            "log_loss": 1.2,
            "macro_f1": 0.2,
        },
    }
    values.update(overrides)
    return ReportMetricRow(**values)


def _selected_row(**overrides) -> ReportMetricRow:
    values = {
        "split": "test",
        "train_seasons": "2020/21;2021/22",
        "evaluation_season": "2022/23",
        "row_count": 306,
        "metrics": {
            "accuracy": 0.5,
            "balanced_accuracy": 0.35,
            "log_loss": 1.0,
            "macro_f1": 0.4,
        },
    }
    values.update(overrides)
    return ReportMetricRow(**values)


def _matrix(correct_draws: int, predicted_draw_total: int) -> dict[str, dict[str, int]]:
    away_predicted_draws = predicted_draw_total - correct_draws
    return {
        "H": {"H": 10, "D": 0, "A": 0},
        "D": {"H": 2, "D": correct_draws, "A": 3},
        "A": {"H": 4, "D": away_predicted_draws, "A": 5},
    }


if __name__ == "__main__":
    unittest.main()
