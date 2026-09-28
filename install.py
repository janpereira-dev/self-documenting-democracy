"""Install this package into one project without replacing existing files."""
import argparse
from pathlib import Path
import shutil
import stat


def reject_links(path):
    for candidate in (path, *path.parents):
        try:
            metadata = candidate.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(metadata.st_mode) or getattr(metadata, 'st_file_attributes', 0) & 0x400:
            raise ValueError(f'Links and junctions are not allowed: {candidate}')


def install(target, apply=False, platform='codex'):
    if platform not in {'codex', 'claude', 'both'}:
        raise ValueError('Platform must be codex, claude, or both')
    target = Path(target).absolute()
    reject_links(target)
    if not target.is_dir():
        raise ValueError('Target must be an existing project directory')
    package = Path(__file__).resolve().parent
    pairs = []
    if platform in {'codex', 'both'}:
        pairs.extend([
        (package / 'skills/helldocs',
         target / '.agents/skills/helldocs'),
        (package / 'adapters/codex/helldocs_archivist.toml',
         target / '.codex/agents/helldocs_archivist.toml'),
        ])
    if platform in {'claude', 'both'}:
        pairs.extend([
            (package / 'skills/helldocs', target / '.claude/skills/helldocs'),
            (package / 'adapters/claude/helldocs-archivist.md',
             target / '.claude/agents/helldocs-archivist.md'),
        ])
    for source, destination in pairs:
        reject_links(destination)
        if destination.exists():
            raise FileExistsError(f'Refusing to overwrite: {destination}')
        if not source.exists():
            raise FileNotFoundError(source)
    # Preflight both destinations before creating either. No global configuration edits.
    if apply:
        for source, destination in pairs:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                with source.open('rb') as reader, destination.open('xb') as writer:
                    shutil.copyfileobj(reader, writer)
    return [str(destination) for _, destination in pairs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project')
    parser.add_argument('--platform', choices=['codex', 'claude', 'both'], default='codex')
    parser.add_argument('--apply', action='store_true', help='Actually copy files; default is preview')
    args = parser.parse_args()
    try:
        destinations = install(args.project, args.apply, args.platform)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Installation stopped: {error}\n')
    print('Installed files:' if args.apply else 'Preview only. Add --apply to install:')
    print('\n'.join(destinations))
