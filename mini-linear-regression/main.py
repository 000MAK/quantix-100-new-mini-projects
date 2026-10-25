from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def linear_regression(data):
    x=[float(v) for v in data.get('x',[])]; y=[float(v) for v in data.get('y',[])]
    if len(x)!=len(y) or len(x)<2: raise ValueError('x and y must have equal length >= 2')
    mx,my=statistics.mean(x),statistics.mean(y); den=sum((a-mx)**2 for a in x)
    if den==0: raise ValueError('x values must not all be equal')
    slope=sum((a-mx)*(b-my) for a,b in zip(x,y))/den; intercept=my-slope*mx
    ss_tot=sum((b-my)**2 for b in y); ss_res=sum((b-(slope*a+intercept))**2 for a,b in zip(x,y))
    r2=1.0 if ss_tot==0 and ss_res==0 else (0.0 if ss_tot==0 else 1-ss_res/ss_tot)
    return {'slope':round(slope,8),'intercept':round(intercept,8),'r_squared':round(r2,8)}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return linear_regression(data)

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
