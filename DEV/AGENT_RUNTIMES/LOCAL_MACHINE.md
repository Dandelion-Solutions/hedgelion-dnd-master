# Local-machine transport and verification overlay

This file applies to local-agent sessions that work from a real checkout and have native Git and shell access.

## Fresh remote state

The configured repository remote is the remote transport authority in this runtime. Establish a fresh baseline before substantive work and refresh again before integration/publication or a currentness-sensitive remote mutation. Ordinary in-scope local edits and RED/GREEN iterations use the pinned baseline; they do not require a fetch before each edit. At each required refresh:

1. inspect the configured remote and target branch; do not guess either;
2. run `git fetch --prune <remote>` successfully before treating any remote-tracking ref as current. An alternative is permitted only if it demonstrably updates and prunes the relevant remote-tracking refs; describe that equivalent command in the work record;
3. read the refreshed remote-tracking commit and compare it with the intended base;
4. if the refresh cannot be completed, report the evidence as local-only and do not claim a fresh remote HEAD.

An already-present `refs/remotes/<remote>/<branch>` value is only a cache. A bare `git fetch` without demonstrated update-and-prune effect is not evidence of a fresh remote HEAD.

## Local publication

Use ordinary non-force native Git publication. Before publishing, confirm the exact target branch and that the intended update is a fast-forward. After publication, obtain fresh remote evidence with the applicable native Git remote operation and compare the remote ref with the published commit.

Never force-push a live ref. Branch/ref deletion remains prohibited under `AGENTS.md`; pruning stale local remote-tracking cache during the required fetch does not authorize deleting a remote branch/ref.

## Local verification

Run the task-relevant tests, maintenance audit, validators, build/package checks and other available checks locally on the VPS. Record the actual commands, exit status and any unavailable checks.

GitHub-hosted CI is not available merely because local Git is available. Do not claim that a hosted workflow ran, passed or was inspected unless this runtime actually has that capability. Local verification is valid local evidence; it is not a fabricated CI substitute.

## Bounded local work and isolation

When the current role/task/approved plan authorizes them, ordinary in-scope reversible edits, local tests, diagnostics and task-owned temporary fixtures proceed without per-command PO permission. This overlay does not grant mutation authority to read-only/review roles or expand the task's write set. Runtime/sandbox enforcement still applies; a denied operation must use a permitted equivalent or be reported accurately.

Use the discovered checkout/tool environment; keep the accepted .hdm-devtools dependency policy. Do not change global packages or unrelated machine state. Put detached clean-source validation, isolated parallel tasks and scratch artifacts outside the scanned checkout, under task-owned /tmp/hdm-dev/<session>/<task> where this OpenCode environment permits it. A detached checkout/snapshot does not authorize creating a branch.

Before recursive cleanup, prove the exact target was created by this task, remains within that task's scratch directory after canonical path/symlink resolution, and contains no unowned data. Clean only that target. Never delete someone else's workspace artifacts to make an audit pass. Validate a clean exact-source snapshot when unrelated workspace carriers contaminate the primary checkout, and report both surfaces honestly.

One coordinator owns integration, cursor/status and remote publication. Subagents return bounded deltas/proof; no simultaneous writers to the same physical file or shared Git index. Preserve independent accepted inputs when rebasing/integrating, then run the required checks on final bytes before publication.
