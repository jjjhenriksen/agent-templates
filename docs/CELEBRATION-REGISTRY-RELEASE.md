# Celebration: consume the owner's ClawHub skills

The public release should install the six skills from the owner's ClawHub releases, pinned to exact versions—not carry duplicate skill source copies. The review edition currently bundles exact local copies because the skills have NOT been published. This is a deliberate offline review stage, not registry-backed installation.

## After owner approval, not before
1. Publish the reviewed skill folders from agent-skills under the selected authenticated publisher. Record actual package references, exact versions and returned source/artifact identities. Confirm registry detail/read access and scan/install eligibility. Do not assume a GitHub handle is the ClawHub publisher or invent successful releases.
2. Supply a private JSON map to scripts/celebration_registry_plan.py: exactly the six skill names, each with ref and version. Ref is its actual registry name (publisher-scoped when applicable); version is exact semver. No live pins file or fabricated public-release manifest is committed before those releases exist.
3. The offline/read-only helper prints a release projection: CLAW manifest containing six kind:skill / source:clawhub requirements, replacement routing based on installed skill discovery, and the exact bundled workspace files to OMIT from a NEW staging package. It never installs, publishes or edits the reviewed source. It does not verify registry existence; use step 1 receipts.
4. Stage a new package with projected manifest/routing and no bundled skill copies. Preserve the original review source. Review other wording and source provenance, bump release version as appropriate, validate/build/inspect and preview Add against the actual registry releases. Remote preflight or missing consent is a blocker, not a reason to silently fall back to duplicates.
5. Present the exact artifact and requirements to the owner for template publication approval. Template Add installs requirements subject to trust/capability/host policy; dependency pinning doesn't grant authority or silently update an already-created agent. No auto-update promises.

The same native profile mechanism can declare the independent Christmas appearance plugin once its actual registry artifact/version and managed installation are verified. Skill selection, event recipes and agent behavior do not depend on which palette is selected. No automatic theme switch is needed.

## Reproduce projection tests

```sh
python3 -m unittest discover -s tests -p test_celebration_registry_plan.py -v
```

Tests use synthetic test-publisher refs only in memory/temp files. They prove exact dependency rendering, no bundled-skill mappings, discovery-based routing, rejection of incomplete/floating inputs and unchanged review source. They do NOT prove any synthetic ref exists, registry permissions or real installation.

Reference: https://docs.openclaw.ai/clawhub/templates.md — packages kind:skill / source:clawhub / ref / exact version; native extension requirements belong in profiles/openclaw.yml. Publication remains gated on owner approval.
