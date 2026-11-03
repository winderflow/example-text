#!/usr/bin/env python3
"""Validate actual inventory, file integrity, author/license coverage, and pinned provenance."""
import csv
import hashlib
import json
import struct
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from collect_web_images import dimensions

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/catalog.json').read_text())
locks={s['id']:s for s in json.loads((root/'data/sources.lock.json').read_text())['sources']}
assert {s['id'] for s in data['sources']}==set(locks),'Missing source catalog entry'
assert all(s.get('kind') in {'specialist','supporting'} for s in data['sources'])
seen=set();paths=set();counts=Counter();categories=Counter();png_paths=set()
for asset in data['assets']:
    assert asset['id'] not in seen,asset['id'];seen.add(asset['id'])
    assert asset['path'] not in paths,asset['path'];paths.add(asset['path'])
    file=(root/asset['path']).resolve();assert file.is_relative_to(root/'assets')
    raw=file.read_bytes();assert len(raw)==asset['bytes']
    assert hashlib.sha256(raw).hexdigest()==asset['sha256'],file
    fmt=file.suffix.lower().lstrip('.')
    if fmt=='svg':assert ET.fromstring(raw).tag.split('}')[-1]=='svg',file
    elif fmt in {'png','jpg','jpeg'}:
        w,h=dimensions(raw);assert (w,h)==(asset['pixel_width'],asset['pixel_height']);assert max(w,h)>=1600
    else:raise AssertionError('Unsupported original image format')
    assert asset['author'] and asset['license'] and asset['license_url'] and asset['attribution']
    source=locks[asset['source']];assert asset['commit']==source['commit']
    assert asset['source_url'].startswith(source['repository']+'/blob/'+source['commit']+'/')
    assert (root/'licenses'/asset['source']).is_dir()
    if asset['source']=='reactome' and asset['original_path'].startswith('icons/'):assert file.with_suffix('.xml').exists()
    if asset['source']=='openstax-anatomy':
        assert asset['commit']=='b0058a743bdd2cc08196abaaa7d5469970c0d80c'
        assert asset['license']=='CC-BY-4.0' and asset.get('evidence_url')
        assert (root/'licenses/openstax-anatomy/evidence').is_dir()
    if asset['source']=='lucide' and file.stem in {'database','triangle-alert','circle-arrow-up'}:
        assert asset['license']=='ISC AND MIT','Missing inherited Feather MIT conditions'
        assert 'Cole Bemis' in asset['author']
    if asset['source']=='electrical-symbol-library':
        assert asset['original_path'].startswith('src/symbols/'),'NC-licensed repository files must not be imported as CC0'
        assert asset['license']=='CC0-1.0'
    if asset['source']=='gissymbology':
        collection=Path(asset['original_path']).parts[1]
        assert collection in {'microzonazione','carg','fdgc','sicod'}
        assert (root/'licenses'/asset['source']/collection/'license').exists()
    if asset.get('requires_png_fallback'):assert asset.get('preview_path')==asset.get('ppt_png_path') and asset.get('ppt_png_path'),'Static HTML SVG requires rendered PPT fallback'
    if asset.get('ppt_png_path'):
        png=(root/asset['ppt_png_path']).resolve();assert png.is_relative_to(root/'assets/ppt-png')
        raw_png=png.read_bytes();assert raw_png.startswith(b'\x89PNG\r\n\x1a\n')
        width,height=struct.unpack('>II',raw_png[16:24])
        assert (width,height)==(asset['ppt_png_width'],asset['ppt_png_height'])
        assert max(width,height)==2400
        assert len(raw_png)==asset['ppt_png_bytes']
        assert hashlib.sha256(raw_png).hexdigest()==asset['ppt_png_sha256']
        png_paths.add(asset['ppt_png_path'])
    counts[asset['source']]+=1;categories[asset['category']]+=1
actual={f.relative_to(root).as_posix() for f in (root/'assets').rglob('*') if f.is_file() and f.suffix.lower() in {'.svg','.png','.jpg','.jpeg'} and not f.is_relative_to(root/'assets/ppt-png')}
assert actual==paths,'Unindexed or missing original image'
assert counts==Counter({s['id']:s['count'] for s in data['sources']})
assert categories==Counter({c['id']:c['count'] for c in data['categories']})
with (root/'data/manifest.csv').open(encoding='utf-8-sig',newline='') as fp:
    rows=list(csv.DictReader(fp));assert len(rows)==len(seen)
    assert {r['sha256'] for r in rows}=={a['sha256'] for a in data['assets']}
if png_paths:
    selection=json.loads((root/'data/ppt-selection.json').read_text());renders=json.loads((root/'data/ppt-renders.json').read_text())['renders']
    assert set(selection['asset_ids'])==set(renders)
    assert len(png_paths)==len(selection['asset_ids'])
    assert {p.relative_to(root).as_posix() for p in (root/'assets/ppt-png').rglob('*.png')}==png_paths
    for a in data['assets']:
        if a.get('ppt_png_path'):assert renders[a['id']]['source_sha256']==a['sha256']
if (root/'data/ppt-deck.json').exists():
    deck=json.loads((root/'data/ppt-deck.json').read_text());raw_deck=(root/deck['file']).read_bytes()
    assert hashlib.sha256(raw_deck).hexdigest()==deck['sha256']
    with zipfile.ZipFile(root/deck['file']) as archive:
        slidefiles=[n for n in archive.namelist() if __import__('re').fullmatch(r'ppt/slides/slide\d+\.xml',n)]
        assert len(slidefiles)==deck['slides']
        images={hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist() if n.startswith('ppt/media/')}
        assert images=={x['sha256'] for x in deck['images']}
        notes='\n'.join(archive.read(n).decode() for n in archive.namelist() if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml'))
        assert all(x['asset_id'] in seen and x['attribution'].split('Source: ')[1].split('. License:')[0].replace('&','&amp;') in notes for x in deck['images'])
assert data.get('format_counts',{})==dict(Counter(Path(a['path']).suffix.lower().lstrip('.') for a in data['assets']))
print(f'PASS: {len(seen)} original images, {len(png_paths)} PPT PNGs, {len(counts)} sources; hashes, dimensions, XML, licenses, provenance, counts and CSV verified')
