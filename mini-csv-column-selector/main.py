from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def csv_select_columns(data):
    rows = list(csv.DictReader(io.StringIO(str(data.get('csv', '')))))
    cols = list(data.get('columns', []))
    if rows and any(c not in rows[0] for c in cols): raise ValueError('one or more columns not found')
    out = io.StringIO(newline=''); writer = csv.DictWriter(out, fieldnames=cols, lineterminator='\n')
    if cols: writer.writeheader()
    writer.writerows({c:r.get(c,'') for c in cols} for r in rows)
    return {'csv': out.getvalue(), 'rows': len(rows), 'columns': cols}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return csv_select_columns(data)

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
