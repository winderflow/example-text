#!/usr/bin/env python3
"""Fetch exact public upstream revisions from sources.lock.json. Never executes upstream code."""
import argparse
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--dest',type=Path,default=ROOT/'.cache/sources');p.add_argument('--only',nargs='+',help='Optional source IDs to fetch; omission fetches all locked sources');args=p.parse_args()
    args.dest.mkdir(parents=True,exist_ok=True)
    sources=json.loads((ROOT/'data/sources.lock.json').read_text())['sources']
    if args.only and set(args.only)-{s['id'] for s in sources}:raise SystemExit('Unknown source ID in --only')
    for source in sources:
        if args.only and source['id'] not in args.only:continue
        directory=args.dest/source['id'];repository=source['repository']+'.git';commit=source['commit']
        if directory.exists():
            actual=subprocess.check_output(['git','-C',str(directory),'rev-parse','HEAD'],text=True).strip()
            if actual!=commit:raise SystemExit(f'Refusing to overwrite existing checkout {directory}; expected {commit}')
        else:
            directory.mkdir();subprocess.run(['git','init',str(directory)],check=True)
            subprocess.run(['git','-C',str(directory),'remote','add','origin',repository],check=True)
            fetch=['git','-C',str(directory),'fetch','--depth','1']
            if source.get('sparse_paths'):
                subprocess.run(['git','-C',str(directory),'sparse-checkout','set','--cone',*source['sparse_paths']],check=True)
                fetch+=['--filter=blob:none']
            subprocess.run(fetch+['origin',commit],check=True)
            subprocess.run(['git','-C',str(directory),'checkout','--detach','FETCH_HEAD'],check=True)
        print(source['id'],commit,flush=True)

if __name__=='__main__':main()
