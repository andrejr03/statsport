import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from src.statsport.data_processing import (
    PROCESSED_COLUMNS,
    assert_chronological,
    map_home_win_target,
    map_target_label,
    process_all_raw_files,
    process_raw_file,
    validate_required_columns,
)


RAW_FILENAMES = (
    "football-data-co-uk_bundesliga_2020-2021.csv",
    "football-data-co-uk_bundesliga_2021-2022.csv",
    "football-data-co-uk_bundesliga_2022-2023.csv",
    "football-data-co-uk_bundesliga_2023-2024.csv",
    "football-data-co-uk_bundesliga_2024-2025.csv",
)


class DataProcessingTests(unittest.TestCase):
    def test_required_column_validation_rejects_missing_column(self):
        with self.assertRaisesRegex(ValueError, "FTR"):
            validate_required_columns(
                ["Div", "Date", "Time", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]
            )

    def test_target_label_mapping_accepts_only_1x2_values(self):
        self.assertEqual(map_target_label("H"), "H")
        self.assertEqual(map_target_label("d"), "D")
        self.assertEqual(map_target_label(" A "), "A")
        with self.assertRaisesRegex(ValueError, "Unexpected FTR"):
            map_target_label("X")

    def test_fallback_label_mapping_is_binary_and_deterministic(self):
        self.assertEqual(map_home_win_target("H"), 1)
        self.assertEqual(map_home_win_target("D"), 0)
        self.assertEqual(map_home_win_target("A"), 0)

    def test_processing_preserves_chronological_order_and_row_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw_dir = Path(tmp) / "raw"
            raw_dir.mkdir()
            _write_raw_csv(
                raw_dir / RAW_FILENAMES[0],
                [
                    ["D1", "19/09/2020", "14:30", "Team C", "Team D", "0", "1", "A"],
                    ["D1", "18/09/2020", "19:30", "Team A", "Team B", "2", "0", "H"],
                ],
            )
            for filename in RAW_FILENAMES[1:]:
                _write_raw_csv(
                    raw_dir / filename,
                    [["D1", "01/08/2021", "15:30", "Team E", "Team F", "1", "1", "D"]],
                )

            output_path = Path(tmp) / "processed.csv"
            summary = process_all_raw_files(raw_dir, output_path)

            rows = _read_processed(output_path)
            self.assertEqual(summary.total_rows, 6)
            self.assertEqual(len(rows), 6)
            self.assertEqual(list(rows[0].keys()), list(PROCESSED_COLUMNS))
            self.assertEqual(rows[0]["match_date"], "2020-09-18")
            self.assertEqual(rows[0]["home_team"], "Team A")
            self.assertEqual(rows[0]["target_1x2"], "H")
            assert_chronological(rows)

    def test_processing_does_not_mutate_raw_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / "single-season.csv"
            _write_raw_csv(
                raw_path,
                [["D1", "18/09/2020", "19:30", "Team A", "Team B", "2", "0", "H"]],
            )
            before_hash = _sha256(raw_path)
            before_mtime = raw_path.stat().st_mtime_ns

            rows = process_raw_file(raw_path, "2020/21")

            self.assertEqual(len(rows), 1)
            self.assertEqual(_sha256(raw_path), before_hash)
            self.assertEqual(raw_path.stat().st_mtime_ns, before_mtime)


def _write_raw_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Div", "Date", "Time", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
        writer.writerows(rows)


def _read_processed(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    unittest.main()
