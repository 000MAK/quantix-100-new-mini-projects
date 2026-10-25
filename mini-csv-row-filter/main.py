from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def csv_filter_rows(data):
    rows = list(csv.DictReader(io.StringIO(str(data.get('csv', '')))))
    col, op, wanted = str(data.get('column', '')), str(data.get('operator', 'eq')), str(data.get('value', ''))
    if rows and col not in rows[0]: raise ValueError('column not found')
    def keep(row):
        got = row.get(col, '')
        if op == 'eq': return got == wanted
        if op == 'contains': return wanted.casefold() in got.casefold()
        try: a, b = float(got), float(wanted)
        except ValueError: return False
        if op == 'gt': return a > b
        if op == 'lt': return a < b
        if op == 'gte': return a >= b
        if op == 'lte': return a <= b
        raise ValueError('unsupported operator')
    out = io.StringIO(newline=''); writer = csv.DictWriter(out, fieldnames=list(rows[0]) if rows else [], lineterminator='\n')
    if rows: writer.writeheader()
    writer.writerows(r for r in rows if keep(r))
    return {'csv': out.getvalue(), 'rows_kept': sum(1 for r in rows if keep(r))}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return csv_filter_rows(data)

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
