from __future__ import annotations
import base64, binascii, calendar, collections, csv, datetime, hashlib, io, json, math, os, re, secrets, statistics, string, unicodedata, uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

def gitignore_generator(data):
    templates={'python':['__pycache__/','*.py[cod]','.venv/','venv/','.env','.pytest_cache/'],'node':['node_modules/','dist/','.env','npm-debug.log*'],'windows':['Thumbs.db','Desktop.ini','*.lnk'],'macos':['.DS_Store','.AppleDouble','._*'],'vscode':['.vscode/'],'data':['*.db','*.sqlite3','data/','logs/']}
    selected=data.get('templates', ['python','windows','macos','vscode'])
    out=[]
    for name in selected:
        if name not in templates: raise ValueError(f'unknown template: {name}')
        out += [f'# {name}'] + templates[name]
    return '\n'.join(dict.fromkeys(out))+'\n'


def process(data):
    """Run the selected local transformation."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return gitignore_generator(data)

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
