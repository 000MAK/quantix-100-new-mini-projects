from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def password_strength(data):
    p=str(data.get('password','')); classes=sum(bool(re.search(pat,p)) for pat in (r'[a-z]',r'[A-Z]',r'\d',r'[^A-Za-z0-9]'))
    alphabet=sum(n for n,pat in ((26,r'[a-z]'),(26,r'[A-Z]'),(10,r'\d'),(32,r'[^A-Za-z0-9]')) if re.search(pat,p))
    entropy=round(len(p)*math.log2(max(alphabet,1)),1)
    score=0 if len(p)<8 else min(4, (1 if len(p)>=12 else 0)+(1 if len(p)>=16 else 0)+(1 if classes>=3 else 0)+(1 if classes==4 else 0))
    return {'length':len(p),'character_classes':classes,'estimated_entropy_bits':entropy,'score_0_to_4':score,'note':'Heuristic only; not a breach check.'}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return password_strength(data)

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
