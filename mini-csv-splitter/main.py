from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def csv_split(data):
    raw = str(data.get('csv', '')); chunk_size = int(data.get('rows_per_part', 100))
    if chunk_size < 1: raise ValueError('rows_per_part must be positive')
    reader = csv.DictReader(io.StringIO(raw)); rows = list(reader); fields = reader.fieldnames or []
    parts = []
    for i in range(0, len(rows), chunk_size):
        out = io.StringIO(newline=''); writer = csv.DictWriter(out, fieldnames=fields, lineterminator='\n'); writer.writeheader(); writer.writerows(rows[i:i+chunk_size]); parts.append(out.getvalue())
    if not parts and fields: parts = [','.join(fields)+'\n']
    return {'parts': parts, 'part_count': len(parts), 'rows': len(rows)}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return csv_split(data)

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
