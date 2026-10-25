from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def microtask_estimate(data):
    tasks=data.get('tasks',[]); minutes=sum(float(t['minutes']) for t in tasks); rate=float(data.get('hourly_rate',30))
    if any(float(t['minutes'])<0 for t in tasks) or rate<0: raise ValueError('minutes and rate must be non-negative')
    return {'task_count':len(tasks),'total_minutes':round(minutes,2),'total_hours':round(minutes/60,2),'estimated_value':round(minutes*rate/60,2),'rate_used':rate}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return microtask_estimate(data)

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
