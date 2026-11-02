#!/usr/bin/env python3
"""Validate actual inventory, file integrity, author/license coverage, and pinned provenance."""
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/catalog.json').read_text())
locks={s['id']:s for s in json.loads((root/'data/sources.lock.json').read_text())['sources']}
seen=set();paths=set();counts=Counter();categories=Counter()
for asset in data['assets']:
    assert asset['id'] not in seen,asset['id'];seen.add(asset['id'])
    assert asset['path'] not in paths,asset['path'];paths.add(asset['path'])
    file=(root/asset['path']).resolve();assert file.is_relative_to(root/'assets')
    raw=file.read_bytes();assert len(raw)==asset['bytes']
    assert hashlib.sha256(raw).hexdigest()==asset['sha256'],file
    assert ET.fromstring(raw).tag.split('}')[-1]=='svg',file
    assert asset['author'] and asset['license'] and asset['license_url'] and asset['attribution']
    source=locks[asset['source']];assert asset['commit']==source['commit']
    assert asset['source_url'].startswith(source['repository']+'/blob/'+source['commit']+'/')
    assert (root/'licenses'/asset['source']).is_dir()
    if asset['source']=='reactome':assert file.with_suffix('.xml').exists()
    counts[asset['source']]+=1;categories[asset['category']]+=1
actual={f.relative_to(root).as_posix() for f in (root/'assets').rglob('*.svg')}
assert actual==paths,'Unindexed or missing SVG'
assert counts==Counter({s['id']:s['count'] for s in data['sources']})
assert categories==Counter({c['id']:c['count'] for c in data['categories']})
with (root/'data/manifest.csv').open(encoding='utf-8-sig',newline='') as fp:
    rows=list(csv.DictReader(fp));assert len(rows)==len(seen)
    assert {r['sha256'] for r in rows}=={a['sha256'] for a in data['assets']}
print(f'PASS: {len(seen)} SVGs, {len(counts)} sources; hashes, XML, licenses, provenance, counts and CSV verified')
