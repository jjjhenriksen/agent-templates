# Optional assignment automation lane

## Implemented, runnable without accounts
`scripts/refresh.py` re-reads explicitly authorized local JSON exports on each invocation, validates timestamps and assignment states, detects added/removed/changed assignments, orders open deadlines, and emits a dated daily brief, optional due reminders, source coverage and a proposed checkpoint. Standard-library only; read-only, no network, no credentials, installation, submission or instructor messages. Export removal means **absent from this export**, not completed or deleted in the LMS. Course policy checks still govern any assessed work.

Supply one config alongside the export files (private workspace, never public source checkout):
```json
{"timezone":"Europe/London","brief_time":"08:30","stale_hours":24,"reminders":true,"reminder_hours":24,"sources":[{"id":"course-a","authorized":true,"path":"course-a.json"}]}
```
Each configured source is required coverage; include inaccessible courses too. Missing files produce explicit gaps, not an empty successful scan. Export shape:
```json
{"observed_at":"2030-04-11T08:00:00Z","assignments":[{"id":"response-1","due_at":"2030-04-12T17:00:00Z","status":"draft"}]}
```
Use opaque aliases; valid statuses: not-started, draft, submitted, graded. Unknown deadline is null. `observed_at` is the actual source inspection/export time, NEVER runner time or file modification time. Keep original URL/file/section receipts in a private source index keyed by source ID; attach those receipts when presenting the brief. This runner cites source alias and observation date, not invented live LMS evidence.

From the added workspace:
```sh
python3 scripts/refresh.py private/refresh/config.json --now 2030-04-11T08:30:00Z
python3 scripts/refresh.py private/refresh/config.json --state private/refresh/checkpoint.json --now 2030-04-11T09:30:00Z
```
`--now` must be supplied by the caller's verified clock (fixed in tests). Config paths resolve relative to the config file, cannot escape that directory even via symlinks. Invalid/missing source retains the last valid snapshot with warning; stale data remains visibly stale. Removed configured sources disappear from the brief. No automatic source discovery. Deadline order is not an effort-aware recommendation; the agent adjusts the top three using known rubric/dependencies/capacity without concealing unknown dates.

## Optional host automation, not an installed sync engine
Investigated 2026-11-09: OpenClaw 2026.11.1 `automations --help` and `automations add --help`; official automation schedules documentation supports `--cron` plus `--tz`, isolated agent turns, command payloads and delivery targeting. Docs index also uses `create`; this installed CLI exposes `add`. Use receiving-host help/schema, not a guessed command. References: https://docs.openclaw.ai/automation/cron-jobs.md and https://docs.openclaw.ai/automation/cron-jobs/schedules.md.

An operator can authorize an isolated agent job on that host, selecting the actual added agent, private source root, timing/timezone, recipient and allowed tools. Use one stable declaration/job ID; inspect before adding another. Suggested job: hourly refresh during approved hours, brief at the configured local time; or daily only with explicitly daily detection latency. `brief_time` is a gate, not a scheduler: first run at/after it emits once per local date, including DST repeated hours. Reminders default to the config opt-in, never infer consent. Disable/reconcile the same job on pause/revocation/course close; don't leave recurring jobs after the term. No cronJobs are declared by this package.

Authorized job turn contract:
1. Read source index and config; refresh only explicitly authorized sources. With only supplied exports, re-read them unchanged; don't relabel observation dates. A separately authorized browser may inspect exact assignment/rubric pages and update exports, retaining original receipts and scan scope. Authentication through host secure UI only; no passwords/tokens in chat. This is a manual/browser adapter procedure, NOT a bundled LMS API connector. Failed login/pagination/filter coverage must remain missing/stale.
2. Run refresh with current offset-aware clock and existing checkpoint. A corrupt checkpoint is a failure: preserve it, don't silently reset deduplication. Serialize runs; concurrent checkpoint writers aren't supported.
3. Review concise brief/notifications plus coverage. Share only with the authorized student destination. Don't send checkpoint JSON, raw records or private source text. If both outputs are empty, remain quiet; still flag failed/stale coverage in the daily brief.
4. `next_state` is a proposed local emission checkpoint, NOT a delivery receipt. After confirmed delivery (or intentional no-output run), the host may atomically save it privately under scoped write authority, preserving last good revision. On failed/unknown send, retain pending output and reconcile the original delivery before retrying. No exactly-once external delivery guarantee. Do not advance checkpoint before reconciliation or blindly resend. Without host writes, persist it manually or accept repeat outputs; the helper never claims durable dedup itself.

## Limits and fallback
No Canvas API, OAuth, iCalendar parser, authenticated LMS refresh, scheduler creation, persistent store, transport or multi-user service is bundled. Local supplied-source refresh/diff/brief is implemented; unattended live LMS acquisition and delivery remain unconfigured integration work requiring receiving-host verification. Without shell, perform a dated supplied-source brief conversationally and label calculations/diffs unverified. Without scheduler, run on demand. Never call stale exports a live sync. Snapshot freshness is supplied evidence, not authenticated truth.
