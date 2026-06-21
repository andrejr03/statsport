"""Leakage-safe core feature engineering for StatSport."""

from __future__ import annotations

import csv
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path

from src.statsport.data_processing import PROCESSED_COLUMNS


ROLLING_WINDOW_MATCHES = 5

CORE_FEATURE_COLUMNS: tuple[str, ...] = (
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

FEATURE_DATASET_COLUMNS: tuple[str, ...] = PROCESSED_COLUMNS + CORE_FEATURE_COLUMNS

OPTIONAL_FEATURE_MARKERS: tuple[str, ...] = (
    "shots_on_target",
    "league_position",
    "elo",
)


@dataclass(frozen=True)
class FeatureSummary:
    """Summary of a generated feature dataset."""

    output_path: Path
    total_rows: int
    season_row_counts: dict[str, int]
    missingness: dict[str, int]
    feature_columns: tuple[str, ...]


def build_feature_rows(processed_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return match rows with leakage-safe pre-match core features."""

    sorted_rows = sorted(
        enumerate(processed_rows),
        key=lambda item: (
            item[1]["season"],
            item[1]["match_date"],
            item[1]["kickoff_time"],
            item[0],
        ),
    )
    team_history: dict[str, deque[dict[str, float]]] = {}
    feature_rows: list[dict[str, str]] = []

    for _, row in sorted_rows:
        home_team = row["home_team"]
        away_team = row["away_team"]
        home_history = team_history.setdefault(home_team, deque(maxlen=ROLLING_WINDOW_MATCHES))
        away_history = team_history.setdefault(away_team, deque(maxlen=ROLLING_WINDOW_MATCHES))

        home_stats = _history_averages(home_history)
        away_stats = _history_averages(away_history)

        feature_row = {column: row[column] for column in PROCESSED_COLUMNS}
        feature_row.update(
            {
                "home_advantage": "1",
                "home_recent_form_points_avg": _format_float(home_stats["points"]),
                "away_recent_form_points_avg": _format_float(away_stats["points"]),
                "recent_form_points_diff": _format_float(
                    home_stats["points"] - away_stats["points"]
                ),
                "home_goals_scored_avg": _format_float(home_stats["goals_scored"]),
                "away_goals_scored_avg": _format_float(away_stats["goals_scored"]),
                "goals_scored_diff": _format_float(
                    home_stats["goals_scored"] - away_stats["goals_scored"]
                ),
                "home_goals_conceded_avg": _format_float(home_stats["goals_conceded"]),
                "away_goals_conceded_avg": _format_float(away_stats["goals_conceded"]),
                "goals_conceded_diff": _format_float(
                    home_stats["goals_conceded"] - away_stats["goals_conceded"]
                ),
                "home_goal_difference_avg": _format_float(home_stats["goal_difference"]),
                "away_goal_difference_avg": _format_float(away_stats["goal_difference"]),
                "goal_difference_diff": _format_float(
                    home_stats["goal_difference"] - away_stats["goal_difference"]
                ),
            }
        )
        feature_rows.append(feature_row)

        home_goals = int(row["full_time_home_goals"])
        away_goals = int(row["full_time_away_goals"])
        home_points, away_points = _points_from_goals(home_goals, away_goals)
        home_history.append(
            {
                "points": float(home_points),
                "goals_scored": float(home_goals),
                "goals_conceded": float(away_goals),
                "goal_difference": float(home_goals - away_goals),
            }
        )
        away_history.append(
            {
                "points": float(away_points),
                "goals_scored": float(away_goals),
                "goals_conceded": float(home_goals),
                "goal_difference": float(away_goals - home_goals),
            }
        )

    return feature_rows


def build_feature_dataset(processed_path: Path, output_path: Path) -> FeatureSummary:
    """Read a processed dataset, generate core features, and write the feature dataset."""

    with processed_path.open(newline="", encoding="utf-8") as handle:
        processed_rows = list(csv.DictReader(handle))

    validate_processed_columns(processed_rows)
    feature_rows = build_feature_rows(processed_rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FEATURE_DATASET_COLUMNS)
        writer.writeheader()
        writer.writerows(feature_rows)

    return summarize_feature_rows(feature_rows, output_path)


def validate_processed_columns(rows: list[dict[str, str]]) -> None:
    """Validate the input rows contain the Milestone 2 processed columns."""

    if not rows:
        raise ValueError("Processed dataset is empty")
    columns = set(rows[0])
    missing = [column for column in PROCESSED_COLUMNS if column not in columns]
    if missing:
        raise ValueError(f"Missing processed columns: {', '.join(missing)}")


def summarize_feature_file(output_path: Path) -> FeatureSummary:
    """Read a feature dataset and summarize it."""

    with output_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return summarize_feature_rows(rows, output_path)


def summarize_feature_rows(rows: list[dict[str, str]], output_path: Path) -> FeatureSummary:
    """Summarize generated feature rows."""

    season_counts = Counter(row["season"] for row in rows)
    missingness = {
        column: sum(1 for row in rows if not (row.get(column) or "").strip())
        for column in FEATURE_DATASET_COLUMNS
    }
    return FeatureSummary(
        output_path=output_path,
        total_rows=len(rows),
        season_row_counts=dict(sorted(season_counts.items())),
        missingness=missingness,
        feature_columns=CORE_FEATURE_COLUMNS,
    )


def optional_features_present(columns: list[str]) -> list[str]:
    """Return optional feature markers found in a list of columns."""

    found: list[str] = []
    for column in columns:
        lower = column.lower()
        if any(marker in lower for marker in OPTIONAL_FEATURE_MARKERS):
            found.append(column)
    return found


def assert_feature_chronological(rows: list[dict[str, str]]) -> None:
    """Validate season/date/time ordering for feature rows."""

    observed = [(row["season"], row["match_date"], row["kickoff_time"]) for row in rows]
    if observed != sorted(observed):
        raise ValueError("Feature rows are not in chronological season/date/time order")


def _history_averages(history: deque[dict[str, float]]) -> dict[str, float]:
    if not history:
        return {
            "points": 0.0,
            "goals_scored": 0.0,
            "goals_conceded": 0.0,
            "goal_difference": 0.0,
        }
    denominator = float(len(history))
    return {
        "points": sum(item["points"] for item in history) / denominator,
        "goals_scored": sum(item["goals_scored"] for item in history) / denominator,
        "goals_conceded": sum(item["goals_conceded"] for item in history) / denominator,
        "goal_difference": sum(item["goal_difference"] for item in history) / denominator,
    }


def _points_from_goals(home_goals: int, away_goals: int) -> tuple[int, int]:
    if home_goals > away_goals:
        return 3, 0
    if home_goals < away_goals:
        return 0, 3
    return 1, 1


def _format_float(value: float) -> str:
    return f"{value:.6f}"

