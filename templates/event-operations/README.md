# Event Operations

A practical operations partner for a workshop, community meeting or small conference. Turn scattered commitments into a runnable schedule, resolve the dependencies that matter, and leave the next shift a printable handoff. No dashboard, account or structured intake required.

Start with: “Our workshop is Saturday, doors at 09:30, 35 people. Can you turn these notes into a run of show?” Paste notes you may share with the host. The agent reuses supplied facts, drafts the schedule immediately, and asks only for the missing fact that blocks the next decision.

This complements Celebration Coordinator: celebration handles occasion design, gifts, menus and personal hosting; this package handles operational execution after the event concept is chosen. It does not edit or depend on that package.

## Use
Read BOOTSTRAP.md, then ask for a schedule, readiness check, change assessment or shift handoff. Copy only the resources you need from workspace/templates. Markdown is the normal working format. The optional offline helper accepts a small JSON schedule and prints dependency warnings; the agent can do the same reasoning without Python.

```sh
python3 templates/event-operations/workspace/scripts/readiness.py templates/event-operations/workspace/examples/workshop.json
python3 -m unittest discover -s tests -v
python3 scripts/check_repo.py
openclaw templates validate templates/event-operations
openclaw templates dev templates/event-operations
openclaw templates build templates/event-operations --out /tmp/event-operations.tgz
```

No sends, bookings, spending, reminders or live monitoring are configured. Receiving-host permissions and conversational behavior need separate evaluation. See ACCEPTANCE.md for scenarios, not claimed live results.
