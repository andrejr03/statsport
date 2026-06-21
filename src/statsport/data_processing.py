"""Raw Football-Data.co.uk match processing for StatSport."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path
from typing import Iterable


RAW_SEASON_FILES: tuple[tuple[str, str], ...] = (
    ("2020/21", "football-data-co-uk_bundesliga_2020-2021.csv"),
    ("2021/22", "football-data-co-uk_bundesliga_2021-2022.csv"),
    ("2022/23", "football-data-co-uk_bundesliga_2022-2023.csv"),
    ("2023/24", "football-data-co-uk_bundesliga_2023-2024.csv"),
    ("2024/25", "football-data-co-uk_bundesliga_2024-2025.csv"),
)

REQUIRED_RAW_COLUMNS: tuple[str, ...] = (
    "Div",
    "Date",
    "Time",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
)

PROCESSED_COLUMNS: tuple[str, ...] = (
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
)

VALID_TARGETS = {"H", "D", "A"}


@dataclass(frozen=True)
class ProcessingSummary:
    """Summary of a processed dataset build."""

    output_path: Path
    total_rows: int
    season_row_counts: dict[str, int]
    target_distribution: dict[str, int]
    missingness: dict[str, int]


def validate_required_columns(fieldnames: Iterable[str] | None) -> None:
    """Raise ValueError when a raw CSV lacks required columns."""

    columns = set(fieldnames or [])
    missing = [column for column in REQUIRED_RAW_COLUMNS if column not in columns]
    if missing:
        raise ValueError(f"Missing required raw columns: {', '.join(missing)}")


def map_target_label(raw_target: str) -> str:
    """Map Football-Data.co.uk FTR values to the approved 1X2 labels."""

    target = raw_target.strip().upper()
    if target not in VALID_TARGETS:
        raise ValueError(f"Unexpected FTR value: {raw_target!r}")
    return target


def map_home_win_target(raw_target: str) -> int:
    """Map FTR to the approved fallback Home Win vs Not Home Win label."""

    return 1 if map_target_label(raw_target) == "H" else 0


def parse_match_date(raw_date: str) -> datetime.date:
    """Parse Football-Data.co.uk match dates to a date object."""

    value = raw_date.strip()
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Could not parse match date: {raw_date!r}")


def parse_kickoff_time(raw_time: str) -> time:
    """Parse kickoff time, using midnight when the source value is blank."""

    value = raw_time.strip()
    if not value:
        return time(0, 0)
    for fmt in ("%H:%M", "%H.%M"):
        try:
            return datetime.strptime(value, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Could not parse kickoff time: {raw_time!r}")


def process_raw_file(raw_path: Path, season: str) -> list[dict[str, str]]:
    """Process one raw season CSV into normalized match rows."""

    rows: list[dict[str, str]] = []
    with raw_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        validate_required_columns(reader.fieldnames)
        for raw_index, raw_row in enumerate(reader):
            if not any((value or "").strip() for value in raw_row.values()):
                continue

            match_date = parse_match_date(raw_row["Date"])
            kickoff_time = parse_kickoff_time(raw_row["Time"])
            target_1x2 = map_target_label(raw_row["FTR"])
            full_time_home_goals = _parse_int(raw_row["FTHG"], "FTHG")
            full_time_away_goals = _parse_int(raw_row["FTAG"], "FTAG")

            rows.append(
                {
                    "season": season,
                    "source_file": raw_path.name,
                    "division": raw_row["Div"].strip(),
                    "match_date": match_date.isoformat(),
                    "kickoff_time": kickoff_time.strftime("%H:%M"),
                    "home_team": raw_row["HomeTeam"].strip(),
                    "away_team": raw_row["AwayTeam"].strip(),
                    "full_time_home_goals": str(full_time_home_goals),
                    "full_time_away_goals": str(full_time_away_goals),
                    "target_1x2": target_1x2,
                    "target_home_win": str(map_home_win_target(target_1x2)),
                    "_season_order": str(_season_order(season)),
                    "_raw_index": str(raw_index),
                }
            )
    return rows


def process_all_raw_files(raw_dir: Path, output_path: Path) -> ProcessingSummary:
    """Process all approved raw files and write the normalized dataset."""

    processed_rows: list[dict[str, str]] = []
    for season, filename in RAW_SEASON_FILES:
        raw_path = raw_dir / filename
        if not raw_path.exists():
            raise FileNotFoundError(f"Missing approved raw file: {raw_path}")
        processed_rows.extend(process_raw_file(raw_path, season))

    processed_rows.sort(
        key=lambda row: (
            int(row["_season_order"]),
            row["match_date"],
            row["kickoff_time"],
            int(row["_raw_index"]),
        )
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROCESSED_COLUMNS)
        writer.writeheader()
        for row in processed_rows:
            writer.writerow({column: row[column] for column in PROCESSED_COLUMNS})

    return summarize_processed_rows(processed_rows, output_path)


def summarize_processed_file(output_path: Path) -> ProcessingSummary:
    """Read a processed dataset and return validation-friendly summary values."""

    with output_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return summarize_processed_rows(rows, output_path)


def summarize_processed_rows(
    rows: list[dict[str, str]],
    output_path: Path,
) -> ProcessingSummary:
    """Summarize processed rows without modifying them."""

    season_counts = Counter(row["season"] for row in rows)
    target_counts = Counter(row["target_1x2"] for row in rows)
    missingness = {
        column: sum(1 for row in rows if not (row.get(column) or "").strip())
        for column in PROCESSED_COLUMNS
    }
    return ProcessingSummary(
        output_path=output_path,
        total_rows=len(rows),
        season_row_counts=dict(sorted(season_counts.items())),
        target_distribution=dict(sorted(target_counts.items())),
        missingness=missingness,
    )


def assert_chronological(rows: list[dict[str, str]]) -> None:
    """Validate season/date/time ordering for processed rows."""

    observed = [
        (_season_order(row["season"]), row["match_date"], row["kickoff_time"])
        for row in rows
    ]
    if observed != sorted(observed):
        raise ValueError("Processed rows are not in chronological season/date/time order")


def _parse_int(raw_value: str, column: str) -> int:
    value = raw_value.strip()
    if not value:
        raise ValueError(f"Missing required numeric value in {column}")
    return int(value)


def _season_order(season: str) -> int:
    try:
        return [season for season, _ in RAW_SEASON_FILES].index(season)
    except ValueError as exc:
        raise ValueError(f"Unexpected season label: {season!r}") from exc

