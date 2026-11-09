# Deployment and packaging

## Requirements and scope
OpenClaw with experimental Templates support (tested CLI: 2026.11.1). Host-selected model and permissions. Python 3.11+ and IANA timezone data only for optional helper/tests. No accounts or pip/npm package dependencies for the planning agents. Web research requires host-granted web tools; supplied sources remain usable without them. These packages don't provide a tool sandbox; set and test least privilege on the receiving host.

## Preview
From repository root, for each desired template:
```sh
openclaw templates validate ./templates/travel-copilot
openclaw templates dev ./templates/travel-copilot
openclaw templates inspect ./templates/travel-copilot
```
Inspect the manifest, all selected files and executable helper. Previews don't add an agent, enable jobs or connect accounts. To add, enable Settings → Labs → Templates, then deliberately run `openclaw templates add ./templates/travel-copilot`. Never run Add in CI or against a user's live workspace merely to validate a package.

## Build immutable artifacts
```sh
python3 scripts/build_packages.py --out /tmp/agent-template-build
```
Use a new output directory each time; existing artifacts are never overwritten. The script invokes OpenClaw validate/dev/build, performs two builds and compares bytes, and writes SHA256SUMS plus receipts. It does not publish or install. GitHub Actions runs standard-library tests; the OpenClaw packaging gate is separately recorded in VERIFICATION.md, not implied by green Python CI.

## Where to put private records
After Add, keep real plans in private/ inside that agent's authorized workspace. The published repository contains only blank shapes and fictional examples. Do not symlink this source repository to private folders or commit live plans. Keep separate workspaces per trusted organizer/organization. Don't admit guests or members into a session with private file access.

## Updates and deletion
New package versions don't update existing agents. Review changes and migrate records intentionally; adding again creates another ordinary agent. Agent deletion uses normal OpenClaw controls and may remove its workspace and assigned jobs; shared dependencies are managed separately. These editions declare none. Back up/export private records deliberately before any deletion; no destructive cleanup is automated here.

## Publication boundaries
This repository hosts package source. It is not an npm package feed, ClawHub listing or installed agent. For a future ClawHub submission, build an immutable .tgz, inspect exact files/digest and use the registry's authenticated human review/publish flow. Do not assume a GitHub push authorizes registry upload, integrations or scheduled work. See https://docs.openclaw.ai/cli/templates.md and https://docs.openclaw.ai/clawhub/templates.md.
