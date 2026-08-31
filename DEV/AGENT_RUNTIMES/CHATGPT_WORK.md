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
-> create commit with expected parent
-> non-force update ref
-> verify ref/tree
```

For repository text files, use Connector UTF-8 text interfaces directly. Do not manually Base64-encode/decode Markdown, JSON, YAML, Python, configuration or other semantic text for transport.

## Verification

Use Connector read-back as remote-publication evidence. Inspect hosted CI/status when it is available and required by the task; if no run/status can be obtained, state that limitation rather than treating CI as passed.

Use the current ChatGPT Work/Codex skills and tools when available. Their availability is runtime evidence, not a promise made to local-agent sessions.
