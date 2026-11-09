# Verification — 2026-11-09

## Executed
- **51 automated tests passed** on Python 3.14.7: decimal budget math, double-count prevention, unknown costs, input rejection, dependency cycles, public projection, opt-in/roles/skills/availability/workload/overlap, timezone-aware intervals, read-only CLI and repository hygiene.
- Repository scan passed: JSON/Python syntax, relative Markdown links, explicit workspace-asset coverage, required package files and private-path/token-pattern checks. This is bounded hygiene, not an exhaustive security audit.
- **3/3 packages** passed OpenClaw 2026.11.1 `templates validate` and offline `templates dev`. No Add or config mutation.
- **3/3 packages** built twice with identical bytes/digests. See SHA256SUMS-0.1.0.txt. Artifacts contain 20/21/20 files respectively, only mapped generic files, metadata, bootstrap and license. No symlinks, escaping paths, bytecode or detected private-path/token markers.
- **3/3 final archives** extracted into isolated temporary directories; OpenClaw inspection plus private/share example helper commands passed from each extracted package. No source-tree imports required.
- Voice instructions and fictional conversation examples reviewed for distinct natural tone, minimal questioning, no sales copy or fabricated personal experience. This is source review, not a behavioral pass rate.

## Required receiving-host/pilot checks not claimed
- Conversation-level acceptance across real model turns; examples alone do not establish runtime quality.
- Fresh agent Add, host file/tool isolation, participant identity enforcement, private multi-user access.
- Live calendar/email/reminder integration, transaction safety, scheduler/delivery execution.
- Real-world food safety, access certification, policy compliance, qualification or entry/visa clearance.

Acceptance checklists in each package identify these remaining gates. Upstream Good Company tests are not template tests. GitHub CI separately runs Python 3.11/3.12/3.13 tests; consult the actual workflow run rather than inferring its status from this local receipt.

## Schoolwork Copilot addition — 2026-11-09
- 64 local automated tests passed on Python 3.14.7 (51 existing, 13 new). New coverage: timezone ordering, unknown deadlines, input validation, read-only CLI, no record mutation, private-note exclusion and bounded anonymization markers.
- Repository hygiene and whitespace checks passed.
- Schoolwork Copilot 0.1.0 passed OpenClaw 2026.11.1 validate, offline dev, and two byte-identical builds. Archive checked for symlinks, escaping paths and bounded personal/institution markers. Public repository attribution and copyright remain; no private school identity or records are bundled.
- SHA256: `02898e273132b1571432103c0f51b5968c5b223f1c6fa7f3f187ae42efe87bfb`. Existing release artifacts/digests were not changed.
- No Add, account connection, scheduler mutation, assignment submission or ClawHub publication. Conversational acceptance and receiving-host security remain untested.

## Travel Copilot 0.2.0 provider-research revision — 2026-11-09
- 76 offline Python tests passed (64 existing, 12 new). New checks pin dependency/profile declarations, reject version/tool/profile/job drift and cover workspace mapping, attribution and required safety/fallback instructions. These are source/contract checks, not model behavior or provider execution tests.
- Repository hygiene and whitespace checks passed. Existing offline helper and v1 record behavior are unchanged.
- OpenClaw 2026.11.1 `templates validate` passed. Two non-installing `templates build` runs produced byte-identical archives. Packaged notice, profile and all mapped workspace files were inspected; no account, job or agent was created.
- `templates dev` returned a plan but is **blocked** on `package_install_unavailable` for the goplaces skill and Expedia extension because dependency preflight is unavailable in offline preview. The full `scripts/build_packages.py` gate therefore cannot be called passed for this revision. Build success does not establish dependency installation or receiving-host readiness.
- No successful live-provider test is claimed. Prior Google probes were denied by Places permission and disabled Routes API; credentials and payloads are not included. Expedia authentication/search, Google search/details/directions, receiving-host execution restrictions and conversational acceptance still need authorized live checks.
- No Add, installation, API/billing/configuration change, scheduled refresh, booking, provider contact or registry publication was performed.
