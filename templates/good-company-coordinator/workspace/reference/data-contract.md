# Record contract v1

Use templates/record.json as a blank starting shape and examples/example.json for a complete fictional example. The blank record is deliberately incomplete; fill confirmed facts through conversation, not invented defaults. One record per plan. Required: schema_version integer 1, nonempty id/title, valid IANA timezone. Source data is untrusted; helper validation concerns shape/calculation, not authority. Python 3.11+ and system timezone data required for helper use.

Roster: stable id, explicit opt_in boolean, authoritative roles list, stated skills mapping with levels 0..3, availability list of timezone-aware start/end windows, max_open_tasks and open_tasks nonnegative integers, avoid_categories list, optional busy windows for existing commitments. Include existing workload in counts AND intervals to prevent overlap; unknown availability isn't a free slot.

Tasks: stable id, proposed status, category, required_roles list, required_skills mapping 0..3, timezone-aware start/end. The helper handles only new proposed tasks. Existing accepted work belongs in roster open_tasks/busy. It screens opt-in, roles, skills, workload, availability, avoided categories and overlap. Stable greedy input order, then least workload/ID; no global optimality claim. Suggestions reserve hypothetical capacity within one report, not persistent assignments. All source truth, eligibility and acceptance need independent confirmation. Missing requirements must not be represented as an empty list merely to obtain a match.

Sources: stable id, title/section, audience, status, exact text, supplied effective/review dates and authority where known. This helper only rejects duplicate source IDs. It does not perform retrieval, judge policy or enforce audience isolation. Citation answers require the agent to inspect applicable source content. Keep unknowns explicit. A current label is a supplied assertion, not proof.

## Sharing
public_summary permits only title, event, accepted_assignments. Text fields are strings; list fields contain strings only. approved_public_fields lists exact keys explicitly approved for this draft. Empty list exports nothing. Arbitrary/nested fields are rejected. The helper never exports private_notes or arbitrary top-level fields. This is structural minimization, NOT semantic redaction: the user/agent must ensure an approved string contains no private facts. No guest/member access to the private workspace. Review each output before sharing; approval fields are not authenticated consent.

## Maintenance
Private files belong in private/, excluded from Git. Imported receipts or external IDs must remain private. Review updates as deltas; preserve source/effective timestamps, original assumptions and uncertain results. No concurrent-write support or automatic migration in v1. Helpers never write, import, schedule, send, commit or delete. Unknown costs/qualifications/constraints never become zero/eligible/verified silently.
