from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def habit_streak(data):
    dates=sorted({datetime.date.fromisoformat(x) for x in data.get('dates',[])})
    best=cur=0; prev=None
    for d in dates:
        cur=cur+1 if prev and d==prev+datetime.timedelta(days=1) else 1
        best=max(best,cur); prev=d
    as_of=datetime.date.fromisoformat(data['as_of']) if data.get('as_of') else (dates[-1] if dates else None)
    current=0
    if as_of:
        ds=set(dates); d=as_of
        while d in ds: current+=1; d-=datetime.timedelta(days=1)
    return {'longest_streak':best,'current_streak_as_of_date':current,'unique_days':len(dates)}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return habit_streak(data)

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
