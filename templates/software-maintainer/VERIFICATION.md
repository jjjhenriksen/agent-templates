# Verification — 2026-11-09

OpenClaw CLI 2026.11.1 (7150cf8), source based on main 04c523f, including this package patch.

- `python3 -m unittest discover -s tests -v`: 78 tests passed.
- `python3 scripts/check_repo.py`: hygiene, local links, syntax and asset coverage passed.
- `openclaw templates validate templates/software-maintainer --json`: passed.
- `openclaw templates dev templates/software-maintainer --json`: offline preview passed; no blockers.
- Two `openclaw templates build templates/software-maintainer --out <fresh artifact> --json` runs: byte-identical via `cmp`.
- Built artifact SHA-256: `505c3b6b0fab21f265638521ce41f5be6eee463ac22f6cbb371402c604bba92b`.

No Add/install, registry upload, live integration, scheduler change, receiving-host isolation test or conversation-level evaluation was performed. Manual scenarios in ACCEPTANCE.md remain unexecuted. Full repository build script was not used because Travel Copilot's documented optional-provider preflight is a separate gate; only this new dependency-free package was built here.
