from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def secret_redactor(data):
    text=str(data.get('text',''))
    patterns=[r'(?i)(api[_-]?key\s*[:=]\s*)[^\s,;]+',r'(?i)(token\s*[:=]\s*)[^\s,;]+',r'(?i)(password\s*[:=]\s*)[^\s,;]+',r'(?i)(secret\s*[:=]\s*)[^\s,;]+',r'(?i)(authorization\s*:\s*bearer\s+)[A-Za-z0-9._~+/-]+=*']
    for pat in patterns: text=re.sub(pat,lambda m:m.group(1)+'[REDACTED]',text)
    return text


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return secret_redactor(data)

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
