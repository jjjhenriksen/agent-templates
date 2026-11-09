# 0.2.0 verification
Observed 2026-11-09 using OpenClaw 2026.11.1 (7150cf8) and standard-library Python tests.

- `python3 -m unittest discover -s tests -v`: 78 tests in 0.571s; passed.
- `python3 scripts/check_repo.py`: passed asset coverage, local links, syntax and hygiene checks.
- `openclaw templates validate ./templates/schoolwork-copilot --json`: ok.
- `openclaw templates dev ./templates/schoolwork-copilot --json`: offline preview, no blockers, mutation disallowed.
- Two `openclaw templates build ./templates/schoolwork-copilot --out <fresh-output.tgz> --json` runs: byte-identical.
- Artifact SHA-256: `e7081161f94a3ebd3b5a24e7745ef8ca275da925b7d2ca58efd6eb2df5b21578`.

Reproduce from this branch with two distinct fresh output paths and compare bytes (`cmp first.tgz second.tgz`). Package-root verification notes/tests are not mapped runtime assets, so they do not change the artifact digest. No Add, account connection, provider send, registry upload, scheduler mutation or deployment occurred.

Static tests validate packaging, not conversational compliance. Fictional worked cases and acceptance scenarios require a receiving-model pilot. Host security, real consent, policy authority, food/access conditions and external integrations were not live-tested. Existing offline helpers are unchanged; no runtime engine is added. This is a workflow/resource release, not an automation implementation.
