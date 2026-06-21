#!/usr/bin/env python3
"""Build leakage-safe core features for the StatSport Bundesliga dataset."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.statsport.feature_engineering import ROLLING_WINDOW_MATCHES, build_feature_dataset


PROCESSED_PATH = REPO_ROOT / "data" / "processed" / "bundesliga_2020_2025_matches_processed.csv"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "bundesliga_2020_2025_features.csv"


def main() -> int:
    summary = build_feature_dataset(PROCESSED_PATH, OUTPUT_PATH)
    print(
        json.dumps(
            {
                "output_path": str(summary.output_path.relative_to(REPO_ROOT)),
                "total_rows": summary.total_rows,
                "season_row_counts": summary.season_row_counts,
                "feature_columns": list(summary.feature_columns),
                "rolling_window_matches": ROLLING_WINDOW_MATCHES,
                "missingness": summary.missingness,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

