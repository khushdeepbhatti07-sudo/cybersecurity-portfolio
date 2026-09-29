# File Integrity Monitor

A small defensive Python CLI that compares a local folder against a trusted SHA-256 baseline. Useful for learning how configuration drift and unexpected file changes are detected.

## What it does

- Hashes file contents in 1 MiB chunks rather than loading entire files into memory.
- Reports `ADDED`, `MODIFIED`, and `DELETED` paths in deterministic JSON output.
- Stores the original baseline and timestamped check events in SQLite.
- Preserves the baseline between checks so changes remain visible until explicitly re-baselined to a new database.
- Rejects symlinks, a database inside the monitored folder, and a baseline belonging to a different folder.
- Aborts on unreadable files or detected changes during hashing rather than recording an incomplete scan.

No third-party packages, administrator privileges, network access, or file-content storage. Requires Python 3.9+.

## Quick demo

Run the four demo commands in the [main README](../README.md#try-a-project), preceded by its `mkdir` command. To inspect persisted events:

```bash
python3 -c "import sqlite3; db=sqlite3.connect('demo.sqlite'); print(db.execute('SELECT observed, kind, path FROM events').fetchall()); db.close()"
```

Example check output after editing the demonstration file:

```json
{
  "baseline_files": 1,
  "scanned_files": 1,
  "events": [
    {"kind": "MODIFIED", "path": "example.txt"}
  ]
}
```

## Interface

```text
python3 file-integrity-monitor/fim.py init <folder> --database <new-database>
python3 file-integrity-monitor/fim.py check <folder> --database <existing-database>
```

| Exit status | Meaning |
| --- | --- |
| 0 | Baseline created or no content changes detected |
| 1 | Changes detected |
| 2 | Invalid input, scan failure, or database error |

## Design and limits

The `baseline` table maps relative paths to SHA-256 digests. The `metadata` table binds the snapshot to its absolute root. The `events` table records observation time, change type, and relative path, not the underlying content. Hashing is linear in total file bytes; path records are held in memory.

This is an on-demand snapshot checker, not a real-time watcher or malware classifier. A legitimate edit generates the same change signal as a malicious edit. Permissions-only changes and empty directory changes are not tracked. Renames appear as a deletion plus an addition. Each check logs all current differences from the original baseline, so repeated checks can repeat events. Deleted-and-restored files between scans are invisible.

A live directory is not an atomic filesystem snapshot. Keep the test directory idle while scanning; the modification check cannot eliminate every race. Do not use concurrent initialization or checks against the same database. Protect the baseline separately: anyone who can alter it can undermine comparison. To accept a new trusted state, investigate changes first and initialize a new database path. The tool never repairs or deletes monitored files.

## Next learning steps

Add a periodic watcher, then event retention and permission-change tracking. These are future work, not implemented features.
