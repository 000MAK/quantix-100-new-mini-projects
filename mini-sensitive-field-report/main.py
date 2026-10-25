from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def sensitive_field_report(data):
    tokens=('password','secret','token','api_key','apikey','private_key','email','phone','ssn','address','credit_card')
    matches=[]
    def walk(x,path=''):
        if isinstance(x,dict):
            for k,v in x.items():
                p=f'{path}.{k}' if path else str(k)
                if any(t in str(k).casefold() for t in tokens): matches.append(p)
                walk(v,p)
        elif isinstance(x,list):
            for i,v in enumerate(x): walk(v,f'{path}[{i}]')
    walk(data.get('value',{}))
    return {'sensitive_key_paths':sorted(set(matches)),'values_disclosed':False}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return sensitive_field_report(data)

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
