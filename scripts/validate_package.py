"""Validate package invariants and local links. Requires Python 3.11+."""
from pathlib import Path
import re
import struct
import tomllib
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def validate_svg(path):
    raw = path.read_text(encoding='utf-8')
    assert '<!DOCTYPE' not in raw.upper() and '<!ENTITY' not in raw.upper(), path
    root = ET.fromstring(raw)
    allowed = {'svg', 'g', 'path', 'circle', 'rect', 'polygon', 'polyline',
               'line', 'ellipse', 'title', 'desc', 'text', 'tspan'}
    for element in root.iter():
        assert element.tag.rsplit('}', 1)[-1] in allowed, path
        for name, value in element.attrib.items():
            name = name.rsplit('}', 1)[-1].lower()
            assert not name.startswith('on') and name not in {'href', 'src', 'style'}, path
            assert not re.search(r'url\s*\(|javascript:|data:', value, re.I), path


def validate():
    agent = tomllib.loads((ROOT / 'adapters/codex/democracy_archivist.toml').read_text(encoding='utf-8'))
    assert agent['name'] == 'democracy_archivist'
    assert agent['sandbox_mode'] == 'read-only'
    assert agent['description'] and agent['developer_instructions']
    claude = (ROOT / 'adapters/claude/democracy-archivist.md').read_text(encoding='utf-8')
    frontmatter = claude.split('---', 2)[1]
    assert 'name: democracy-archivist' in frontmatter
    assert 'tools: Read, Grep, Glob' in frontmatter
    assert 'model: inherit' in frontmatter
    assert 'skills:' not in frontmatter, 'Do not preload both editions'
    names = {f'self-documenting-democracy-{locale}' for locale in ('en', 'es')}
    assert {p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()} == names
    for name in names:
        folder = ROOT / 'skills' / name
        skill = (folder / 'SKILL.md').read_text(encoding='utf-8')
        assert f'name: {name}\n' in skill
        assert 'description:' in skill.split('---', 2)[1]
        metadata = (folder / 'agents/openai.yaml').read_text(encoding='utf-8')
        assert f'${name}' in metadata
        locale = name.rsplit('-', 1)[1]
        assert f'docs/super-earth/{locale}/' in skill
        assert f'docs/super-earth/{locale}/' in (folder / 'references/documentation-contract.md').read_text(encoding='utf-8')
    checked = 0
    for path in ROOT.rglob('*'):
        if '.git' in path.parts or not path.is_file():
            continue
        if path.suffix == '.svg':
            validate_svg(path)
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
            if path.is_relative_to(ROOT / 'skills'):
                bundle = ROOT / 'skills' / path.relative_to(ROOT / 'skills').parts[0]
                assert target.is_relative_to(bundle), f'Skill is not self-contained: {path}: {link}'
            checked += 1
    for name in ['democracy-recruitment.png', 'democracy-high-command.png']:
        data = (ROOT / 'assets/propaganda' / name).read_bytes()
        assert data[:8] == b'\x89PNG\r\n\x1a\n'
        width, height = struct.unpack('>II', data[16:24])
        assert width >= 1000 and height >= 600
    print(f'Package invariants valid; {checked} local links checked; 2 PNG headers validated.')


if __name__ == '__main__':
    validate()
