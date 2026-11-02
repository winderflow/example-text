#!/usr/bin/env python3
"""Fetch exact public upstream revisions from sources.lock.json. Never executes upstream code."""
import argparse
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--dest',type=Path,default=ROOT/'.cache/sources');args=p.parse_args()
    args.dest.mkdir(parents=True,exist_ok=True)
    for source in json.loads((ROOT/'data/sources.lock.json').read_text())['sources']:
        directory=args.dest/source['id'];repository=source['repository']+'.git';commit=source['commit']
        if directory.exists():
            actual=subprocess.check_output(['git','-C',str(directory),'rev-parse','HEAD'],text=True).strip()
            if actual!=commit:raise SystemExit(f'Refusing to overwrite existing checkout {directory}; expected {commit}')
        else:
            directory.mkdir();subprocess.run(['git','init',str(directory)],check=True)
            subprocess.run(['git','-C',str(directory),'remote','add','origin',repository],check=True)
            subprocess.run(['git','-C',str(directory),'fetch','--depth','1','origin',commit],check=True)
            subprocess.run(['git','-C',str(directory),'checkout','--detach','FETCH_HEAD'],check=True)
        print(source['id'],commit,flush=True)

if __name__=='__main__':main()
