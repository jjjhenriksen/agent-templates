# Agent Templates

**Less to keep in your head. More room for the thing you actually want to do.**

Five portable OpenClaw agents by Jacqueline Henriksen. Practical, human-sounding planning partners—not bots that hand you a longer checklist and call it help.

| Template | What it takes off your plate | First useful output |
|---|---|---|
| [Schoolwork Copilot](templates/schoolwork-copilot) | Rubrics, coursework planning, study and permitted research/drafting | A source-backed assignment packet with next steps and verification gaps |
| [Celebration Coordinator](templates/celebration-coordinator) | Occasions, guests, gifts, meals, budgets and changing capacity | A realistic plan, smaller fallback and next three actions |
| [Travel Copilot](templates/travel-copilot) | Comparing flights, stays and places, trip costs and itinerary planning | A source-labelled comparison or trip plan tailored to the request |
| [Good Company Coordinator](templates/good-company-coordinator) | Repeated policy questions, volunteer matching and draft follow-ups | A cited answer or reviewable coordination packet |

**Versions: Travel Copilot 0.2.0; other packages 0.1.0.** Complete package sources, onboarding, workflows, voice examples, blank records, fictional examples, offline reporting helpers, acceptance checklists and test automation. Travel Copilot now declares pinned Expedia and goplaces dependencies for operator-configured research; other packages remain dependency-free planning editions. No credentials, hidden account setup, preconfigured reminders or transactions. Google API usage can incur operator-authorized charges. They are not autonomous booking or service agents. Conversation-level quality and receiving-host security still need pilot evaluation.

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

## Current registry releases

[Celebration Coordinator 0.3.2](releases/celebration-coordinator) migrates the manifest and declares Christmas Themes plus Instacart MCP. [Everyday Meal Planner](templates/meal-planner) plans ordinary weeks, pantry-first shopping, prep and leftovers, with optional Instacart MCP. Neither source connects an account or orders groceries. See [current release validation](docs/MEAL-THEMES-VERIFICATION.md). Older bundled review editions and their historical tests are retained, not silently treated as current registry artifacts.
