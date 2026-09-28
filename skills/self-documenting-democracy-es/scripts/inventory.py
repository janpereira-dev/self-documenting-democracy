"""Metadata-only project inventory. Never follows links or reads file contents."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import stat


PRUNED = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist',
          'build', 'coverage', '.next', '.cache', 'vendor'}
PRIVATE_DIRS = {'.ssh', '.aws', '.azure', '.kube', 'secrets', 'credentials',
                'profiles', 'dumps', 'backups'}
PRIVATE_SUFFIXES = {'.pem', '.key', '.pfx', '.p12', '.keystore', '.sqlite',
                    '.sqlite3', '.db', '.dump', '.log', '.har'}
BINARY_SUFFIXES = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.pdf',
                   '.zip', '.gz', '.7z', '.exe', '.dll', '.woff', '.woff2',
                   '.mp4', '.mp3', '.glb', '.bin'}


def is_link(st):
    return stat.S_ISLNK(st.st_mode) or bool(
        getattr(st, 'st_file_attributes', 0) & 0x400)


def inventory(root, max_bytes=1_000_000):
    root = Path(os.path.abspath(root))
    for ancestor in (root, *root.parents):
        if is_link(ancestor.lstat()):
            raise ValueError('Root and ancestors must not be links or junctions')
    if not root.is_dir():
        raise ValueError('Root must be a directory')
    entries = []

    def walk(directory):
        try:
            with os.scandir(directory) as scan:
                children = sorted(scan, key=lambda item: item.name.casefold())
        except OSError as error:
            entries.append({'path': directory.relative_to(root).as_posix(),
                            'kind': 'directory', 'status': 'blocked',
                            'reason': type(error).__name__})
            return
        for item in children:
            path = Path(item.path)
            relative = path.relative_to(root).as_posix()
            row = {'path': relative, 'kind': 'unknown', 'status': 'pending',
                   'reason': 'metadata_only_not_read'}
            try:
                st = item.stat(follow_symlinks=False)
                if is_link(st):
                    row.update(kind='link', status='excluded', reason='link_or_reparse_point')
                elif stat.S_ISDIR(st.st_mode):
                    name = item.name.lower()
                    reason = ('private_directory' if name in PRIVATE_DIRS else
                              'generated_or_vendor' if name in PRUNED else
                              'documentation_output' if relative == 'docs/super-earth' else None)
                    if reason:
                        row.update(kind='directory', status='excluded', reason=reason)
                    else:
                        walk(path)
                        continue
                elif stat.S_ISREG(st.st_mode):
                    name = item.name.lower()
                    suffix = path.suffix.lower()
                    private = (name.startswith('.env') or name in {'.npmrc', '.pypirc',
                               'id_rsa', 'id_ed25519', '.netrc'} or
                               any(word in name for word in ('secret', 'credential', 'token')) or
                               suffix in PRIVATE_SUFFIXES)
                    row.update(kind='file', size=st.st_size, mtime_ns=st.st_mtime_ns)
                    if private:
                        row.update(status='excluded', reason='potentially_sensitive')
                    elif suffix in BINARY_SUFFIXES:
                        row.update(status='excluded', reason='binary_asset')
                    elif st.st_size > max_bytes:
                        row.update(status='blocked', reason='large_file_requires_chunked_review')
                else:
                    row.update(kind='special', status='excluded', reason='special_file')
            except OSError as error:
                row.update(status='blocked', reason=type(error).__name__)
            entries.append(row)
    walk(root)
    return {'schema_version': 1, 'mode': 'metadata_only',
            'scope': str(root), 'entries': entries,
            'counts': dict(Counter(row['status'] for row in entries)),
            'limitations': ['Excluded directory contents are not enumerated.',
                            'Filename rules do not guarantee secret detection.',
                            'Inventory does not establish reading or documentation coverage.',
                            'Filesystem can change during or after inventory.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root')
    parser.add_argument('--max-bytes', type=int, default=1_000_000)
    args = parser.parse_args()
    if args.max_bytes < 1:
        parser.error('--max-bytes must be positive')
    try:
        result = inventory(args.root, args.max_bytes)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Inventory failed: {error}\n')
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
