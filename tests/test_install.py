import importlib.util
from pathlib import Path
import shutil
import uuid
import unittest

SCRIPT = Path(__file__).parents[1] / 'install.py'
SPEC = importlib.util.spec_from_file_location('installer', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InstallTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parent
        self.root = parent / ('fixture-' + uuid.uuid4().hex)
        self.root.mkdir()
        self.addCleanup(self.clean_fixture, parent)

    def clean_fixture(self, parent):
        assert self.root.resolve().parent == parent
        assert not self.root.is_symlink()
        shutil.rmtree(self.root)

    def test_preview_does_not_write(self):
        self.assertEqual(len(MODULE.install(self.root)), 2)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_install_preserves_unrelated_content(self):
        original = self.root / 'README.md'
        original.write_text('Existing work')
        MODULE.install(self.root, apply=True)
        self.assertEqual(original.read_text(), 'Existing work')
        self.assertTrue((self.root / '.agents/skills/helldocs/SKILL.md').is_file())
        self.assertTrue((self.root / '.codex/agents/helldocs_archivist.toml').is_file())

    def test_conflict_stops_before_partial_install(self):
        existing = self.root / '.codex/agents/helldocs_archivist.toml'
        existing.parent.mkdir(parents=True)
        existing.write_text('Existing agent')
        with self.assertRaises(FileExistsError):
            MODULE.install(self.root, apply=True)
        self.assertFalse((self.root / '.agents').exists())
        self.assertEqual(existing.read_text(), 'Existing agent')

    def test_claude_only(self):
        MODULE.install(self.root, apply=True, platform='claude')
        self.assertTrue((self.root / '.claude/skills/helldocs/SKILL.md').is_file())
        self.assertTrue((self.root / '.claude/agents/helldocs-archivist.md').is_file())
        self.assertFalse((self.root / '.codex').exists())
        self.assertFalse((self.root / '.agents').exists())

    def test_both_platforms_share_identical_skill(self):
        self.assertEqual(len(MODULE.install(self.root, apply=True, platform='both')), 4)
        codex = self.root / '.agents/skills/helldocs/SKILL.md'
        claude = self.root / '.claude/skills/helldocs/SKILL.md'
        self.assertEqual(codex.read_bytes(), claude.read_bytes())

    def test_claude_conflict_prevents_all_writes(self):
        existing = self.root / '.claude/agents/helldocs-archivist.md'
        existing.parent.mkdir(parents=True)
        existing.write_text('Existing agent')
        with self.assertRaises(FileExistsError):
            MODULE.install(self.root, apply=True, platform='both')
        self.assertFalse((self.root / '.agents').exists())
        self.assertFalse((self.root / '.codex').exists())
        self.assertFalse((self.root / '.claude/skills').exists())

    def test_unknown_platform_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.install(self.root, apply=True, platform='unknown')
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
