"""Structural regressions, not proof of agent behavior or a general SVG sanitizer."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate_package.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SecurityTests(unittest.TestCase):
    def test_svg_rejects_active_or_external_content(self):
        for payload in (
            '<script>alert(1)</script>',
            '<image href="https://example.invalid/track"/>',
            '<foreignObject/>',
            '<path onclick="alert(1)"/>',
            '<path fill="url(https://example.invalid/track)"/>',
            '<animate attributeName="href"/>',
        ):
            with self.subTest(payload=payload):
                path = Mock()
                path.read_text.return_value = '<svg>' + payload + '</svg>'
                with self.assertRaises(AssertionError):
                    validator.validate_svg(path)

    def test_bundled_insignia_pass_static_allowlist(self):
        for path in (ROOT / 'skills').rglob('*.svg'):
            validator.validate_svg(path)

    def test_ci_does_not_pass_credentials_to_package_installers(self):
        workflow = (ROOT / '.github/workflows/validate.yml').read_text()
        self.assertIn('persist-credentials: false', workflow)
        self.assertNotIn('GH_TOKEN:', workflow)
        self.assertNotIn('npx ', workflow)
        self.assertNotIn('pull_request_target', workflow)


if __name__ == '__main__':
    unittest.main()
