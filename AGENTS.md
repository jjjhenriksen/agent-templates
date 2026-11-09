# Repository guidance

This repository contains public, portable planning templates. Never import private workspace instructions, memories, real records, credentials, absolute local paths or channel IDs. Preserve user work. Every package must be independently buildable using OpenClaw Templates with explicitly mapped assets. No live Add, registry upload, transactions, provider sends, or scheduler changes in tests.

Keep human voice examples and capability boundaries accurate. Python helpers must remain offline/read-only and standard-library only. Add regression tests for math/privacy/assignment changes. Run tests, repository checks and non-installing package validation/build before claiming a release is verified. Host security and conversational behavior require separate tests; don't label them passed from source inspection.
