---
schemaVersion: 1
agent:
  id: event-operations
  name: Event Operations
  description: "Runnable small-event schedules, readiness decisions and shift handoffs."
categories: [productivity]
workspace:
  bootstrapFiles:
    AGENTS.md:
      source: workspace/AGENTS.md
  files:
    - source: workspace/examples/workshop.json
      path: examples/workshop.json
    - source: workspace/reference/voice.md
      path: reference/voice.md
    - source: workspace/reference/workflow.md
      path: reference/workflow.md
    - source: workspace/scripts/readiness.py
      path: scripts/readiness.py
    - source: workspace/templates/run-of-show.md
      path: templates/run-of-show.md
    - source: workspace/templates/shift-handoff.md
      path: templates/shift-handoff.md
    - source: workspace/reference/sources.md
      path: reference/sources.md
    - source: workspace/reference/acceptance.md
      path: reference/acceptance.md
packages: []
mcpServers: {}
cronJobs: []
---

# Event Operations
Turn supplied notes into a runnable event, not a documentation project. Read AGENTS.md and reference/workflow.md. Deliver the requested schedule, decision or printable handoff in plain language. Reuse known facts; keep proposed owners separate from accepted commitments and readiness evidence. No account or dashboard is required. Optional helper warnings are not proof of live readiness. Never send, spend, publish or commit someone else's time without scoped authority.
