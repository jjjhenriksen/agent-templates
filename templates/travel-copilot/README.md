# Travel Copilot

Feasible travel plans with source checks, access details, and room to change your mind.

**Status: 0.2.0 provider-research edition.** Includes an agent prompt, first-run onboarding, operating instructions, workflow, voice examples, data contract, blank record, fictional worked example, offline helper and acceptance checklist. Declares pinned Expedia plugin and goplaces skill dependencies. Accounts, the Google CLI/API setup, credentials and execution restrictions require separate operator setup. No scheduled jobs or transactions.

## Try it safely
From repository root:
```sh
python3 templates/travel-copilot/workspace/scripts/plan.py templates/travel-copilot/workspace/examples/example.json
openclaw templates validate ./templates/travel-copilot
openclaw templates dev ./templates/travel-copilot
```
These checks do not install an agent. To add one, enable Templates in Settings → Labs, inspect first, then deliberately run:
```sh
openclaw templates inspect ./templates/travel-copilot
openclaw templates add ./templates/travel-copilot
```
Add creates a new ordinary agent; adding again creates another. Templates do not auto-update existing agents. The receiving host controls tools, model, secrets and access. Review [deployment](../../docs/DEPLOYMENT.md) first.

## First conversation
> Do you have somewhere in mind, or are we choosing? Tell me where you’re starting, roughly when, and the budget you want me to work within.

Or: “Use the fictional example and show me what you do.” Never confuse demo output with a live plan.

## What you get
Read [workflow](workspace/reference/workflow.md), [voice examples](workspace/reference/voice.md), [data contract](workspace/reference/data-contract.md), [optional integrations](workspace/reference/integrations.md), and [acceptance scenarios](ACCEPTANCE.md). The agent maintains private records for you; JSON editing is not onboarding homework.

Helper commands print a private report by default. `--share` prints only explicitly allowlisted public_summary values after exact field approval; review before sharing. No authentication or ACL is provided. Do not accept member/guest queries inside the organizer's private session.

## Limits
The helper validates record shape and computes a bounded report; it doesn't verify real-world facts or constrain the host agent's permissions. Expedia may send authentication emails only after exact current confirmation. Searches require configured provider access; no successful live-provider test is claimed. No booking, provider contact, calendar sync, secure multi-user access or unattended work is implemented. [Test evidence](../../docs/VERIFICATION.md) distinguishes automated checks from unrun conversation/host tests.

## Provider research
See [provider workflow](workspace/reference/provider-research.md) and
[Google setup/boundaries](workspace/reference/goplaces.md). Expedia results are a
single-provider view, not market-wide inventory. Google lookups may incur API
charges and disclose submitted locations. Missing setup degrades to supplied-source
planning with explicit gaps; it never triggers installation or billing changes.
The native profile adds shell execution: workspace-only file settings do not
sandbox it. Review and enforce host permissions before Add.

This adapts the Travel Concierge research work from OpenClaw Awesome Templates;
see [third-party notices](workspace/reference/provider-notices.md). Unlike that package, this edition
keeps the existing v1 record and offline helper, uses Markdown rather than a
second JSON schema/dashboard, and declares no automatic daily refresh.
