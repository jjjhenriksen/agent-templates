# From notes to a runnable event

## 1. Establish the smallest usable baseline
Extract date, timezone, venue, fixed windows, headcount range, organizer, access constraints and existing commitments. Label source and last confirmation for changeable facts. If event timing is unknown, draft relative timings rather than invent a date. Ask one blocking question, not a questionnaire.

## 2. Build the requested working artifact
For a run of show, include setup, doors, transitions, breaks, program, teardown and keys/venue return. Each critical cue needs start/end, role, named proposed or accepted owner, predecessor, and a concrete readiness check with evidence. “AV done” is weaker than “soundcheck heard from back row, confirmed by AV lead at 09:10.” Acceptance is the person's agreement; readiness is the task's evidence. Keep them separate.

Work backwards from fixed windows. Check overlapping assignments, realistic transition buffers and access/cleanup labor. For dependencies, distinguish completion prerequisites from parallel preparation. If no accepted owner exists, offer a scope reduction or ask the organizer to resolve the critical gap. Don't silently assign a volunteer.

## 3. Test readiness and handle changes
Check only relevant critical dependencies: access route, room release, staff briefing, equipment, signage, arrivals and safe capacity. Mark ready / unconfirmed / blocked using dated evidence, not optimism. A helper warning is not a live inspection. For a change, identify the affected cues, owners and promises, then propose the smallest repair. Preserve original commitments until the organizer decides; record decision, reason, owner and timestamp. Escalate only the decisions needed now, not a giant blocked-action register.

## 4. Hand over
Produce a printable, versioned one-page handoff when asked: next cues, accepted owners, current readiness gaps, contingency trigger and decision authority. Use role/contact references, not private details. Include timezone and last-updated time; don't invent a “confirmed” timestamp. Separate volunteer/public copies from organizer-only logistics. Ask where a shared copy will go when privacy depends on it. Archive or delete private event data only under the owner's retention instruction; no automatic cleanup.

## Optional helper
`scripts/readiness.py` reads a JSON file and writes warnings to stdout only. Nonempty warnings exit 1; malformed input exits 2. `accepted` must be true and `ready` must be true to pass each cue. An owner string is not evidence of consent. Times use one local event-day clock; split overnight events into separate dated schedules. The helper checks prerequisite finish times but not staff overlap, venue conditions, buffers or legal safety. Check those separately. JSON is optional, never a required conversation format.
