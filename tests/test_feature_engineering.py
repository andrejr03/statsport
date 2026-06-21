import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from src.statsport.feature_engineering import (
    CORE_FEATURE_COLUMNS,
    FEATURE_DATASET_COLUMNS,
    ROLLING_WINDOW_MATCHES,
    assert_feature_chronological,
    build_feature_dataset,
    build_feature_rows,
    optional_features_present,
)


class FeatureEngineeringTests(unittest.TestCase):
    def test_rolling_calculations_use_prior_matches_only(self):
        rows = [
            _processed_row("2020/21", "2020-09-18", "19:30", "Alpha", "Beta", 2, 0, "H"),
            _processed_row("2020/21", "2020-09-25", "19:30", "Alpha", "Beta", 1, 1, "D"),
        ]

        features = build_feature_rows(rows)

        self.assertEqual(features[0]["home_recent_form_points_avg"], "0.000000")
        self.assertEqual(features[0]["away_recent_form_points_avg"], "0.000000")
        self.assertEqual(features[1]["home_recent_form_points_avg"], "3.000000")
        self.assertEqual(features[1]["away_recent_form_points_avg"], "0.000000")
        self.assertEqual(features[1]["home_goals_scored_avg"], "2.000000")
        self.assertEqual(features[1]["away_goals_conceded_avg"], "2.000000")
        self.assertEqual(features[1]["home_goal_difference_avg"], "2.000000")
        self.assertEqual(features[1]["away_goal_difference_avg"], "-2.000000")

    def test_window_uses_last_five_prior_matches(self):
        rows = []
        for index in range(6):
            rows.append(
                _processed_row(
                    "2020/21",
                    f"2020-09-{18 + index:02d}",
                    "15:30",
                    "Alpha",
                    f"Opponent {index}",
                    index,
                    0,
                    "H" if index > 0 else "D",
                )
            )

        features = build_feature_rows(rows)

        self.assertEqual(ROLLING_WINDOW_MATCHES, 5)
        self.assertEqual(features[5]["home_goals_scored_avg"], "2.000000")
        self.assertEqual(features[5]["home_goal_difference_avg"], "2.000000")

    def test_row_count_feature_presence_and_optional_absence(self):
        rows = [
            _processed_row("2020/21", "2020-09-18", "19:30", "Alpha", "Beta", 2, 0, "H"),
            _processed_row("2020/21", "2020-09-19", "15:30", "Gamma", "Delta", 1, 1, "D"),
        ]

        features = build_feature_rows(rows)

        self.assertEqual(len(features), len(rows))
        self.assertEqual(list(features[0].keys()), list(FEATURE_DATASET_COLUMNS))
        for column in CORE_FEATURE_COLUMNS:
            self.assertIn(column, features[0])
        self.assertEqual(optional_features_present(list(features[0].keys())), [])

    def test_generation_is_deterministic(self):
        rows = [
            _processed_row("2020/21", "2020-09-18", "19:30", "Alpha", "Beta", 2, 0, "H"),
            _processed_row("2020/21", "2020-09-25", "19:30", "Alpha", "Beta", 1, 1, "D"),
        ]

        self.assertEqual(build_feature_rows(rows), build_feature_rows(rows))

    def test_output_is_chronological_even_when_input_is_not(self):
        rows = [
            _processed_row("2020/21", "2020-09-25", "19:30", "Alpha", "Beta", 1, 1, "D"),
            _processed_row("2020/21", "2020-09-18", "19:30", "Alpha", "Beta", 2, 0, "H"),
        ]

        features = build_feature_rows(rows)

        self.assertEqual(features[0]["match_date"], "2020-09-18")
        assert_feature_chronological(features)

    def test_feature_dataset_does_not_mutate_processed_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            processed_path = Path(tmp) / "processed.csv"
            output_path = Path(tmp) / "features.csv"
            _write_processed_csv(
                processed_path,
                [
                    _processed_row("2020/21", "2020-09-18", "19:30", "Alpha", "Beta", 2, 0, "H"),
                    _processed_row("2020/21", "2020-09-25", "19:30", "Alpha", "Beta", 1, 1, "D"),
                ],
            )
            before_hash = _sha256(processed_path)
            before_mtime = processed_path.stat().st_mtime_ns

            summary = build_feature_dataset(processed_path, output_path)

            self.assertEqual(summary.total_rows, 2)
            self.assertEqual(_sha256(processed_path), before_hash)
            self.assertEqual(processed_path.stat().st_mtime_ns, before_mtime)


def _processed_row(
    season: str,
    match_date: str,
    kickoff_time: str,
    home_team: str,
    away_team: str,
    home_goals: int,
    away_goals: int,
    target: str,
) -> dict[str, str]:
    return {
        "season": season,
        "source_file": "test.csv",
        "division": "D1",
        "match_date": match_date,
        "kickoff_time": kickoff_time,
        "home_team": home_team,
        "away_team": away_team,
        "full_time_home_goals": str(home_goals),
        "full_time_away_goals": str(away_goals),
        "target_1x2": target,
        "target_home_win": "1" if target == "H" else "0",
    }


def _write_processed_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "season",
                "source_file",
                "division",
                "match_date",
                "kickoff_time",
                "home_team",
                "away_team",
                "full_time_home_goals",
                "full_time_away_goals",
                "target_1x2",
                "target_home_win",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    unittest.main()
