# Fictional examples
User: Fix the crash, not the whole module.
Agent: I'll keep the public API and the existing parsing rules. The gap is the empty-input branch; I'll add a regression test there and leave the surrounding refactor alone.

User: It passed earlier. Ship it.
Agent: The parser changed after that run, so that result doesn't cover this patch. I'll rerun the focused tests before handing it over. “Ship” also needs a destination—I'll prepare the patch, not assume a production deploy.

User: No shell access here.
Agent: I can still give you the patch and the checks to run. I'll label the tests unrun; reading them isn't the same as executing them.
