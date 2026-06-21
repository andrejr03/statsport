#!/usr/bin/env python3
"""Build StatSport Logistic Regression explainability artifacts."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.statsport.baseline import load_feature_rows
from src.statsport.explainability import (
    global_csv_fieldnames,
    global_influence_markdown,
    limitations_markdown,
    load_coefficients,
    model_behaviour_summary_markdown,
    prediction_card_markdown,
    rank_global_features,
    select_explanation_examples,
    training_feature_stats,
)


FEATURE_DATA_PATH = REPO_ROOT / "data" / "processed" / "bundesliga_2020_2025_features.csv"
REPORT_DIR = REPO_ROOT / "outputs" / "reports"
COEFFICIENTS_PATH = REPORT_DIR / "logistic_regression_coefficients.csv"
COMPARISON_SUMMARY_PATH = REPORT_DIR / "model_comparison_summary.md"

GLOBAL_INFLUENCE_CSV_PATH = REPORT_DIR / "global_feature_influence.csv"
GLOBAL_INFLUENCE_MD_PATH = REPORT_DIR / "global_feature_influence.md"
MODEL_BEHAVIOUR_SUMMARY_PATH = REPORT_DIR / "model_behaviour_summary.md"
LIMITATIONS_PATH = REPORT_DIR / "limitations_and_uncertainty.md"
PREDICTION_CARD_PATHS = tuple(
    REPORT_DIR / f"prediction_explanation_card_{index}.md"
    for index in range(1, 4)
)


def main() -> int:
    rows = load_feature_rows(FEATURE_DATA_PATH)
    coefficients = load_coefficients(COEFFICIENTS_PATH)
    rankings = rank_global_features(coefficients)
    stats = training_feature_stats(rows)
    examples = select_explanation_examples(rows, coefficients, stats)
    comparison_summary = COMPARISON_SUMMARY_PATH.read_text(encoding="utf-8")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _write_global_influence_csv(GLOBAL_INFLUENCE_CSV_PATH, rankings)
    GLOBAL_INFLUENCE_MD_PATH.write_text(
        global_influence_markdown(rankings),
        encoding="utf-8",
    )
    MODEL_BEHAVIOUR_SUMMARY_PATH.write_text(
        model_behaviour_summary_markdown(rankings, comparison_summary),
        encoding="utf-8",
    )
    LIMITATIONS_PATH.write_text(limitations_markdown(), encoding="utf-8")
    for index, (path, example) in enumerate(zip(PREDICTION_CARD_PATHS, examples), start=1):
        path.write_text(prediction_card_markdown(example, index), encoding="utf-8")

    print(
        json.dumps(
            {
                "global_feature_influence_csv": str(
                    GLOBAL_INFLUENCE_CSV_PATH.relative_to(REPO_ROOT)
                ),
                "global_feature_influence_md": str(
                    GLOBAL_INFLUENCE_MD_PATH.relative_to(REPO_ROOT)
                ),
                "model_behaviour_summary": str(
                    MODEL_BEHAVIOUR_SUMMARY_PATH.relative_to(REPO_ROOT)
                ),
                "limitations": str(LIMITATIONS_PATH.relative_to(REPO_ROOT)),
                "prediction_cards": [
                    str(path.relative_to(REPO_ROOT)) for path in PREDICTION_CARD_PATHS
                ],
                "selected_examples": [
                    {
                        "category": example.category,
                        "match_date": example.row["match_date"],
                        "home_team": example.row["home_team"],
                        "away_team": example.row["away_team"],
                        "predicted": example.predicted_class,
                        "actual": example.actual_class,
                        "confidence": f"{example.confidence:.12f}",
                    }
                    for example in examples
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _write_global_influence_csv(path: Path, rankings: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=global_csv_fieldnames())
        writer.writeheader()
        writer.writerows(rankings)


if __name__ == "__main__":
    raise SystemExit(main())
