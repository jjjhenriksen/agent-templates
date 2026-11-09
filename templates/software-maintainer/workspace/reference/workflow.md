# Bounded change workflow

## Inspect before editing
Locate repo root, applicable AGENTS.md and contribution/security guides. Inspect current branch, revision, status (including untracked files) and relevant diffs without dumping secret contents. Identify protected/generated paths and user-owned edits. Never reset, clean, force checkout or stash them to make work convenient. If overlap is unavoidable, ask which change to preserve or work in a separate authorized checkout. Don't assume a dirty file is yours.

Read the issue and nearby code/tests. Establish observable acceptance criteria and explicit non-goals in a few lines; reuse existing criteria. Record the baseline revision and relevant pre-existing failure. For mutable or external facts use current source evidence, not memory. Run commands only within host authorization; inspect project scripts before executing. Avoid unreviewed install hooks, network and services. If execution is unavailable, state that and continue with static reasoning.

## Implement and verify
Trace the failure, make the smallest complete fix, and add a regression test that fails before and passes after. Consider API compatibility, invalid inputs and security effects. Follow local style, dependencies, test runner and documentation conventions. Don't casually update lockfiles, generated code or unrelated formatting. A docs-only request needs an actual edit and link/example checks, not fictional test coverage.

Use a reviewable patch. For each acceptance criterion, identify the smallest meaningful test. Run targeted checks first, then the repo's required broader gates when available. Record command, working directory, exit/result and tested revision or a clear “working tree based on <revision>, including this patch” identifier. Tests run before the last source edit don't verify the last source edit. If anything changes after testing, rerun relevant checks. Separate pre-existing failures, new failures and unavailable checks; never call not-run passed.

## Review and deliver
Read the final diff, including untracked additions, for accidental files, secrets, generated output, behavior and error cases. Compare against initial scope and status; confirm unrelated edits remain intact. Fix substantive review findings, retest changed code, and keep the same task moving.

Default handoff: what changed, relevant files, exact checks/results, remaining risk. No mandatory ledger. If authorized to commit, stage explicit owned paths, inspect staged diff and leave unrelated changes unstaged. If authorized to open a PR, verify intended remote/base and head, push only that branch, open the PR and return its URL. CI pending is pending; local tests are not CI. If delivery tools are unavailable, return the patch and blocker rather than promising later publication. Never merge, publish packages, deploy, rotate credentials or migrate data merely because implementation was authorized.
