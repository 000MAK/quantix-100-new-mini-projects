from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def pomodoro_plan(data):
    sessions=int(data.get('sessions',4)); work=int(data.get('work_minutes',25)); br=int(data.get('break_minutes',5)); longbr=int(data.get('long_break_minutes',15))
    if sessions<1 or sessions>50 or min(work,br,longbr)<0: raise ValueError('invalid session settings')
    t=0; blocks=[]
    for i in range(1,sessions+1):
        blocks.append({'type':'work','session':i,'start_minute':t,'end_minute':t+work}); t+=work
        if i<sessions:
            pause=longbr if i%4==0 else br
            blocks.append({'type':'break','after_session':i,'start_minute':t,'end_minute':t+pause}); t+=pause
    return {'blocks':blocks,'total_minutes':t}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return pomodoro_plan(data)

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
