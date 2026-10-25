from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def invoice_text(data):
    invoice=str(data.get('invoice_number','DRAFT')); client=str(data.get('client','Client')); currency=str(data.get('currency','USD'))
    lines=[f'# Invoice {invoice}',f'Client: {client}','', '| Item | Qty | Unit price | Total |','|---|---:|---:|---:|']; total=0.0
    for item in data.get('items',[]):
        qty=float(item['quantity']); price=float(item['unit_price'])
        if qty<0 or price<0: raise ValueError('quantity and price must be non-negative')
        sub=qty*price; total+=sub; lines.append(f"| {item['description']} | {qty:g} | {price:.2f} {currency} | {sub:.2f} {currency} |")
    lines += ['',f'**Total due: {total:.2f} {currency}**','', 'Draft only; verify tax and legal requirements before use.']
    return {'markdown':'\n'.join(lines),'total':round(total,2),'currency':currency}


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return invoice_text(data)

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
