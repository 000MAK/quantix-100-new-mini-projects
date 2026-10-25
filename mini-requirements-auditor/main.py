from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def requirements_audit(data):
    names=[]; unpinned=[]
    for line in str(data.get('text','')).splitlines():
        s=line.strip()
        if not s or s.startswith(('#','-','http://','https://')): continue
        m=re.match(r'^([A-Za-z0-9_.-]+)',s)
        if not m: continue
        name=re.sub(r'[-_.]+','-',m.group(1)).casefold(); names.append(name)
        if not re.search(r'==|~=|>=|<=|!=|===',s): unpinned.append(name)
    counts=collections.Counter(names)
    return {'duplicates':sorted(k for k,v in counts.items() if v>1),'unpinned':sorted(set(unpinned)),'packages_seen':len(names)}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return requirements_audit(data)

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
