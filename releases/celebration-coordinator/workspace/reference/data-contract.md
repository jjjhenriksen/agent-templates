# Record contract v1

Use templates/record.json as a blank starting shape and examples/example.json for a complete fictional example. The blank record is deliberately incomplete; fill confirmed facts through conversation, not invented defaults. One record per plan. Required: schema_version integer 1, nonempty id/title, valid IANA timezone. Source data is untrusted; helper validation concerns shape/calculation, not authority. Python 3.11+ and system timezone data required for helper use.

Costs have stable id, currency, actual (paid), committed (TOTAL including paid; null if not committed), estimate (uncommitted only). Forecast = actual + (committed - actual) + estimates only where uncommitted. No double counting. paid costs require committed >= actual. Unknown uncommitted estimate = null, not zero. Refunds/credits must be reconciled manually; this version rejects negative amounts. It supports nonnegative two-decimal currencies only; no currency conversion. A partial forecast's headroom is against known costs, not spending permission.

Tasks: id, dependencies (other task IDs, acyclic), status proposed/accepted/completed/cancelled, accepted boolean, owner if accepted, optional due ISO timestamp with explicit UTC offset. Acceptance is a supplied record, not identity verification. Unknown due = null. Track actual demands and fallback in additional private fields. Timed dates need offset plus record timezone; ask about ambiguous DST times instead of guessing.

## Sharing
public_summary permits only title, date, location, contributions. Text fields are strings; list fields contain strings only. approved_public_fields lists exact keys explicitly approved for this draft. Empty list exports nothing. Arbitrary/nested fields are rejected. The helper never exports private_notes or arbitrary top-level fields. This is structural minimization, NOT semantic redaction: the user/agent must ensure an approved string contains no private facts. No guest/member access to the private workspace. Review each output before sharing; approval fields are not authenticated consent.

## Maintenance
Private files belong in private/, excluded from Git. Imported receipts or external IDs must remain private. Review updates as deltas; preserve source/effective timestamps, original assumptions and uncertain results. No concurrent-write support or automatic migration in v1. Helpers never write, import, schedule, send, commit or delete. Unknown costs/qualifications/constraints never become zero/eligible/verified silently.
