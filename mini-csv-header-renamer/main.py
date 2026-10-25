from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def csv_rename_headers(data):
    rows = list(csv.DictReader(io.StringIO(str(data.get('csv', '')))))
    renames = data.get('rename', {})
    old_fields = list(rows[0].keys()) if rows else []
    new_fields = [renames.get(k, k) for k in old_fields]
    if len(set(new_fields)) != len(new_fields): raise ValueError('renamed columns must be unique')
    out = io.StringIO(newline=''); writer = csv.writer(out, lineterminator='\n')
    if old_fields: writer.writerow(new_fields)
    for row in rows: writer.writerow([row[k] for k in old_fields])
    return out.getvalue()


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return csv_rename_headers(data)

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
