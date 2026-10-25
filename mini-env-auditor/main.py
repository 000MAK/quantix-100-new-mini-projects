from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def env_audit(data):
    keys=[]; suspicious=[]; duplicates=[]; seen=set()
    for line in str(data.get('text','')).splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        s=re.sub(r'^export\s+','',s)
        if '=' not in s: continue
        key,val=s.split('=',1); key=key.strip()
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',key): continue
        if key in seen: duplicates.append(key)
        seen.add(key); keys.append(key)
        if val.strip().strip('"\'') and re.search(r'(SECRET|TOKEN|PASSWORD|API_KEY|PRIVATE_KEY|CREDENTIAL)',key,re.I): suspicious.append(key)
    return {'keys':sorted(set(keys)),'duplicate_keys':sorted(set(duplicates)),'review_secret_like_values_by_key_only':sorted(set(suspicious)),'values_disclosed':False}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return env_audit(data)

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
