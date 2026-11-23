# Travel Copilot

Less trip-planning admin. More useful options.

Compare flights, places to stay and things to do, then turn the shortlist into a practical itinerary with clear costs, dated sources and honest gaps.

## Start with a trip, not a form

> “Plan four nights in Chicago for two people in May, starting from Los Angeles. Budget $1,500 before flights. Compare neighborhoods and give us a relaxed itinerary.”

Or ask for one small job: compare three hotels, estimate the whole-party budget, or revise a day when plans change. You don't need to edit JSON or maintain a dashboard.

## What it helps with

- Flight, accommodation and place comparisons against your dates, party and budget.
- Straightforward itineraries, transport estimates and missing-cost checks.
- Source-labelled recommendations that distinguish estimates from checked inventory.
- Optional accessibility research, pacing, packing and lower-effort alternatives when requested or relevant.
- Private planning records, reusable worksheets and a read-only offline reporting helper.

## Optional provider research

The package declares **goplaces 1.0.0** and **Expedia plugin 1.0.4**. The receiving operator must separately configure provider access, credentials and permissions. Google Places/Routes also needs its CLI/API setup and may incur authorized API charges. Submitted searches disclose their query details to the provider.

Expedia is a single-provider view, not a market-wide search. No successful live-provider integration test is claimed. Without provider access, Travel Copilot can still work from supplied sources and clearly mark what remains unknown.

## Add it deliberately

Download this Template's artifact from ClawHub, extract it, and review its contents. With a compatible OpenClaw CLI, point these commands at the extracted package directory:

```sh
openclaw templates inspect ./package
openclaw templates add ./package --dry-run --json
```

After reviewing permissions and dependencies, enable **Settings → Labs → Templates** and deliberately use `openclaw templates add ./package` to create a new agent. This is a **Template**, not a skill; do not use `openclaw skills install`. Repeated Add creates another agent, not an in-place update.

## You stay in control

Travel Copilot researches and drafts. It does **not** book, pay, cancel, check in, submit claims, contact suppliers or accept terms. Expedia authentication emails require fresh confirmation for the exact address and step. No scheduled refresh, price alerts, calendar sync or unattended service is included.

Keep passport details, payment information, booking locators and live whereabouts out of shared notes. The host chooses the model and controls access. Workspace-only file settings do **not** sandbox shell execution; receiving-host restrictions need separate review and testing.

## Verification and limits

The 0.2.0 base passed 77 offline repository tests, package validation and reproducible builds. Provider dependency preflight was unavailable in the tested runtime; receiving-host installation and live provider behavior remain unverified. These checks are not proof of real-world travel accuracy or host isolation. This documentation release adds the README to the distributed artifact; it does not add runtime capabilities.

## Source and attribution

Created by Jacqueline Henriksen. [Source repository](https://github.com/jjjhenriksen/agent-templates/tree/main/templates/travel-copilot). MIT licensed.

Provider research adapts work from OpenClaw Awesome Templates. Bundled notices are in `workspace/reference/provider-notices.md`.


## Travel Themes · 0.2.5

Includes the pinned `openclaw-travel-themes@0.1.0` plugin dependency: **Window Seat** and **Sleeper Car**, each with light/dark palettes and scenic backgrounds. After the managed Add/install and trust review, choose `travel-themes/window-seat` or `travel-themes/sleeper-car` in Settings → Appearance, and select matching artwork under Background. Appearance remains viewer-controlled: the template does not change your selected theme or layout. Themes register no tools, services, network access or runtime dependencies. Provider setup and all existing research-only boundaries remain unchanged. Existing agents are not automatically upgraded when a new template version is published.
