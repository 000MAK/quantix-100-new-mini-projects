"""Run the full 20-model benchmark with public online datasets."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from online_research_models import BIKE_SOURCE, WINE_SOURCE, load_bike_sharing, load_wine_quality, run_online_models
from online_model_extensions import run_additional_models

def run_all_online_models(wine=None, bike_hour=None, bike_day=None, seed: int = 42) -> dict[str, Any]:
    if wine is None:
        wine = load_wine_quality()
    if bike_hour is None or bike_day is None:
        loaded_hour, loaded_day = load_bike_sharing()
        bike_hour = bike_hour if bike_hour is not None else loaded_hour
        bike_day = bike_day if bike_day is not None else loaded_day
    first_ten = run_online_models(wine=wine, bike_hour=bike_hour, bike_day=bike_day, seed=seed)["results"]
    second_ten = run_additional_models(wine=wine, bike_hour=bike_hour, seed=seed)
    results = first_ten + second_ten
    if len(results) != 20 or len({row["model"] for row in results}) != 20:
        raise RuntimeError(f"Expected twenty uniquely named model experiments, got {len(results)}.")
    return {
        "title": "Quantix: 20 Statistical and Machine-Learning Models on Online Data",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": [
            {"name": WINE_SOURCE, "url": "https://archive.ics.uci.edu/dataset/186/wine+quality", "license": "CC BY 4.0"},
            {"name": BIKE_SOURCE, "url": "https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset", "license": "CC BY 4.0"},
        ],
        "model_count": 20,
        "results": results,
        "interpretation": "Metrics come from the documented holdout schemes for these public datasets. They are educational benchmarks, not insurance pricing, medical, regulatory, or investment advice.",
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="", help="Optional JSON report output path.")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    report = run_all_online_models(seed=args.seed)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        destination = Path(args.output).expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
