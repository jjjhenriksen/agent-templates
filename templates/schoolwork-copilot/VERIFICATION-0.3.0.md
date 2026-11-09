# 0.3.0 optional automation lane verification
Observed 2026-11-09, OpenClaw 2026.11.1 (7150cf8).

- 90 standard-library tests passed (`python3 -m unittest discover -s tests -q`). Includes 12 new refresh tests: CLI read-only/redacted failure, local refresh, changes/removal, checkpoint deduplication, missing/stale/future/regressing/naive sources, unknown deadlines, submitted filtering, authorization/path rejection, opt-out reminders, local timing and DST repeated hour.
- `python3 scripts/check_repo.py`: passed.
- `openclaw templates validate templates/schoolwork-copilot --json`: ok.
- `openclaw templates dev templates/schoolwork-copilot --json`: no blockers, offline, no mutation.
- Two fresh `openclaw templates build` outputs compared byte-identical with cmp.
- SHA-256: `54f09b646a250e2985c7335200f7743c60fb8cc8f4ed816f74a5f205ddab605f`.

Reproduce builds with distinct fresh output paths; historical 0.2.0 verification applies only to that version. Tests exercise supplied-source execution, not live LMS access. No installs/Add, credentials, live scheduler/config/account changes, sends or submissions were performed. Supported scheduling investigated via CLI help and official docs; no receiving-host schedule or delivery test was run. Durable checkpoint writes and external receipt reconciliation are host responsibilities; no exactly-once delivery claim. LMS acquisition is not implemented. Only this package and its tests changed.
