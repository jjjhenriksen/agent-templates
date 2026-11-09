# Agent Templates

**Less to keep in your head. More room for the thing you actually want to do.**

Three portable OpenClaw agents by Jacqueline Henriksen. Practical, human-sounding planning partners—not bots that hand you a longer checklist and call it help.

| Template | What it takes off your plate | First useful output |
|---|---|---|
| [Celebration Coordinator](templates/celebration-coordinator) | Occasions, guests, gifts, meals, budgets and changing capacity | A realistic plan, smaller fallback and next three actions |
| [Travel Copilot](templates/travel-copilot) | Comparing options, access checks, trip costs and disruption planning | A source-labelled trip packet with normal/lower-capacity variants |
| [Good Company Coordinator](templates/good-company-coordinator) | Repeated policy questions, volunteer matching and draft follow-ups | A cited answer or reviewable coordination packet |

**Release: 0.1.0, planning editions.** Complete package sources, onboarding, workflows, voice examples, blank records, fictional examples, offline reporting helpers, acceptance checklists and test automation. No accounts, paid services, hidden installs, preconfigured reminders or external transactions. They are not fully autonomous service integrations. Conversation-level quality and receiving-host security still need pilot evaluation.

## Start here
```sh
git clone https://github.com/jjjhenriksen/agent-templates.git
cd agent-templates
python3 -m unittest discover -s tests -v
python3 scripts/check_repo.py
```
Python 3.11+ with standard library and timezone data is needed only for helpers/tests. No pip dependencies. For agent packaging, OpenClaw Templates is experimental; packages were checked with OpenClaw 2026.11.1. The receiving model and tools are selected by your host, not the package.

### Inspect before adding
```sh
openclaw templates validate ./templates/celebration-coordinator
openclaw templates dev ./templates/celebration-coordinator
openclaw templates inspect ./templates/celebration-coordinator
```
These commands do not install an agent. Enable **Settings → Labs → Templates** before deliberately using `openclaw templates add ./templates/celebration-coordinator`. Replace the directory for the other agents. Each Add creates a new ordinary agent; adding again creates another. No in-place template upgrade lifecycle is promised. See [deployment](docs/DEPLOYMENT.md).

## Human by design
They ask what unlocks the next step, not twenty onboarding questions. They use contractions, ordinary language and concrete options. They acknowledge a difficult constraint without a pep talk. They don't pretend to have taken trips, cooked dinners or worked at your organization.

> “Then the menu changes, not your spending limit.”
>
> “That's a starting point, not enough to book on.”
>
> “That's the gap—not evidence that anyone missed a commitment.”

See the individual voice guides for full fictional exchanges.

## What's included—and what isn't
- Package-root `CLAW.md`, `package.json`, `BOOTSTRAP.md`, README, sources, MIT license, acceptance checklist.
- Explicitly declared workspace instructions, procedures, templates, example JSON and offline `scripts/plan.py`.
- Helpers perform exact decimal calculations, narrow public projection and bounded candidate screening. They never write records, make network calls, schedule or send.
- Optional calendar/email/reminders require separate scoped setup, approval, credentials and execution tests. They are not dependencies smuggled into a “complete” template.
- Good Company is adapted from [the original project](https://github.com/jjjhenriksen/good-company). Its database, FTS5, transactional ledger, provider integrations and unattended cycles are **not** included. See [architecture](docs/ARCHITECTURE.md).

## Read before using
[Research findings](docs/FINDINGS.md) · [architecture](docs/ARCHITECTURE.md) · [deployment](docs/DEPLOYMENT.md) · [privacy/security](SECURITY.md) · [verification](docs/VERIFICATION.md) · [contributing](CONTRIBUTING.md)

Keep actual guest lists, reservations, member records and contacts out of this repository. “Local-first” storage does not mean local inference, and prompt instructions aren't access controls. GitHub hosting is not ClawHub registry publication; neither installs an agent for you.
