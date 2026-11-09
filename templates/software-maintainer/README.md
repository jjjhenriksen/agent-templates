# Software Maintainer

A working coding partner for a bounded bug fix, test or small feature—not a delivery-ledger generator. It inspects the repository, protects existing edits, implements the change when tools permit, and hands over a reviewable patch with honest test evidence.

Start with: “Fix this parser crash. Keep the public API unchanged; don't touch the generated files.” Supply a repository through your host's authorized workspace. The agent reads local instructions, establishes acceptance criteria from the issue, and works to the smallest verified change.

No GitHub account, MCP server or network access is required for local work. Without write/exec tools it can produce a proposed patch and commands, explicitly unexecuted. PR creation, pushes and release actions require the appropriate tools and scoped authority. No credentials, integrations, jobs or tool sandbox are shipped.

## Try the fictional repair exercise
Ask the agent to fix workspace/examples/repair-repo under the instructions there. Its failing regression test is an intentional input, not a package-suite failure. The desired behavior and independent acceptance checks are in ACCEPTANCE.md. Do not mistake supplied expectations for observed results.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repo.py
openclaw templates validate templates/software-maintainer
openclaw templates dev templates/software-maintainer
openclaw templates build templates/software-maintainer --out /tmp/software-maintainer.tgz
```

Use templates/change-brief.md only if a brief helps; a small fix usually needs a few sentences and the patch. Receiving-host isolation and conversation quality require separate pilot evaluation.
