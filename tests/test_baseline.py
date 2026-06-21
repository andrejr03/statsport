import math
import unittest

from src.statsport.baseline import (
    CLASS_ORDER,
    TEST_SEASON,
    TRAIN_SEASONS,
    WALK_FORWARD_FOLDS,
    balanced_accuracy,
    build_walk_forward_splits,
    calculate_metrics,
    confusion_matrix,
    derive_class_probabilities,
    evaluate_split,
    log_loss,
    macro_f1,
    predict_home_win,
    split_train_test,
)


class BaselineTests(unittest.TestCase):
    def test_home_advantage_prediction_is_constant_home_win(self):
        rows = [_row("2024/25", "A"), _row("2024/25", "D"), _row("2024/25", "H")]

        self.assertEqual(predict_home_win(rows), ["H", "H", "H"])

    def test_probabilities_sum_to_one_and_follow_stable_class_order(self):
        rows = [
            _row("2020/21", "H"),
            _row("2020/21", "H"),
            _row("2020/21", "D"),
            _row("2020/21", "A"),
        ]

        probabilities = derive_class_probabilities(rows)

        self.assertEqual(tuple(probabilities.keys()), CLASS_ORDER)
        self.assertEqual(CLASS_ORDER, ("H", "D", "A"))
        self.assertTrue(math.isclose(sum(probabilities.values()), 1.0))
        self.assertEqual(probabilities, {"H": 0.5, "D": 0.25, "A": 0.25})

    def test_probabilities_are_derived_only_from_training_rows(self):
        training_rows = [_row("2020/21", "H"), _row("2020/21", "H"), _row("2020/21", "D")]
        validation_rows = [_row("2021/22", "A"), _row("2021/22", "A"), _row("2021/22", "A")]

        result = evaluate_split("fixture", ("2020/21",), "2021/22", training_rows, validation_rows)

        self.assertEqual(result.probabilities, {"H": 2 / 3, "D": 1 / 3, "A": 0.0})

    def test_metric_correctness_on_deterministic_fixture(self):
        y_true = ["H", "D", "A", "H"]
        y_pred = ["H", "H", "H", "H"]
        probabilities = {"H": 0.5, "D": 0.25, "A": 0.25}

        metrics = calculate_metrics(y_true, y_pred, probabilities)

        self.assertAlmostEqual(metrics["accuracy"], 0.5)
        self.assertAlmostEqual(metrics["balanced_accuracy"], 1 / 3)
        expected_loss = -(
            math.log(0.5) + math.log(0.25) + math.log(0.25) + math.log(0.5)
        ) / 4
        self.assertAlmostEqual(metrics["log_loss"], expected_loss)
        self.assertAlmostEqual(metrics["macro_f1"], 2 / 9)
        self.assertEqual(balanced_accuracy(y_true, y_pred), 1 / 3)
        self.assertAlmostEqual(log_loss(y_true, probabilities), expected_loss)
        self.assertAlmostEqual(macro_f1(y_true, y_pred), 2 / 9)

    def test_confusion_matrix_uses_stable_actual_by_predicted_order(self):
        matrix = confusion_matrix(["H", "D", "A", "H"], ["H", "H", "H", "D"])

        self.assertEqual(list(matrix.keys()), list(CLASS_ORDER))
        self.assertEqual(matrix["H"], {"H": 1, "D": 1, "A": 0})
        self.assertEqual(matrix["D"], {"H": 1, "D": 0, "A": 0})
        self.assertEqual(matrix["A"], {"H": 1, "D": 0, "A": 0})

    def test_chronological_split_correctness(self):
        rows = _season_rows()

        train_rows, test_rows = split_train_test(rows)

        self.assertEqual(TRAIN_SEASONS, ("2020/21", "2021/22", "2022/23", "2023/24"))
        self.assertEqual(TEST_SEASON, "2024/25")
        self.assertEqual([row["season"] for row in train_rows], list(TRAIN_SEASONS))
        self.assertEqual([row["season"] for row in test_rows], ["2024/25"])

    def test_walk_forward_fold_correctness(self):
        rows = _season_rows()

        splits = build_walk_forward_splits(rows)

        observed_folds = [(train, validation) for train, validation, _, _ in splits]
        observed_validation_seasons = [
            validation_rows[0]["season"] for _, _, _, validation_rows in splits
        ]

        self.assertEqual(observed_folds, list(WALK_FORWARD_FOLDS))
        self.assertEqual([len(train_rows) for _, _, train_rows, _ in splits], [1, 2, 3])
        self.assertEqual(observed_validation_seasons, ["2021/22", "2022/23", "2023/24"])


def _row(season: str, target: str) -> dict[str, str]:
    return {"season": season, "target_1x2": target}


def _season_rows() -> list[dict[str, str]]:
    return [
        _row("2020/21", "H"),
        _row("2021/22", "D"),
        _row("2022/23", "A"),
        _row("2023/24", "H"),
        _row("2024/25", "D"),
    ]


if __name__ == "__main__":
    unittest.main()
