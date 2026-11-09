# Schoolwork Copilot
A practical coursework partner: turn a prompt and rubric into a realistic plan, explain difficult material, support permitted research/writing/code, and verify the result without inventing evidence.

**0.1.0 planning edition.** Input: assignment materials, course rules, desired help and optional authorized LMS view. Output: a rubric-grounded work packet, source receipts, a smaller fallback and verified completion gaps. Read [sources](SOURCES.md), [acceptance scenarios](ACCEPTANCE.md) and [workflow](workspace/reference/workflow.md).

Includes portable adaptations of coursework drafting, Canvas LMS navigation, numerical/algorithm verification and cross-draft merging procedures. Institution-neutral and fictional-data-only. The host supplies model, browser/file tools and permissions; no login, integrations, external skills, paid services or automations are installed. Canvas guidance is not a Canvas API connector. Course AI/collaboration rules determine the permitted help. No grade guarantees or autonomous submissions.

From repository root:
```sh
openclaw templates validate ./templates/schoolwork-copilot
openclaw templates dev ./templates/schoolwork-copilot
python3 templates/schoolwork-copilot/workspace/scripts/plan.py templates/schoolwork-copilot/workspace/examples/example.json
```
These commands do not install an agent. See [deployment](../../docs/DEPLOYMENT.md) before deliberate Add. Keep real records in the receiving private workspace; never commit them here. The optional read-only helper orders known deadlines and flags unknown ones; it does not estimate effort, schedule, monitor or submit work.
