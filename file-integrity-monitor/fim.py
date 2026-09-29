"""Local SHA-256 snapshots. Stores metadata and hashes, never file contents."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
from datetime import datetime, timezone


def snapshot(root):
    records = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlinks are not supported: {path}')
        if not path.is_file():
            continue
        before = path.stat()
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        after = path.stat()
        if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
            raise ValueError(f'File changed during scan; retry: {path}')
        records[path.relative_to(root).as_posix()] = digest.hexdigest()
    return records


def run(root, database, initialize=False):
    root = root.resolve(strict=True)
    database = database.resolve()
    if not root.is_dir():
        raise ValueError('Root must be a directory.')
    if database == root or root in database.parents:
        raise ValueError('Keep the database outside the monitored directory.')
    if initialize and database.exists():
        raise ValueError('Database already exists; choose a new path to preserve the baseline.')
    if not initialize and not database.is_file():
        raise ValueError('Baseline missing; run init first.')
    current = snapshot(root)  # Complete scan before any database writes.
    stamp = datetime.now(timezone.utc).isoformat()
    if initialize:
        with sqlite3.connect(database) as db:
            db.execute('CREATE TABLE metadata (root TEXT NOT NULL, created TEXT NOT NULL)')
            db.execute('CREATE TABLE baseline (path TEXT PRIMARY KEY, sha256 TEXT NOT NULL)')
            db.execute('CREATE TABLE events (observed TEXT, kind TEXT, path TEXT)')
            db.execute('INSERT INTO metadata VALUES (?, ?)', (str(root), stamp))
            db.executemany('INSERT INTO baseline VALUES (?, ?)', current.items())
        return {'baseline_files': len(current), 'events': []}
    with sqlite3.connect(database) as db:
        if db.execute('SELECT root FROM metadata').fetchone()[0] != str(root):
            raise ValueError('This baseline belongs to a different directory.')
        baseline = dict(db.execute('SELECT path, sha256 FROM baseline'))
        events = []
        for path in sorted(current.keys() | baseline.keys()):
            kind = ('ADDED' if path not in baseline else
                    'DELETED' if path not in current else
                    'MODIFIED' if current[path] != baseline[path] else None)
            if kind:
                events.append({'kind': kind, 'path': path})
        db.executemany('INSERT INTO events VALUES (?, ?, ?)',
                       [(stamp, event['kind'], event['path']) for event in events])
    return {'baseline_files': len(baseline), 'scanned_files': len(current), 'events': events}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'check'])
    parser.add_argument('root', type=Path)
    parser.add_argument('--database', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run(args.root, args.database, args.command == 'init')
    except (OSError, ValueError, sqlite3.Error) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result['events'] else 0


if __name__ == '__main__':
    sys.exit(main())
