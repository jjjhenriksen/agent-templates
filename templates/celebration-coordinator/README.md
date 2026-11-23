# Celebration Coordinator

Plan dinners, parties, potlucks and gifts with practical hosting workflows.

**Status: 0.3.0 review edition.** Includes an agent prompt, first-run onboarding, operating instructions, workflow, voice examples, data contract, blank record, fictional worked example, offline helper and acceptance checklist. No accounts, external dependencies, scheduled jobs or transactions.

## Try it safely
From repository root:
```sh
python3 templates/celebration-coordinator/workspace/scripts/plan.py templates/celebration-coordinator/workspace/examples/example.json
openclaw templates validate ./templates/celebration-coordinator
openclaw templates dev ./templates/celebration-coordinator
```
These checks do not install an agent. To add one, enable Templates in Settings → Labs, inspect first, then deliberately run:
```sh
openclaw templates inspect ./templates/celebration-coordinator
openclaw templates add ./templates/celebration-coordinator
```
Add creates a new ordinary agent; adding again creates another. Templates do not auto-update existing agents. The receiving host controls tools, model, secrets and access. Review [deployment](../../docs/DEPLOYMENT.md) first.

## First conversation
> What are we planning, and when? If you already know the spending limit or the one thing you want to keep, tell me that too.

Or: “Use the fictional example and show me what you do.” Never confuse demo output with a live plan.

## What you get
Read [workflow](workspace/reference/workflow.md), [voice examples](workspace/reference/voice.md), [data contract](workspace/reference/data-contract.md), [optional integrations](workspace/reference/integrations.md), and [acceptance scenarios](ACCEPTANCE.md). The agent maintains private records for you; JSON editing is not onboarding homework.

Helper commands print a private report by default. `--share` prints only explicitly allowlisted public_summary values after exact field approval; review before sharing. No authentication or ACL is provided. Do not accept member/guest queries inside the organizer's private session.

## Limits
The helper validates record shape and computes a bounded report; it doesn't verify real-world facts or constrain the host agent's permissions. No external sends, calendar sync, inventory feed, secure multi-user access or unattended work is implemented. [Test evidence](../../docs/VERIFICATION.md) distinguishes automated checks from unrun conversation/host tests.

## Expanded working services
See the [service playbook](workspace/reference/event-studio.md) and [optional worksheet](workspace/templates/whole-event.md). Includes a fictional worked exchange and pilot acceptance cases. These are authored procedures, not evidence of a model/host pilot.

## Six standalone skills, bundled for review
See [skill routing](workspace/reference/hosting-skills.md). Includes run-of-show production, menu/prep arithmetic, shared potluck signups (Google Sheets default), gift follow-through, event change control and finite reminder lifecycle. Four helpers run offline; no live provider connection is included. Ordinary hosting language replaces forced capacity/stamina framing.

Authoritative skill source: [agent-skills](https://github.com/jjjhenriksen/agent-skills/pull/13). Exact source commit and per-file SHA-256 are recorded in bundled-skills.lock.json. These source copies keep this template independently buildable before ClawHub skill releases exist; there are no fabricated registry dependencies. After publication, a separately reviewed release may pin actual skill references rather than duplicate copies.

Christmas themes may be offered with the template as a separate appearance plugin; there is no theme-to-workflow coupling. This skills update does not install/publish that plugin or claim its unresolved managed-installation check passed.

The existing event record/helper and new skill-specific helpers have separate contracts; see routing before mapping data. No secure guest portal, authenticated provider workflow, unattended browser signup or exactly-once reminder service is claimed.

## Registry-backed release path
The intended ClawHub template release installs these skills from the owner's actual ClawHub releases, with exact versions and no duplicate bundled copies. Until skill publication is approved, this review package stays runnable offline. [Release projection and gates](../../docs/CELEBRATION-REGISTRY-RELEASE.md) documents the offline helper and what remains blocked on real publication receipts.
