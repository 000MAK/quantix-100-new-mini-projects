from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def validate_config_types(data):
    value=data.get('config',{}); schema=data.get('required_types',{})
    mapping={'str':str,'string':str,'int':int,'integer':int,'float':float,'number':(int,float),'bool':bool,'boolean':bool,'list':list,'dict':dict,'object':dict}
    errors=[]
    for key,kind in schema.items():
        if key not in value: errors.append({'key':key,'error':'missing'}); continue
        t=mapping.get(str(kind).casefold())
        if t is None: errors.append({'key':key,'error':'unknown expected type'}); continue
        ok=isinstance(value[key],t) and not (t is int and isinstance(value[key],bool))
        if not ok: errors.append({'key':key,'error':'wrong type','expected':kind,'actual':type(value[key]).__name__})
    return {'valid':not errors,'errors':errors}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return validate_config_types(data)

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
