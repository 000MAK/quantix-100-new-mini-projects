from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def csv_sanitize_formulas(data):
    rows = list(csv.reader(io.StringIO(str(data.get('csv', '')))))
    out = io.StringIO(newline=''); writer = csv.writer(out, lineterminator='\n')
    changed = 0
    for row in rows:
        safe = []
        for cell in row:
            if cell.lstrip().startswith(('=', '+', '-', '@')):
                cell = "'" + cell; changed += 1
            safe.append(cell)
        writer.writerow(safe)
    return {'csv': out.getvalue(), 'cells_neutralized': changed}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return csv_sanitize_formulas(data)

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
