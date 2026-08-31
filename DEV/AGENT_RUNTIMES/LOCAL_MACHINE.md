# Local-machine transport and verification overlay

This file applies to local-agent sessions that work from a real checkout and have native Git and shell access.

## Fresh remote state

The configured repository remote is the remote transport authority in this runtime. Before a correctness-sensitive write:

1. inspect the configured remote and target branch; do not guess either;
2. run `git fetch --prune <remote>` successfully before treating any remote-tracking ref as current. An alternative is permitted only if it demonstrably updates and prunes the relevant remote-tracking refs; describe that equivalent command in the work record;
3. read the refreshed remote-tracking commit and compare it with the intended base;
4. if the refresh cannot be completed, report the evidence as local-only and do not claim a fresh remote HEAD.

An already-present `refs/remotes/<remote>/<branch>` value is only a cache. A bare `git fetch` without demonstrated update-and-prune effect is not evidence of a fresh remote HEAD.

## Local publication

Use ordinary non-force native Git publication. Before publishing, confirm the exact target branch and that the intended update is a fast-forward. After publication, obtain fresh remote evidence with the applicable native Git remote operation and compare the remote ref with the published commit.

Never force-push a live ref unless the human architect explicitly authorizes the exact ref and operation.

## Local verification

Run the task-relevant tests, maintenance audit, validators, build/package checks and other available checks locally on the VPS. Record the actual commands, exit status and any unavailable checks.

GitHub-hosted CI is not available merely because local Git is available. Do not claim that a hosted workflow ran, passed or was inspected unless this runtime actually has that capability. Local verification is valid local evidence; it is not a fabricated CI substitute.
