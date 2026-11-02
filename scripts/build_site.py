#!/usr/bin/env python3
"""Create minimal Pages artifact; Python standard library only."""
import shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1];dest=root/'dist'
if dest.exists():shutil.rmtree(dest)
dest.mkdir()
for name in ['index.html','app.js','styles.css','.nojekyll']:
    shutil.copyfile(root/name,dest/name)
for name in ['assets','data','licenses','docs']:
    shutil.copytree(root/name,dest/name)
print('Static site prepared in dist/')
