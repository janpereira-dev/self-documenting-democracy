from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / 'skills/self-documenting-democracy-en'
ES = ROOT / 'skills/self-documenting-democracy-es'


class EditionTests(unittest.TestCase):
    def test_bundles_have_matching_resources(self):
        def resources(folder):
            return {p.relative_to(folder) for p in folder.rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts}
        self.assertEqual(resources(EN), resources(ES))

    def test_optional_inventory_helpers_are_identical(self):
        self.assertEqual((EN / 'scripts/inventory.py').read_bytes(),
                         (ES / 'scripts/inventory.py').read_bytes())

    def test_sources_remain_equivalent(self):
        def links(folder):
            text = (folder / 'references/sources.md').read_text(encoding='utf-8')
            return set(re.findall(r'\]\((https://[^)]+)\)', text))
        self.assertEqual(links(EN), links(ES))

    def test_coverage_states_remain_equivalent(self):
        for folder in (EN, ES):
            contract = (folder / 'references/documentation-contract.md').read_text(encoding='utf-8')
            for state in ('observed', 'inferred', 'unknown', 'contradicted',
                          'pending', 'read', 'partial', 'excluded', 'blocked'):
                self.assertIn(f'`{state}`', contract)

    def test_default_destinations_do_not_collide(self):
        for folder, locale, other in ((EN, 'en', 'es'), (ES, 'es', 'en')):
            contract = (folder / 'references/documentation-contract.md').read_text(encoding='utf-8')
            self.assertIn(f'`docs/super-earth/{locale}/`', contract)
            self.assertNotIn(f'`docs/super-earth/{other}/`', contract)


if __name__ == '__main__':
    unittest.main()
