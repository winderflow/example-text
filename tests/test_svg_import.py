"""Regression cases for scientific SVG safety and original bitmap resolution."""
import contextlib
import hashlib
import io
import json
import runpy
import shutil
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_catalog
from build_catalog import check_svg

class SVGImportTests(unittest.TestCase):
    def test_editor_export_setting_is_not_an_event(self):
        check_svg(b'<svg xmlns="http://www.w3.org/2000/svg" only_selected="false"><path d="M0 0L1 1"/></svg>')

    def test_credit_anchor_and_embedded_color_profile(self):
        check_svg(b'<svg xmlns="http://www.w3.org/2000/svg"><a href="https://www.swissbiopics.org/"><path/></a><color-profile href="data:application/vnd.iccprofile;base64,AAAA"/></svg>')

    def test_active_or_external_content_is_rejected(self):
        for content in ['<svg onload="alert(1)"/>','<svg><script/></svg>','<svg><image href="missing.jpg"/></svg>','<svg><image href="https://example.org/image.png"/></svg>']:
            with self.subTest(content=content),self.assertRaises(ValueError):check_svg(content.encode(),True)

    def test_static_html_requires_review_and_does_not_allow_scripts(self):
        raw=b'<svg><foreignObject><div>Scientific label</div></foreignObject></svg>'
        with self.assertRaises(ValueError):check_svg(raw)
        check_svg(raw,True)
        with self.assertRaises(ValueError):check_svg(b'<svg><foreignObject><div onclick="x()">label</div></foreignObject></svg>',True)


class NativeBitmapImportTests(unittest.TestCase):
    """Exercise the real importer and validator with isolated source selections."""

    @staticmethod
    def png(width, height):
        def chunk(kind, content):
            return struct.pack('>I', len(content)) + kind + content + struct.pack('>I', zlib.crc32(kind + content))
        rows = (b'\0' + b'\x20\x90\x80' * width) * height
        return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b'')

    @contextlib.contextmanager
    def imported(self, cases, minimum_long_edge=600, minimum_short_edge=200):
        commit = '1' * 40
        repository = 'https://github.com/fixture/labicons'
        with tempfile.TemporaryDirectory(prefix='native-bitmap-import-') as directory:
            root = Path(directory) / 'gallery'
            upstream = Path(directory) / 'upstream' / 'cpm-labicons'
            (root / 'data/source-selections').mkdir(parents=True)
            (upstream / 'equipment/PNG').mkdir(parents=True)
            (upstream / 'LICENSE.md').write_text('Creative Commons Attribution 4.0 International')
            (upstream / 'equipment/README.md').write_text('Fixture author: https://orcid.org/0000-0002-1825-0097')
            source = dict(id='cpm-labicons', repository=repository, commit=commit)
            (root / 'data/sources.lock.json').write_text(json.dumps(dict(retrieved_at='2026-11-04', sources=[source])))
            selected = []
            originals = {}
            for name, width, height in cases:
                path = 'equipment/PNG/' + name + '.png'
                raw = self.png(width, height)
                (upstream / path).write_bytes(raw)
                originals[path] = raw
                selected.append(dict(path=path, sha256=hashlib.sha256(raw).hexdigest(), license='CC-BY-4.0', author='Fixture author', author_url='https://orcid.org/0000-0002-1825-0097', title=name, evidence_path='equipment/README.md'))
            selection = dict(commit=commit, minimum_long_edge=minimum_long_edge, minimum_short_edge=minimum_short_edge, assets=selected)
            (root / 'data/source-selections/cpm-labicons.json').write_text(json.dumps(selection))
            with mock.patch.object(build_catalog, 'ROOT', root), mock.patch.object(sys, 'argv', ['build_catalog.py', '--sources', str(upstream.parent)]), mock.patch.object(build_catalog.subprocess, 'check_output', side_effect=[commit + '\n', '']), contextlib.redirect_stdout(io.StringIO()):
                build_catalog.main()
            catalog = json.loads((root / 'data/catalog.json').read_text())
            excluded = json.loads((root / 'data/excluded.json').read_text())
            yield root, catalog, excluded, originals

    @staticmethod
    def validate(root):
        scripts = root / 'scripts'
        scripts.mkdir(exist_ok=True)
        shutil.copyfile(Path(build_catalog.__file__).with_name('validate.py'), scripts / 'validate.py')
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(str(scripts / 'validate.py'), run_name='__main__')

    def test_standard_resolution_boundaries_and_portrait_orientation(self):
        cases = [('minimum-landscape', 600, 200), ('minimum-portrait', 200, 600), ('short-long-edge', 599, 200), ('short-short-edge', 600, 199)]
        with self.imported(cases) as (root, catalog, excluded, originals):
            self.assertEqual({asset['name'] for asset in catalog['assets']}, {'minimum-landscape', 'minimum-portrait'})
            self.assertEqual(len(excluded), 2)
            self.assertTrue(any('long-edge' in item['reason'] for item in excluded))
            self.assertTrue(any('short-edge' in item['reason'] for item in excluded))
            for asset in catalog['assets']:
                self.assertEqual(asset['quality_tier'], 'native-standard')
                self.assertEqual((root / asset['path']).read_bytes(), originals[asset['original_path']], 'Accepted originals must remain byte-identical')
            self.validate(root)

    def test_hd_boundary_comes_from_native_pixels_and_preserves_author_url(self):
        with self.imported([('standard', 1599, 200), ('highres', 1600, 200)]) as (root, catalog, excluded, _):
            self.assertEqual(excluded, [])
            self.assertEqual({asset['name']: asset['quality_tier'] for asset in catalog['assets']}, {'standard': 'native-standard', 'highres': 'native-highres'})
            for asset in catalog['assets']:
                self.assertEqual(asset['author_url'], 'https://orcid.org/0000-0002-1825-0097')
                self.assertIn('Fixture author', asset['attribution'])
                self.assertIn('/' + '1' * 40 + '/equipment/README.md', asset['evidence_url'])
            self.validate(root)
            catalog['assets'][0]['quality_tier'] = 'native-highres' if catalog['assets'][0]['quality_tier'] == 'native-standard' else 'native-standard'
            (root / 'data/catalog.json').write_text(json.dumps(catalog))
            with self.assertRaises(AssertionError):
                self.validate(root)

    def test_standard_policy_cannot_omit_the_200_pixel_short_edge(self):
        with self.assertRaisesRegex(AssertionError, 'short edge|resolution policy'):
            with self.imported([('too-narrow', 600, 199)], minimum_short_edge=1):
                pass

    def test_legacy_hd_policy_still_requires_1600_native_pixels(self):
        with self.imported([('below-hd', 1599, 200), ('native-hd', 1600, 200)], minimum_long_edge=1600, minimum_short_edge=1) as (root, catalog, excluded, _):
            self.assertEqual([asset['name'] for asset in catalog['assets']], ['native-hd'])
            self.assertEqual(len(excluded), 1)
            self.assertEqual(catalog['assets'][0]['quality_tier'], 'native-highres')
            self.validate(root)

if __name__=='__main__':unittest.main()
