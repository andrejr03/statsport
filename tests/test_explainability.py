import unittest

from src.statsport.baseline import CLASS_ORDER
from src.statsport.explainability import (
    global_influence_markdown,
    limitations_markdown,
    rank_global_features,
    select_explanation_examples,
    training_feature_stats,
    explain_row,
    prediction_card_markdown,
)
from src.statsport.selected_model import FEATURE_COLUMNS


class ExplainabilityTests(unittest.TestCase):
    def test_coefficient_ranking_generation(self):
        rankings = rank_global_features(_coefficients())

        home_rows = [row for row in rankings if row["class"] == "H"]

        self.assertEqual(home_rows[0]["feature"], "goals_scored_diff")
        self.assertEqual(home_rows[0]["rank"], "1")
        self.assertIn("raises the model's Home score", home_rows[0]["interpretation"])

    def test_stable_class_ordering(self):
        rankings = rank_global_features(_coefficients())

        classes_by_block = [
            rankings[index * len(FEATURE_COLUMNS)]["class"]
            for index in range(len(CLASS_ORDER))
        ]

        self.assertEqual(classes_by_block, list(CLASS_ORDER))

    def test_deterministic_example_selection(self):
        rows = _rows()
        coefficients = _coefficients()
        stats = training_feature_stats(rows)

        first = select_explanation_examples(rows, coefficients, stats)
        second = select_explanation_examples(rows, coefficients, stats)

        self.assertEqual([example.category for example in first], [
            "strong_correct_prediction",
            "difficult_draw_or_draw_adjacent_prediction",
            "incorrect_or_low_confidence_prediction",
        ])
        self.assertEqual(
            [example.row["home_team"] for example in first],
            [example.row["home_team"] for example in second],
        )
        self.assertEqual(len({example.row["home_team"] for example in first}), 3)

    def test_local_explanation_generation(self):
        rows = _rows()
        coefficients = _coefficients()
        stats = training_feature_stats(rows)

        explanation = explain_row(rows[-1], coefficients, stats)

        self.assertIn(explanation.predicted_class, CLASS_ORDER)
        self.assertEqual(len(explanation.top_contributions), 5)
        self.assertEqual(len(explanation.difference_context), 4)
        self.assertIn("raw_value", explanation.top_contributions[0])

    def test_probability_explanation_generation(self):
        rows = _rows()
        coefficients = _coefficients()
        stats = training_feature_stats(rows)

        explanation = explain_row(rows[-1], coefficients, stats)

        self.assertEqual(tuple(explanation.probabilities.keys()), CLASS_ORDER)
        self.assertAlmostEqual(sum(explanation.probabilities.values()), 1.0)

    def test_output_reproducibility(self):
        rows = _rows()
        coefficients = _coefficients()
        rankings = rank_global_features(coefficients)
        stats = training_feature_stats(rows)
        example = select_explanation_examples(rows, coefficients, stats)[0]

        first = (
            global_influence_markdown(rankings),
            prediction_card_markdown(example, 1),
            limitations_markdown(),
        )
        second = (
            global_influence_markdown(rankings),
            prediction_card_markdown(example, 1),
            limitations_markdown(),
        )

        self.assertEqual(first, second)
        self.assertIn("# Prediction Explanation Card 1", first[1])
        self.assertIn("Draw-class weakness", first[2])


def _coefficients() -> dict[str, dict[str, float]]:
    coefficients = {
        class_label: {feature: 0.0 for feature in FEATURE_COLUMNS}
        for class_label in CLASS_ORDER
    }
    coefficients["H"].update(
        {
            "goals_scored_diff": 1.2,
            "goal_difference_diff": 0.8,
            "away_goals_scored_avg": -0.4,
            "intercept": 0.2,
        }
    )
    coefficients["D"].update(
        {
            "recent_form_points_diff": -0.6,
            "goals_scored_diff": -0.5,
            "intercept": 0.0,
        }
    )
    coefficients["A"].update(
        {
            "goals_scored_diff": -1.0,
            "goal_difference_diff": -0.9,
            "away_goals_scored_avg": 0.5,
            "intercept": -0.1,
        }
    )
    for class_label in CLASS_ORDER:
        coefficients[class_label].setdefault("intercept", 0.0)
    return coefficients


def _rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(
        [
            _row("2020/21", "2020-09-01", "Train H1", "Train A1", "H", 1.0, 1.0),
            _row("2021/22", "2021-09-01", "Train H2", "Train A2", "D", 0.0, 0.0),
            _row("2022/23", "2022-09-01", "Train H3", "Train A3", "A", -1.0, -1.0),
            _row("2023/24", "2023-09-01", "Train H4", "Train A4", "H", 0.5, 0.5),
            _row("2024/25", "2024-09-01", "Strong Home", "Away One", "H", 2.0, 2.0),
            _row("2024/25", "2024-09-02", "Draw Case", "Away Two", "D", 0.0, 0.0),
            _row("2024/25", "2024-09-03", "Wrong Home", "Away Three", "A", 0.3, 0.3),
            _row("2024/25", "2024-09-04", "Away Case", "Away Four", "A", -2.0, -2.0),
        ]
    )
    return rows


def _row(
    season: str,
    match_date: str,
    home_team: str,
    away_team: str,
    target: str,
    scoring_edge: float,
    goal_difference_edge: float,
) -> dict[str, str]:
    row = {
        "season": season,
        "match_date": match_date,
        "kickoff_time": "15:30",
        "home_team": home_team,
        "away_team": away_team,
        "full_time_home_goals": "2" if target == "H" else "1",
        "full_time_away_goals": "0" if target == "H" else "1",
        "target_1x2": target,
    }
    for feature in FEATURE_COLUMNS:
        row[feature] = "0.000000"
    row["home_advantage"] = "1.000000"
    row["goals_scored_diff"] = f"{scoring_edge:.6f}"
    row["goal_difference_diff"] = f"{goal_difference_edge:.6f}"
    row["recent_form_points_diff"] = f"{scoring_edge / 2:.6f}"
    row["goals_conceded_diff"] = f"{-goal_difference_edge / 2:.6f}"
    row["away_goals_scored_avg"] = f"{max(0.0, -scoring_edge):.6f}"
    return row


if __name__ == "__main__":
    unittest.main()
