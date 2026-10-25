from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def csv_quality_report(data):
    rows = list(csv.reader(io.StringIO(str(data.get('csv', '')))))
    if not rows: return {'rows': 0, 'columns': 0, 'blank_cells': 0, 'duplicate_rows': 0}
    body = rows[1:]
    return {'rows': len(body), 'columns': len(rows[0]), 'blank_cells': sum(c.strip()=='' for row in body for c in row), 'duplicate_rows': len(body)-len({tuple(r) for r in body})}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return csv_quality_report(data)

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
