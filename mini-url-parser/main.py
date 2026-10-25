from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def url_parse(data):
    p=urlsplit(str(data.get('url','')))
    if p.scheme not in ('http','https') or not p.hostname: raise ValueError('only absolute HTTP/HTTPS URLs are accepted')
    try: port=p.port
    except ValueError as e: raise ValueError('invalid port') from e
    return {'scheme':p.scheme,'host':p.hostname,'port':port,'path':p.path or '/','query_present':bool(p.query),'fragment_present':bool(p.fragment),'credentials_discarded':bool(p.username or p.password)}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return url_parse(data)

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
