# Current-format release verification — 2026-11-10

## Why 0.3.1 cannot be added
ClawHub's deployed consumer (`templateRoutes-DIP48itg.js`, inspected on this date) explicitly rejects `packages`, `profiles`, `extensions`, and `cronJobs`. It requires portable dependencies as `skills`/`plugins` and jobs as `automations`. The installed OpenClaw 2026.11.1 CLI and ClawHub 0.25.1 CLI still validate the old shape. OpenClaw's online Template docs also describe the old dependencies/profile contract. Therefore a clean registry scan plus those old local checks was insufficient evidence of Add compatibility.

## Sources and scope
- `releases/celebration-coordinator`: current 0.3.2 source; six published skill requirements, `openclaw-christmas-themes@0.1.0`, Instacart Developer Platform MCP.
- `templates/meal-planner`: everyday meal planning, no holiday or event dependencies, Instacart MCP and optional offline shopping helper.
- `templates/celebration-coordinator`: preserved 0.3.0 bundled review edition with its original tests. Not the current registry projection.

Instacart uses official production endpoint with a pinned third-party `mcp-remote@0.16.5` stdio adapter, an unresolved API-key reference, and a two-tool allowlist. No credentials, accounts, live connections, shopping pages or checkout were used to test these packages. No host config or installed agents changed.

## Repeatable checks
- `python3 -m unittest discover -s tests -v`
- `python3 scripts/check_repo.py`
- `python3 scripts/build_current_packages.py --out <new-output-directory>` checks asset coverage, path confinement and byte-identical rebuilds. Archives contain the exact current-format CLAW.md, not an old-format compatibility projection.
- Validate source and archive CLAW.md with the deployed ClawHub parser's exported parser (the `o` export of the observed bundle). Old 0.3.1 returns null; both new manifests return a non-null parsed manifest. The live bundle imports are fetched read-only without modifying installed tools.

## Unverified boundaries
Parsing is not a successful end-to-end Add. Receiving-host setup, executable trust/capability consent, MCP authentication, live tool schemas, theme rendering and conversation quality require separate host tests. Instacart needs an operator-provided Developer Platform key. The old authoring/publishing CLI rejects the new valid keys, so it cannot substantiate current-contract Add or release readiness. Never reconvert the published manifest to the old shape to get a green local check. Publication/registry visibility and artifact digest must be verified separately and receipts retained before retries.

Kroger's official API site was reached but its full JS-rendered contract and any official Kroger-owned MCP were not verified. Instacart's official MCP tutorial explicitly documents recipe/list page tools and API-key authentication; its separate OAuth deployment has representative-managed access.

## Recorded results
152 Python tests passed; repository hygiene, local links and Python/JSON syntax passed. Both current-format archives rebuilt byte-identically. Deployed consumer parser rejects 0.3.1 and accepts both replacement manifests. Live Add, MCP and theme-rendering tests remain unrun.
