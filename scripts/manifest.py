#!/usr/bin/env python3
"""Atomically record campaign post progress (local-only manifest).

Usage: python scripts/manifest.py campaign-manifest.json SLUG STAGE '{"postId":"..."}'
"""
import json, os, sys, tempfile
from pathlib import Path

if __name__ == '__main__':
    if len(sys.argv) != 5:
        raise SystemExit('usage: manifest.py FILE SLUG STAGE JSON_FIELDS')
    filename, slug, stage, raw = sys.argv[1:]
    fields = json.loads(raw)
    path = Path(filename)
    data = json.loads(path.read_text()) if path.exists() else {'posts': {}}
    record = data.setdefault('posts', {}).setdefault(slug, {})
    record.update(fields)
    record['stage'] = stage
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=str(path.parent), prefix='.manifest-', suffix='.json')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    print(f'{slug}: {stage}')
