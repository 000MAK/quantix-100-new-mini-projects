from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def net_hourly_rate(data):
    amount=float(data['amount']); costs=sum(float(data.get(k,0)) for k in ('fee','api_cost','reserve')); minutes=float(data['minutes'])
    if minutes<=0: raise ValueError('minutes must be positive')
    if costs<0: raise ValueError('costs must be non-negative')
    net=amount-costs
    return {'estimated_direct_net':round(net,2),'net_hourly_rate':round(net*60/minutes,2),'note':'Estimate after listed direct costs; taxes and fixed overhead excluded.'}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return net_hourly_rate(data)

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
