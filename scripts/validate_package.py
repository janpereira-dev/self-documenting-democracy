"""Validate package invariants and local links. Requires Python 3.11+."""
from pathlib import Path
import re
import struct
import tomllib
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def validate():
    agent = tomllib.loads((ROOT / 'adapters/codex/helldocs_archivist.toml').read_text(encoding='utf-8'))
    assert agent['name'] == 'helldocs_archivist'
    assert agent['sandbox_mode'] == 'read-only'
    assert agent['description'] and agent['developer_instructions']
    claude = (ROOT / 'adapters/claude/helldocs-archivist.md').read_text(encoding='utf-8')
    frontmatter = claude.split('---', 2)[1]
    assert 'name: helldocs-archivist' in frontmatter
    assert 'tools: Read, Grep, Glob' in frontmatter
    assert 'model: inherit' in frontmatter
    assert '  - helldocs' in frontmatter
    skill = (ROOT / 'skills/helldocs/SKILL.md').read_text(encoding='utf-8')
    assert 'name: helldocs\n' in skill
    assert 'description:' in skill.split('---', 2)[1]
    checked = 0
    for path in ROOT.rglob('*'):
        if '.git' in path.parts or not path.is_file():
            continue
        if path.suffix == '.svg':
            ET.parse(path)
        if path.suffix not in {'.md', '.html'}:
            continue
        text = path.read_text(encoding='utf-8')
        links = re.findall(r'\]\(([^)]+)\)', text)
        links += re.findall(r'(?:src|href)="([^"]+)"', text)
        for link in links:
            if '://' in link or link.startswith('#'):
                continue
            target = (path.parent / link.split('#')[0]).resolve()
            assert target.is_relative_to(ROOT), f'Link escapes package: {path}: {link}'
            assert target.exists(), f'Broken link: {path}: {link}'
            checked += 1
    for name in ['helldocs-recruitment.png', 'high-command.png']:
        data = (ROOT / 'assets/propaganda' / name).read_bytes()
        assert data[:8] == b'\x89PNG\r\n\x1a\n'
        width, height = struct.unpack('>II', data[16:24])
        assert width >= 1000 and height >= 600
    print(f'Package invariants valid; {checked} local links checked; 2 PNG headers validated.')


if __name__ == '__main__':
    validate()
