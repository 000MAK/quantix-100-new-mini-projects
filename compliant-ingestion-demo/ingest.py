"""Dry-run-first ingestion of explicitly authorized CSV exports.

This module intentionally does not scrape websites, discover targets, or send
messages. It validates operator-provided authorization/consent attestations,
reports aggregate counts, and optionally exports a minimal pseudonymous review
queue. It is an educational example, not a legal compliance guarantee.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import hmac
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

SOURCE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$")
LOCALE_RE = re.compile(r"^[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})?$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
REQUIRED_COLUMNS = {
    "record_id",
    "source",
    "source_authorized",
    "consent_status",
    "locale",
    "currency",
}
OUTPUT_COLUMNS = [
    "record_ref",
    "source",
    "locale",
    "currency",
    "review_status",
]


def load_config(path: Path) -> dict[str, Any]:
    """Load a YAML config and validate its minimum structure."""
    with path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict):
        raise ValueError("Config must contain a YAML mapping.")
    if not isinstance(config.get("policy"), dict):
        raise ValueError("Config must contain a policy mapping.")
    if not isinstance(config.get("output"), dict):
        raise ValueError("Config must contain an output mapping.")
    if not isinstance(config.get("input_path"), str):
        raise ValueError("Config must define input_path.")
    if not isinstance(config.get("output_path"), str):
        raise ValueError("Config must define output_path.")
    return config


def validate_row(
    row: dict[str, str],
    policy: dict[str, Any],
) -> tuple[bool, str, dict[str, str] | None]:
    """Validate a row without logging or returning any raw identifier."""
    record_id = (row.get("record_id") or "").strip()
    source = (row.get("source") or "").strip()
    authorized_values = {
        str(value).strip().casefold()
        for value in policy.get("authorized_source_values", [])
    }
    consent_values = {
        str(value).strip().casefold()
        for value in policy.get("allowed_consent_statuses", [])
    }
    source_authorized = (row.get("source_authorized") or "").strip().casefold()
    consent_status = (row.get("consent_status") or "").strip().casefold()
    locale = (row.get("locale") or "").strip()
    currency = (row.get("currency") or "").strip().upper()

    if not record_id:
        return False, "missing_record_id", None
    if source_authorized not in authorized_values:
        return False, "source_not_authorized", None
    if consent_status not in consent_values:
        return False, "consent_missing_or_not_allowed", None
    if not SOURCE_RE.fullmatch(source):
        return False, "invalid_source_label", None
    if not LOCALE_RE.fullmatch(locale):
        return False, "invalid_locale", None
    if not CURRENCY_RE.fullmatch(currency):
        return False, "invalid_currency", None

    # Only this small metadata allowlist is carried beyond validation.
    return True, "accepted", {
        "record_id": record_id,
        "source": source,
        "locale": locale.replace("_", "-"),
        "currency": currency,
    }


def pseudonymous_reference(record_id: str, key: bytes) -> str:
    """Create a keyed reference so raw IDs are not written to output."""
    return hmac.new(key, record_id.encode("utf-8"), hashlib.sha256).hexdigest()[:24]


def run(config_path: Path, apply: bool) -> int:
    config = load_config(config_path)
    base_dir = config_path.resolve().parent
    input_path = (base_dir / config["input_path"]).resolve()
    output_path = (base_dir / config["output_path"]).resolve()
    policy = config["policy"]
    max_rows = int(policy.get("max_rows", 5000))
    if max_rows < 1 or max_rows > 100000:
        raise ValueError("policy.max_rows must be between 1 and 100000.")

    if not input_path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    accepted: list[dict[str, str]] = []
    rejected: Counter[str] = Counter()
    rows_seen = 0

    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fields
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"Input is missing required columns: {missing_list}")

        for row in reader:
            rows_seen += 1
            if rows_seen > max_rows:
                raise ValueError(
                    f"Input exceeded configured row limit ({max_rows}); "
                    "nothing was written."
                )
            ok, reason, normalized = validate_row(row, policy)
            if ok and normalized is not None:
                accepted.append(normalized)
            else:
                rejected[reason] += 1

    print(f"Rows examined: {rows_seen}")
    print(f"Rows accepted for human review: {len(accepted)}")
    print(f"Rows rejected: {sum(rejected.values())}")
    for reason, count in sorted(rejected.items()):
        print(f"  {reason}: {count}")

    if not apply:
        print("DRY RUN: no output file was written. Pass --apply to export.")
        return 0

    key_text = os.environ.get("INGEST_PSEUDONYM_KEY", "")
    if len(key_text.encode("utf-8")) < 32:
        print(
            "Refusing to write: set INGEST_PSEUDONYM_KEY to a local secret "
            "of at least 32 bytes. Do not commit it.",
            file=sys.stderr,
        )
        return 2

    output_path.parent.mkdir(parents=True, exist_ok=True)
    review_status = str(
        config.get("output", {}).get("review_status", "needs_human_review")
    )
    key = key_text.encode("utf-8")

    # De-duplicate pseudonymous records before writing a minimal review queue.
    output_rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in accepted:
        record_ref = pseudonymous_reference(item["record_id"], key)
        if record_ref in seen:
            continue
        seen.add(record_ref)
        output_rows.append(
            {
                "record_ref": record_ref,
                "source": item["source"],
                "locale": item["locale"],
                "currency": item["currency"],
                "review_status": review_status,
            }
        )

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Minimal review queue written: {output_path}")
    print(f"Exported pseudonymous records: {len(output_rows)}")
    print("No messages were sent and no external website was contacted.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an authorized CSV export; dry-run unless --apply is set."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("config.example.yaml"),
        help="YAML configuration file (default: config.example.yaml).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the minimal pseudonymous review queue. Default is dry-run.",
    )
    args = parser.parse_args()
    try:
        return run(args.config, args.apply)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
