# Hosting and gift skills

Load only the matching skill for the requested task; do not run all six as onboarding.

| Request | Read |
|---|---|
| Plan/run a dinner, party, holiday event or cleanup | [hosting-run-of-show](../skills/hosting-run-of-show/SKILL.md) |
| Menu, recipe quantities, shopping or kitchen schedule | [menu-prep-planner](../skills/menu-prep-planner/SKILL.md) |
| Shared contributions, potluck slots or claim changes | [potluck-signup-coordinator](../skills/potluck-signup-coordinator/SKILL.md) |
| Gift ideas, budgets, orders, wrapping, delivery or returns | [gift-season-manager](../skills/gift-season-manager/SKILL.md) |
| Changed headcount, date, budget, weather or helper | [event-change-control](../skills/event-change-control/SKILL.md) |
| Finite reminders and their cancellation/reconciliation | [event-reminder-lifecycle](../skills/event-reminder-lifecycle/SKILL.md) |

Google Sheets is the default shared signup tool; a CSV/draft is useful without a connector. A shared editable sheet is not an exclusive-slot database. SignUpGenius packets/exports remain supported; its current terms prohibit automated site use, so browser automation needs provider permission or a verified permitted integration.

The four helpers are optional, Python 3.11+ standard-library, offline/read-only. Their examples and input contracts live inside each skill. Load and review the specific helper before execution. Keep real inputs outside the distributable source. The agent never turns a draft into a live sheet, send, schedule or transaction without host tools and scoped authorization.

These helpers have separate bounded contracts, not a new unified event schema. Existing scripts/plan.py and reference/data-contract.md still own the main record. Menu target_servings/bookings, signup before/after snapshots, gift paid/refund ledger and reminder revisions are derived private inputs. Do not overwrite the main record with a skill example or reinterpret its money fields without explicit mapping. Never count the same purchase in both event and gift totals.

Use plain hosting language. Do not ask for health/stamina details or impose a smaller fallback unless the user requests it or a concrete event constraint calls for it. A UI theme has no authority or workflow meaning.
