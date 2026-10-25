from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def zscore_outliers(data):
    xs=[float(x) for x in data.get('values',[])]; threshold=float(data.get('threshold',2.0))
    if len(xs)<2 or threshold<=0: raise ValueError('at least two values and positive threshold required')
    mean=statistics.mean(xs); sd=statistics.pstdev(xs)
    out=[] if sd==0 else [{'index':i,'value':x,'z_score':round((x-mean)/sd,4)} for i,x in enumerate(xs) if abs((x-mean)/sd)>threshold]
    return {'mean':mean,'population_stddev':sd,'outliers':out}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return zscore_outliers(data)

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
