#!/usr/bin/env python3
"""Create minimal Pages artifact; Python standard library only."""
import shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1];dest=root/'dist'
if dest.exists():shutil.rmtree(dest)
dest.mkdir()
for name in ['index.html','app.js','styles.css','.nojekyll','README.md','LICENSE']:
    shutil.copyfile(root/name,dest/name)
for name in ['assets','data','licenses','docs']:
    shutil.copytree(root/name,dest/name)
if (root/'downloads').is_dir():shutil.copytree(root/'downloads',dest/'downloads')
print('Static site prepared in dist/')
