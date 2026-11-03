"""Regression cases for the scientific SVGs previously rejected by broad checks."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
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

if __name__=='__main__':unittest.main()
