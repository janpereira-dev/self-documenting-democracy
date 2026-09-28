import importlib.util
from pathlib import Path
import shutil
import uuid
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / 'skills/self-documenting-democracy-en/scripts/inventory.py'
SPEC = importlib.util.spec_from_file_location('inventory', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parent
        self.root = parent / ('fixture-' + uuid.uuid4().hex)
        self.root.mkdir()
        self.addCleanup(self.clean_fixture, parent)

    def clean_fixture(self, parent):
        assert self.root.resolve().parent == parent
        assert not self.root.is_symlink()
        shutil.rmtree(self.root)

    def create(self, relative, content='example'):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    def rows(self, **kwargs):
        return {row['path']: row for row in MODULE.inventory(self.root, **kwargs)['entries']}

    def test_files_are_pending_not_read(self):
        self.create('src/main.ts')
        self.assertEqual(self.rows()['src/main.ts']['status'], 'pending')

    def test_private_and_generated_directories_are_not_entered(self):
        self.create('secrets/nested/password.txt')
        self.create('node_modules/pkg/index.js')
        rows = self.rows()
        self.assertEqual(set(rows), {'secrets', 'node_modules'})
        self.assertTrue(all(row['status'] == 'excluded' for row in rows.values()))

    def test_sensitive_files_are_excluded_without_reading(self):
        for name in ['.env', '.env.example', 'access-token.json', 'private.pem', 'local.db']:
            self.create(name, 'DO_NOT_READ')
        with patch.object(Path, 'read_text', side_effect=AssertionError('Content was read')):
            rows = self.rows()
        self.assertTrue(all(row['status'] == 'excluded' for row in rows.values()))

    def test_large_files_are_blocked_not_silently_skipped(self):
        self.create('large.txt', '12345')
        self.assertEqual(self.rows(max_bytes=4)['large.txt']['status'], 'blocked')

    def test_documentation_output_does_not_recurse(self):
        self.create('docs/super-earth/README.md')
        self.create('docs/architecture.md')
        rows = self.rows()
        self.assertEqual(rows['docs/super-earth']['status'], 'excluded')
        self.assertIn('docs/architecture.md', rows)

    def test_permission_error_is_explicit(self):
        original = MODULE.os.scandir
        self.create('restricted/file.txt')
        def scan(path):
            if Path(path).name == 'restricted':
                raise PermissionError('denied')
            return original(path)
        with patch.object(MODULE.os, 'scandir', side_effect=scan):
            self.assertEqual(self.rows()['restricted']['status'], 'blocked')

    def test_reparse_detection(self):
        class Metadata:
            st_mode = 0
            st_file_attributes = 0x400
        self.assertTrue(MODULE.is_link(Metadata()))

    def test_empty_inventory_does_not_claim_coverage(self):
        result = MODULE.inventory(self.root)
        self.assertEqual(result['entries'], [])
        self.assertNotIn('coverage', result)

    def test_unicode_path_is_preserved(self):
        self.create('módulo/diseño.md')
        self.assertIn('módulo/diseño.md', self.rows())


if __name__ == '__main__':
    unittest.main()
