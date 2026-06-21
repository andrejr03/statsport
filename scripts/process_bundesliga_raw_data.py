#!/usr/bin/env python3
"""Build the StatSport processed Bundesliga match dataset."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.statsport.data_processing import process_all_raw_files


RAW_DIR = REPO_ROOT / "data" / "raw"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "bundesliga_2020_2025_matches_processed.csv"


def main() -> int:
    summary = process_all_raw_files(RAW_DIR, OUTPUT_PATH)
    print(
        json.dumps(
            {
                "output_path": str(summary.output_path.relative_to(REPO_ROOT)),
                "total_rows": summary.total_rows,
                "season_row_counts": summary.season_row_counts,
                "target_distribution": summary.target_distribution,
                "missingness": summary.missingness,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

