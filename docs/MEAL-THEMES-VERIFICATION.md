# Meal and theme release verification — 2026-11-10

## Observed compatibility split
ClawHub's deployed page parser (templateRoutes-DIP48itg.js) rejects CLAW.md packages/cronJobs and accepts skills/plugins. The current publisher API and CLI 0.25.1 reject skills/plugins. The installed OpenClaw 2026.11.1 CLI accepts the old format. Both rejected publish requests returned HTTP 400 with no accepted attempt; receipts were retained. No accepted version was overwritten. A clean scan alone did not establish Add compatibility for 0.3.1.

## Compatible source
Celebration 0.3.2 bundles the six locked hosting/gift skills as ordinary mapped workspace files, omits the conflicting dependency/job fields, declares the pinned Christmas Themes plugin through documented profiles/openclaw.yml, and declares Instacart MCP. Everyday Meal Planner has no holiday or skill dependency and the same Instacart MCP. Empty job declarations are omitted; neither package creates automations.

This uses the native-profile mechanism documented in https://docs.openclaw.ai/clawhub/templates and https://docs.openclaw.ai/cli/templates . The live page parser can read the exact CLAW.md, and the old host/publisher can inspect the conventional profile. It does not silently convert an accepted published archive. The older bundled review edition remains reproducible at templates/celebration-coordinator.

## Checks
Run python3 -m unittest discover -s tests -v and python3 scripts/check_repo.py. Build immutable, byte-reproducible archives with python3 scripts/build_current_packages.py --out a-new-directory. Current source projects must also pass installed OpenClaw validate, dev and non-installing add preview. Validate source and exact archive CLAW.md with the deployed page parser. Record actual outcomes separately from manual scenarios.

## Boundaries
No live Add, MCP authentication/tool discovery, grocery page creation, theme rendering, or model/host pilot was performed. Instacart requires an operator-supplied Developer Platform API key. The declared bridge is third-party mcp-remote 0.16.5, not Instacart-authored, and restricts tools to create-recipe/create-shopping-list. It creates external pages, not guaranteed carts, orders or delivery. Secrets remain unresolved references; no account or host configuration changed. Kroger's full API contracts and any official Kroger-owned MCP were not verified. Registry visibility and digest require separate receipts.

## Recorded checks
152 tests passed; repository hygiene and whitespace checks passed. Both source projects validate with the installed CLI and both CLAW.md files pass the deployed page parser. Exact archive publisher dry-runs pass. Meal Planner Add preview has zero blockers (one MCP capability escalation). Celebration Add preview reaches dependency planning but is blocked on this host because Christmas Themes is not in the plugin allowlist; no policy was changed. Its offline dev preview cannot preflight that registry extension. These are not manifest syntax failures or evidence of a live Add. Both archives rebuild byte-identically.
