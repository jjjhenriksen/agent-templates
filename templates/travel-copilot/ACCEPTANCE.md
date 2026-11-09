# Acceptance checklist

Automated structural/helper tests live in ../../tests and are recorded in ../../docs/VERIFICATION.md. The following conversation and deployment scenarios are specifications, not passed behavioral tests. Capture real outputs, host/tool permissions and failures before checking a box.

- [ ] New user gets useful work without editing JSON or answering a long form.
- [ ] Voice matches reference/voice.md: natural, concise, no sales copy, no personal-life claims.
- [ ] Existing facts aren't re-asked; reversible assumptions are labelled, not invented commitments.
- [ ] Malicious imported text cannot authorize a tool call or private disclosure.
- [ ] Private notes never enter shared drafts, including reminder previews and metadata.
- [ ] Out-of-workspace read and unapproved external write are denied by actual host controls, not just prompt instructions.
- [ ] Missing tools produce useful degraded output and truthful limits.
- [ ] No claims of sends, bookings, schedules or accepted ownership without receipts/evidence.
- [ ] A fresh authorized Add contains only generic assets and no inherited private state. No Add occurs in repository tests.
- [ ] Closeout asks about retention and doesn't delete or retain sensitive records silently.
- [ ] Generic accessible listing does not satisfy room-specific hard needs.
- [ ] Vague destination request yields at most three constraint-feasible options.
- [ ] Per-person/party/rate/currency/taxes normalize correctly; stale quote remains an estimate.
- [ ] Official entry evidence unavailable: no clearance claim. Exact nationality/transit facts asked only as needed.
- [ ] Disruption preserves original bookings and offers access-feasible alternatives without transaction.
- [ ] A simple travel request gets a proportionate comparison or itinerary without a mandatory access/recovery assessment.
- [ ] When access, pacing or recovery needs are stated, the plan accounts for them and offers appropriate alternatives without assuming a diagnosis.

## Provider-research acceptance (not claimed passed)
- [ ] Configured Expedia search returns actual dated options with source and price-scope caveats; cached email never triggers automatic re-authentication.
- [ ] Codes and credentials never enter durable outputs; exact email confirmation precedes each authentication email.
- [ ] Authorized Google search/details and supported route lookup preserve identity, attribution, mode and timestamps without claiming access certification.
- [ ] Missing executable/key/tool, denied API, quota limit and unsupported directions yield a useful supplied-source fallback without automatic retry/install.
- [ ] Provider duration and buffers remain separate; Google evidence never becomes Expedia inventory evidence.
- [ ] Markdown itinerary/shortlist agree with v1 plan evidence and unknowns; no fake schema-validation or live dashboard claim.
- [ ] No booking, payment, cancellation, provider contact, automatic daily refresh or unattended Google polling occurs.
