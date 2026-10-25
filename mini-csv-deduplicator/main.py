from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def csv_dedupe(data):
    rows = list(csv.DictReader(io.StringIO(str(data.get('csv', '')))))
    keys = data.get('key_columns') or (list(rows[0].keys()) if rows else [])
    seen, kept = set(), []
    for row in rows:
        key = tuple(row.get(k, '') for k in keys)
        if key not in seen: seen.add(key); kept.append(row)
    out = io.StringIO(newline=''); writer = csv.DictWriter(out, fieldnames=list(rows[0]) if rows else [], lineterminator='\n')
    if rows: writer.writeheader()
    writer.writerows(kept)
    return {'csv': out.getvalue(), 'removed': len(rows)-len(kept), 'rows_kept': len(kept)}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return csv_dedupe(data)

def cli():
    import sys
    try:
        if len(sys.argv) > 2:
            raise ValueError("usage: python main.py [input.json]")
        if len(sys.argv) == 2:
            with open(sys.argv[1], "r", encoding="utf-8") as stream:
                payload = json.load(stream)
        else:
            payload = json.load(sys.stdin)
        result = process(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)

if __name__ == "__main__":
    cli()
