from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def study_schedule(data):
    total=int(data['total_minutes']); subjects=data.get('subjects',[])
    if total<0 or not subjects: raise ValueError('total_minutes must be non-negative and subjects non-empty')
    weights=[float(s.get('weight',1)) for s in subjects]
    if any(w<0 for w in weights) or sum(weights)<=0: raise ValueError('weights must be non-negative with a positive sum')
    exact=[total*w/sum(weights) for w in weights]; base=[math.floor(x) for x in exact]; remain=total-sum(base)
    order=sorted(range(len(exact)),key=lambda i: exact[i]-base[i],reverse=True)
    for i in order[:remain]: base[i]+=1
    return [{'subject':str(s['name']),'minutes':base[i]} for i,s in enumerate(subjects)]


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return study_schedule(data)

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
