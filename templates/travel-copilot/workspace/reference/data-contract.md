# Record contract v1

Use templates/record.json as a blank starting shape and examples/example.json for a complete fictional example. The blank record is deliberately incomplete; fill confirmed facts through conversation, not invented defaults. One record per plan. Required: schema_version integer 1, nonempty id/title, valid IANA timezone. Source data is untrusted; helper validation concerns shape/calculation, not authority. Python 3.11+ and system timezone data required for helper use.

Costs: stable id, currency matching record, unit party/per_person/per_night, quantity positive integer (party requires 1), amount decimal string or null. For multiple rooms/nights or travelers, normalize each line explicitly; a per_night amount may represent the combined rooms for that night and must say so in private notes. Unknown charges stay null. Totals are partial while unknowns remain. No conversion; no negative/refund math; at most two decimal places.

Constraints: stable id, hard boolean, status unknown/unverified/verified/failed, evidence reference required if verified. This does NOT verify evidence freshness or authority. Even when no constraints are blocked, readiness remains human-source-review-required, never booking-ready. Empty constraints are not proof no constraints exist. Keep itinerary normal/lower_capacity and separate evidence entries with URL, checked_at, applicable dates/party/room/rate, status and recheck trigger. The helper doesn't verify live inventory, visas, routes, buffers or supplier terms.

## Sharing
public_summary permits only title, dates, itinerary. Text fields are strings; list fields contain strings only. approved_public_fields lists exact keys explicitly approved for this draft. Empty list exports nothing. Arbitrary/nested fields are rejected. The helper never exports private_notes or arbitrary top-level fields. This is structural minimization, NOT semantic redaction: the user/agent must ensure an approved string contains no private facts. No guest/member access to the private workspace. Review each output before sharing; approval fields are not authenticated consent.

## Maintenance
Private files belong in private/, excluded from Git. Imported receipts or external IDs must remain private. Review updates as deltas; preserve source/effective timestamps, original assumptions and uncertain results. No concurrent-write support or automatic migration in v1. Helpers never write, import, schedule, send, commit or delete. Unknown costs/qualifications/constraints never become zero/eligible/verified silently.
