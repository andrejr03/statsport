import unittest

import numpy as np

from src.statsport.baseline import (
    CLASS_ORDER,
    build_walk_forward_splits,
    split_train_test,
)
from src.statsport.selected_model import (
    FEATURE_COLUMNS,
    coefficient_rows,
    evaluate_selected_model,
    fit_selected_model,
    predict_classes,
    predict_probabilities,
    select_feature_columns,
    transform_features,
)


class SelectedModelTests(unittest.TestCase):
    def test_approved_feature_column_selection(self):
        rows = [_feature_row("2020/21", "H", 1.0)]

        self.assertEqual(select_feature_columns(rows), FEATURE_COLUMNS)
        self.assertEqual(FEATURE_COLUMNS[0], "home_advantage")
        self.assertIn("goal_difference_diff", FEATURE_COLUMNS)

    def test_preprocessing_is_fitted_on_training_rows_only(self):
        training_rows = [
            _feature_row("2020/21", "H", 1.0),
            _feature_row("2020/21", "D", 2.0),
            _feature_row("2020/21", "A", 3.0),
        ]
        evaluation_rows = [_feature_row("2021/22", "H", 100.0)]

        fit = fit_selected_model(training_rows)
        transformed = transform_features(fit, evaluation_rows)

        self.assertAlmostEqual(fit.scaler.mean_[1], 3.0)
        self.assertGreater(transformed[0][1], 100.0)

    def test_probability_outputs_sum_to_one_in_stable_class_order(self):
        training_rows = _training_fixture()
        fit = fit_selected_model(training_rows)

        probabilities = predict_probabilities(fit, training_rows[:3])

        for row in probabilities:
            self.assertEqual(tuple(row.keys()), CLASS_ORDER)
            self.assertTrue(np.isclose(sum(row.values()), 1.0))

    def test_predictions_contain_only_approved_classes(self):
        training_rows = _training_fixture()
        fit = fit_selected_model(training_rows)

        predictions = predict_classes(fit, training_rows)

        self.assertTrue(set(predictions).issubset(set(CLASS_ORDER)))

    def test_split_reuse_matches_baseline_definitions(self):
        rows = _season_fixture()

        train_rows, test_rows = split_train_test(rows)
        folds = build_walk_forward_splits(rows)

        self.assertEqual(
            [row["season"] for row in train_rows],
            ["2020/21", "2021/22", "2022/23", "2023/24"],
        )
        self.assertEqual([row["season"] for row in test_rows], ["2024/25"])
        self.assertEqual(
            [(train, validation) for train, validation, _, _ in folds],
            [
                (("2020/21",), "2021/22"),
                (("2020/21", "2021/22"), "2022/23"),
                (("2020/21", "2021/22", "2022/23"), "2023/24"),
            ],
        )

    def test_coefficients_are_available_for_each_class_and_feature(self):
        fit = fit_selected_model(_training_fixture())

        rows = coefficient_rows(fit)

        self.assertEqual(len(rows), len(CLASS_ORDER) * (len(FEATURE_COLUMNS) + 1))
        self.assertEqual(
            [row["class"] for row in rows[: len(FEATURE_COLUMNS) + 1]],
            ["H"] * (len(FEATURE_COLUMNS) + 1),
        )
        self.assertEqual(rows[len(FEATURE_COLUMNS)]["feature"], "intercept")

    def test_training_and_evaluation_are_deterministic(self):
        rows = _full_evaluation_fixture()

        first_test, first_folds = evaluate_selected_model(rows)
        second_test, second_folds = evaluate_selected_model(rows)

        self.assertEqual(first_test.evaluation.metrics, second_test.evaluation.metrics)
        self.assertEqual(
            first_test.evaluation.confusion_matrix,
            second_test.evaluation.confusion_matrix,
        )
        self.assertEqual(
            [result.evaluation.metrics for result in first_folds],
            [result.evaluation.metrics for result in second_folds],
        )
        self.assertEqual(
            coefficient_rows(first_test.fit),
            coefficient_rows(second_test.fit),
        )


def _feature_row(season: str, target: str, base: float) -> dict[str, str]:
    row = {
        "season": season,
        "target_1x2": target,
    }
    for index, column in enumerate(FEATURE_COLUMNS):
        row[column] = f"{base + index:.6f}"
    row["home_advantage"] = "1.000000"
    return row


def _training_fixture() -> list[dict[str, str]]:
    return [
        _feature_row("2020/21", "H", 1.0),
        _feature_row("2020/21", "D", 2.0),
        _feature_row("2020/21", "A", 3.0),
        _feature_row("2020/21", "H", 4.0),
        _feature_row("2020/21", "D", 5.0),
        _feature_row("2020/21", "A", 6.0),
    ]


def _season_fixture() -> list[dict[str, str]]:
    return [
        _feature_row("2020/21", "H", 1.0),
        _feature_row("2021/22", "D", 2.0),
        _feature_row("2022/23", "A", 3.0),
        _feature_row("2023/24", "H", 4.0),
        _feature_row("2024/25", "D", 5.0),
    ]


def _full_evaluation_fixture() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    season_bases = {
        "2020/21": 1.0,
        "2021/22": 10.0,
        "2022/23": 20.0,
        "2023/24": 30.0,
        "2024/25": 40.0,
    }
    for season, base in season_bases.items():
        rows.extend(
            [
                _feature_row(season, "H", base),
                _feature_row(season, "D", base + 1.0),
                _feature_row(season, "A", base + 2.0),
            ]
        )
    return rows


if __name__ == "__main__":
    unittest.main()
