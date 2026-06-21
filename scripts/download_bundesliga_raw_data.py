#!/usr/bin/env python3
"""Download the approved Football-Data.co.uk Bundesliga raw CSV files."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"

RAW_DATA_FILES = [
    (
        "2020/21",
        "https://www.football-data.co.uk/mmz4281/2021/D1.csv",
        "football-data-co-uk_bundesliga_2020-2021.csv",
    ),
    (
        "2021/22",
        "https://www.football-data.co.uk/mmz4281/2122/D1.csv",
        "football-data-co-uk_bundesliga_2021-2022.csv",
    ),
    (
        "2022/23",
        "https://www.football-data.co.uk/mmz4281/2223/D1.csv",
        "football-data-co-uk_bundesliga_2022-2023.csv",
    ),
    (
        "2023/24",
        "https://www.football-data.co.uk/mmz4281/2324/D1.csv",
        "football-data-co-uk_bundesliga_2023-2024.csv",
    ),
    (
        "2024/25",
        "https://www.football-data.co.uk/mmz4281/2425/D1.csv",
        "football-data-co-uk_bundesliga_2024-2025.csv",
    ),
]


def download_file(url: str, output_path: Path) -> int:
    with urlopen(url, timeout=30) as response:
        data = response.read()
    output_path.write_bytes(data)
    return len(data)


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for season, url, filename in RAW_DATA_FILES:
        output_path = RAW_DIR / filename
        try:
            byte_count = download_file(url, output_path)
        except URLError as exc:
            raise RuntimeError(f"Failed to download {season} from {url}") from exc
        results.append(
            {
                "season": season,
                "source_url": url,
                "output_path": str(output_path.relative_to(REPO_ROOT)),
                "bytes": byte_count,
            }
        )

    print(json.dumps({"downloaded_files": results}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
