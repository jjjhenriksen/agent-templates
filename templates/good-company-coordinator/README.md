# Good Company Coordinator

Cited answers and manageable coordination for nonprofit and community organizers.

**Status: 0.2.0 planning edition.** Includes an agent prompt, first-run onboarding, operating instructions, workflow, voice examples, data contract, blank record, fictional worked example, offline helper and acceptance checklist. No accounts, external dependencies, scheduled jobs or transactions.

## Try it safely
From repository root:
```sh
python3 templates/good-company-coordinator/workspace/scripts/plan.py templates/good-company-coordinator/workspace/examples/example.json
openclaw templates validate ./templates/good-company-coordinator
openclaw templates dev ./templates/good-company-coordinator
```
These checks do not install an agent. To add one, enable Templates in Settings → Labs, inspect first, then deliberately run:
```sh
openclaw templates inspect ./templates/good-company-coordinator
openclaw templates add ./templates/good-company-coordinator
```
Add creates a new ordinary agent; adding again creates another. Templates do not auto-update existing agents. The receiving host controls tools, model, secrets and access. Review [deployment](../../docs/DEPLOYMENT.md) first.

## First conversation
> What’s one thing you need off your plate today—a policy question, an event, or a list of tasks? Give me that and the relevant source, and we’ll start there.

Or: “Use the fictional example and show me what you do.” Never confuse demo output with a live plan.

## What you get
Read [workflow](workspace/reference/workflow.md), [voice examples](workspace/reference/voice.md), [data contract](workspace/reference/data-contract.md), [optional integrations](workspace/reference/integrations.md), and [acceptance scenarios](ACCEPTANCE.md). The agent maintains private records for you; JSON editing is not onboarding homework.

Helper commands print a private report by default. `--share` prints only explicitly allowlisted public_summary values after exact field approval; review before sharing. No authentication or ACL is provided. Do not accept member/guest queries inside the organizer's private session.

## Limits
The helper validates record shape and computes a bounded report; it doesn't verify real-world facts or constrain the host agent's permissions. No external sends, calendar sync, inventory feed, secure multi-user access or unattended work is implemented. [Test evidence](../../docs/VERIFICATION.md) distinguishes automated checks from unrun conversation/host tests.

## Expanded working services
See the [service playbook](workspace/reference/coordination-desk.md) and [optional worksheet](workspace/templates/state-review.md). Includes a fictional worked exchange and pilot acceptance cases. These are authored procedures, not evidence of a model/host pilot.
