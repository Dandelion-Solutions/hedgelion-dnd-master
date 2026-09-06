# ChatGPT Work / Codex runtime overlay

This file applies only to a ChatGPT Work / Codex session that has connected GitHub Connector access.

## Repository transport

Use the connected GitHub Connector for all remote repository communication: refs, commits, trees, blobs, files, comparisons, branch updates, pull requests, issues and hosted-CI reads.

Do not use native Git/GitHub CLI/direct HTTP as a fallback for remote transport in this runtime. In particular, do not run `git clone`, `git fetch`, `git pull`, `git push`, `git ls-remote`, `gh ...`, curl/Python HTTP credential workarounds or SSH/token bypasses.

If the Connector lacks a required capability, report that specific capability gap rather than bypassing it.

## Fresh state and publication

Before a correctness-sensitive remote write, read the current target ref through the Connector. Construct the intended commit from that verified parent, update the ref without force unless explicitly required, then verify the remote ref/tree again.

For multi-file or structural changes, prefer Connector Git-data publication:

```text
read current ref
-> create UTF-8 blobs / reuse existing blob+tree SHAs
-> create tree from verified parent tree
-> create commit with verified parent
-> non-force update ref
-> verify ref/tree
```

### Current ref-transition capability note

The currently exposed Connector ref-update action accepts a target branch/ref, a new commit SHA and a `force` boolean. It does **not** expose a separate expected-old/current-ref SHA argument.

Therefore a preceding ref read is not an atomic compare-and-swap by itself. For HDM-owned append-only refs, correctness-sensitive publication uses the already-accepted monotonic fence:

```text
pin H
-> create intended commit C with parent(C) = H
-> request ref -> C with force=false
```

If the ref has advanced from `H` to an intervening accepted descendant/sibling lineage, stale `C(parent=H)` must not be made current by force or history rewrite. A non-fast-forward rejection is a stale/currentness conflict, not authority to retry blindly.

Any observed force rewrite, rewind, deletion/recreation or other non-monotonic authority-ref movement is outside this supported automatic publication model. In that case invalidate prepared work crossing the discontinuity and fail closed into bounded currentness/integrity recovery before another authority-changing attempt.

Initial ref creation is create-if-absent. A racing/existing ref is a creation conflict, never permission to overwrite it.

Canonical gameplay/publication interpretation is owned by `DEV/docs/superpowers/specs/2026-09-06-hdm-publication-currentness-supported-ref-repair-amendment.md`; this development overlay records the current tool capability and does not independently redefine gameplay semantics.

For repository text files, use Connector UTF-8 text interfaces directly. Do not manually Base64-encode/decode Markdown, JSON, YAML, Python, configuration or other semantic text for transport.

## Verification

Use Connector read-back as remote-publication evidence. Inspect hosted CI/status when it is available and required by the task; if no run/status can be obtained, state that limitation rather than treating CI as passed.

Use the current ChatGPT Work/Codex skills and tools when available. Their availability is runtime evidence, not a promise made to local-agent sessions.
