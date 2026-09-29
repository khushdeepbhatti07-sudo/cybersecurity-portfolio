# Khushdeep Bhatti
### Cybersecurity & Information Assurance · University of Michigan–Dearborn

A focused collection of defensive security tools and systems labs, with an emphasis on C++, local monitoring, and practical investigation.

[LinkedIn](https://www.linkedin.com/in/khushdeep-bhatti/) · [GitHub](https://github.com/khushdeepbhatti07-sudo)

## Projects

| Project | What it demonstrates | Status |
| --- | --- | --- |
| [C++ Security Log Analyzer](security-log-analyzer/) | Parse authentication events, aggregate failures, flag suspicious repetition | Runnable tool + synthetic sample |
| [File Integrity Monitor](file-integrity-monitor/) | SHA-256 snapshots, SQLite event history, structured JSON output | Runnable Python prototype + tests |
| [Windows & Linux Security Baseline Lab](security-baseline-lab/) | Workstation hardening, verification, and remediation documentation | Lab guide; VM evidence pending |

## Try a project

From the repository root, with Python 3.9+:

```bash
mkdir demo-files
python3 -c "from pathlib import Path; Path('demo-files/example.txt').write_text('original')"
python3 file-integrity-monitor/fim.py init demo-files --database demo.sqlite
python3 -c "from pathlib import Path; Path('demo-files/example.txt').write_text('modified')"
python3 file-integrity-monitor/fim.py check demo-files --database demo.sqlite
```

The last command reports `MODIFIED` and exits with status `1` to signal a detected change. Use a fresh database path when repeating the demo. On Windows, use `py -3` in place of `python3`.

## Verify the tools

Requires Python 3.9+ and a C++17 compiler available as `g++`:

```bash
python3 -m unittest discover -s tests -v
```

Tests exercise file change detection, baseline preservation, invalid inputs, CLI exit codes, and the compiled analyzer against synthetic authentication events.

## How to explore this portfolio

Each project explains its purpose, how to run it, and where its detection stops. See [project discussion notes](docs/project-discussion.md) for the design decisions and questions to practice before an interview.

## Development and scope

This portfolio includes AI-assisted implementation and documentation. Runnable code is distinct from hands-on lab evidence: the baseline lab remains a guide until its verification record is completed. These educational prototypes are not production security products. Use only local files and logs you own or have permission to analyze; never commit real authentication logs, secrets, or private baseline databases.
