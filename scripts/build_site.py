#!/usr/bin/env python3
"""Build a bounded Pages artifact while retaining original files in GitHub.

Only the built catalog receives delivery URLs. Repository assets and the source
catalog remain unchanged; the current commit pins every external file version.
"""
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote, urlsplit


LOCAL_IMAGE_LIMIT = 128 * 1024
MAX_SITE_BYTES = 700 * 1024 * 1024
IMAGE_EXTENSIONS = {'.svg', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.tif', '.tiff', '.bmp', '.avif'}


def github_delivery_base(root):
    """Read only the repository identity, never include remote credentials."""
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()

    try:
        remote = git('remote', 'get-url', 'origin')
        commit = git('rev-parse', 'HEAD')
    except subprocess.CalledProcessError as error:
        raise RuntimeError('A GitHub origin and committed HEAD are required to build the site.') from error
    if remote.startswith('git@github.com:'):
        repository = remote[len('git@github.com:'):]
    else:
        parsed = urlsplit(remote)
        if parsed.hostname != 'github.com' or parsed.scheme not in {'https', 'ssh'} or parsed.query or parsed.fragment:
            raise RuntimeError('The site delivery origin must be a GitHub repository.')
        repository = parsed.path.lstrip('/')
    if repository.endswith('.git'):
        repository = repository[:-4]
    parts = repository.split('/')
    if (len(parts) != 2 or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*', parts[0])
            or not re.fullmatch(r'[A-Za-z0-9_.-]+', parts[1]) or parts[1] in {'.', '..'}
            or not re.fullmatch(r'[0-9a-f]{40}', commit)):
        raise RuntimeError('The GitHub repository identity or commit is invalid.')
    return f'https://raw.githubusercontent.com/{repository}/{commit}/'


def rewrite_document_links(filename, root, external_paths, base_url):
    """Keep copied Markdown/HTML links usable when their images leave dist."""
    references = {}
    for asset_path in external_paths:
        relative = Path(os.path.relpath(root / asset_path, filename.parent)).as_posix()
        url = base_url + quote(asset_path, safe='/')
        references[relative] = url
        references[quote(relative, safe='/')] = url
        # JavaScript encodeURIComponent leaves these punctuation characters intact.
        references[quote(relative, safe="/!~*'()")] = url
    if not references:
        return
    # Exact destinations also handle parentheses in filenames and ?raw=true.
    destinations = '|'.join(re.escape(value) for value in sorted(references, key=len, reverse=True))
    pattern = re.compile(r'(?P<prefix>\]\(|(?:href|src)=["\'])(?P<path>' + destinations + r')(?=[?#)"\'\s>]|$)')
    original = filename.read_text(encoding='utf-8')
    rewritten = pattern.sub(lambda match: match['prefix'] + references[match['path']], original)
    if rewritten != original:
        filename.write_text(rewritten, encoding='utf-8')


def build_site(root, dest):
    root, dest = Path(root).resolve(), Path(dest).resolve()
    if dest == root or root.is_relative_to(dest):
        raise ValueError('The output directory must not contain the source repository.')
    base_url = github_delivery_base(root)
    modified = subprocess.run(['git', '-C', str(root), 'diff', '--quiet', 'HEAD', '--', 'assets']).returncode
    untracked = subprocess.check_output(['git', '-C', str(root), 'ls-files', '--others', '--exclude-standard', '--', 'assets'], text=True)
    if modified != 0 or untracked.strip():
        raise RuntimeError('Commit image additions and changes before building commit-pinned GitHub delivery URLs.')
    external_paths = sorted(
        path.relative_to(root).as_posix()
        for path in (root / 'assets').rglob('*')
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS and path.stat().st_size > LOCAL_IMAGE_LIMIT
    )
    omitted = set(external_paths)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for name in ['index.html', 'app.js', 'styles.css', '.nojekyll', 'README.md', 'LICENSE']:
        shutil.copyfile(root / name, dest / name)
    for name in ['assets', 'data', 'licenses', 'docs']:
        def ignore(directory, names):
            return [name for name in names if (Path(directory) / name).relative_to(root).as_posix() in omitted]
        shutil.copytree(root / name, dest / name, ignore=ignore if name == 'assets' else None)
    if (root / 'downloads').is_dir():
        shutil.copytree(root / 'downloads', dest / 'downloads')
    catalog_file = dest / 'data' / 'catalog.json'
    catalog = json.loads(catalog_file.read_text(encoding='utf-8'))
    catalog['delivery'] = {'base_url': base_url, 'external_paths': external_paths}
    catalog_file.write_text(json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    for filename in [dest / 'README.md', *(dest / 'docs').rglob('*.md')]:
        rewrite_document_links(filename, dest, external_paths, base_url)
    total = sum(path.stat().st_size for path in dest.rglob('*') if path.is_file())
    if total > MAX_SITE_BYTES:
        raise RuntimeError(f'Static site is {total / 1024 ** 2:.1f} MiB, above the 700 MiB build limit.')
    print(f'Static site prepared in {dest.name}/: {total / 1024 ** 2:.1f} MiB; '
          f'{len(external_paths):,} larger images use commit-pinned GitHub originals.')
    return {'bytes': total, 'external_count': len(external_paths), 'base_url': base_url}


if __name__ == '__main__':
    repository_root = Path(__file__).resolve().parents[1]
    build_site(repository_root, repository_root / 'dist')
