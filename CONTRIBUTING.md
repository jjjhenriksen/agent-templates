# Contributing

Keep each package standalone and human-sounding. Use fictional data only. Add/update helper tests, package sources, workflow, voice examples and acceptance scenarios together. New workspace assets need explicit CLAW.md mappings. Preserve attribution, exact versioned dependencies and clear capability limits. Never ship source-workspace memories, credentials, absolute private paths or real contact IDs.

Run `python3 -m unittest discover -s tests -v`, `python3 scripts/check_repo.py`, and the non-installing OpenClaw build gate documented in docs/DEPLOYMENT.md. A checklist of intended behavior is not a passed test; record actual evidence. Don't add publishing, installation, scheduling or live-provider actions to tests. Keep tests dependency-free. Version public changes rather than rewriting an existing immutable release artifact.
