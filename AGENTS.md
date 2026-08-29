# HDM Development Agent Instructions

## Scope

This file governs **development work on the HDM engine repository**. It is not part of gameplay/runtime instructions and is never shipped in the runtime release asset.

## Fresh development-session bootstrap

A fresh development chat/session must recover current project state from the repository before doing substantive analysis, proposing architecture, or asking the repository owner to restate information that is already recoverable from project sources.

For architecture/deep-work activity, use this bootstrap order:

```text
current remote ref/state
-> AGENTS.md
-> DEV/DESIGN_PROCESS.md
-> DEV/ARCHITECTURE/DESIGN_PROCESS.md
-> DEV/PROJECT_MAP.md
-> current roadmap/status authority
-> task-specific owning artifacts and relevant evidence
```

At minimum:

1. determine the active remote ref and read current repository state through the connected GitHub transport;
2. read the current `AGENTS.md` on that ref;
3. read the current applicable design-process files rather than relying on remembered versions;
4. read `DEV/PROJECT_MAP.md` and use it to identify the task-specific ownership/dependency route;
5. read the current roadmap/status authority for architecture sequencing when the task is architectural;
6. inspect the actual owning artifacts and relevant neighboring consumers before making correctness-sensitive claims.

Conversation history, model memory, handoff summaries, prior-agent summaries, search snippets and derivative indexes may accelerate orientation, but they are not substitutes for current repository evidence when the owning source is available.

Do not make the repository owner reconstruct repository topology, previous decisions, document contents, accepted constraints, or current stage state that the agent can establish from the repository itself.

## Development design process

Before architecture, system design, deep technical research, or other development work whose scope may affect architecture:

1. read and follow `DEV/DESIGN_PROCESS.md`;
2. for HDM architecture work, also read and follow `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

`DEV/DESIGN_PROCESS.md` is the canonical general development/design process. `DEV/ARCHITECTURE/DESIGN_PROCESS.md` is the project-specific HDM adapter and adds constraints; it does not replace or weaken the general process.

Do not rely on remembered versions of these rules. Read the current files on the active branch before substantive architecture/deep-work activity.

## Documentation evidence and synthesis discipline

Repository documentation volume is an **agent workload problem**, not a human proofreading obligation.

The agent is responsible for discovering the relevant source set, reading it to the depth required by the claim, preserving material qualifiers, reconciling it with current owners, and checking completeness before synthesis. The repository owner should receive decision-ready conclusions and genuine architectural trade-offs, not a request to manually verify whether the agent missed something in a large document corpus.

Hard rules:

- `DEV/PROJECT_MAP.md`, `CANONICAL_ARCHITECTURE_INDEX.md`, roadmaps, summaries, executive syntheses, search results and conversation summaries are routing/compression aids. They do not replace actual owning artifacts for correctness-sensitive conclusions.
- Do not claim architecture, roadmap, requirement, research or review coverage from thematic overlap, representative sampling, remembered content, headings, or an executive summary when the underlying relevant source material is available.
- When a source contains individually enumerated requirements, findings, risks, review issues, candidates, test cases, schema members, deferred items or similar records, preserve item-level semantics where the task depends on coverage. A broad statement such as "the themes are covered" is not evidence that the set is accounted for.
- Qualifiers are part of the evidence. Conditions such as scope limits, confidence, exceptions, non-goals, `revisit when`, defer triggers, negative findings and applicability constraints must survive extraction and synthesis.
- For deep work, use the source-manifest / evidence-extraction / completeness gates defined by `DEV/DESIGN_PROCESS.md` and the HDM-specific rules in `DEV/ARCHITECTURE/DESIGN_PROCESS.md` before producing a roadmap, Decision Brief, candidate specification, coverage claim or canonicalization result.
- A large repository does **not** imply preloading or rereading the entire repository for every task. Use `DEV/PROJECT_MAP.md` to identify the relevant dependency subgraph, then exhaust that task-specific source set to the degree necessary for the claims being made.
- Do not ask the human architect to compensate for incomplete document research. Escalate only the residual product semantics, priorities, material trade-offs, risk acceptance or other decisions that genuinely require human judgment.

## Repository ownership geometry

The source repository has two product ownership trees:

- `GAME/` — exact source tree of the installed runtime distribution. The release builder archives the **contents** of this directory.
- `DEV/` — architecture, tests, release policy, development catalogs/schemas, Superpowers artifacts and developer tooling.

Repository root is reserved for repository infrastructure/metadata such as `.github/`, this `AGENTS.md`, root `README.md`, `.gitignore` and canonical legal files.

Do not recreate old repository-root product/development directories such as `CORE/`, `TESTS/`, `TOOLS/`, `ARCHITECTURE/`, `RELEASE/`, `CATALOG/`, `SCHEMA/`, `SCHEMAS/`, `CAMPAIGN/`, `TEMPLATE/`, `MIGRATIONS/`, `INSTALL/` or `docs/`.

## Root README editorial contract

The repository-root `README.md` is a **manually curated public-facing document owned by the repository owner**. It is not ordinary development documentation and must not be treated as a convenient place to dump technical state.

### Do not modify it opportunistically

Do **not** rewrite, reorganize, condense, expand, modernize, clean up, normalize, re-template or otherwise reshape the root `README.md` as a side effect of architecture work, repository moves, release/version changes, refactors, path migrations, tooling changes, audits or other unrelated implementation work.

Do not perform broad/global path replacements in the root README. Do not replace the whole file merely because one link, path or statement became stale.

Treat the existing wording, tone, jokes, pacing, whitespace, visual separators, section ordering, legal framing and closing text as intentional editorial choices.

### Required editorial structure

Preserve this high-level structure unless the repository owner explicitly asks to change it:

1. **Legal/disclaimer header** — project independence / Wizards of the Coast and trademark framing at the top.
2. **Friendly human-facing section** — approachable explanation of what the project is, why it is interesting and how it feels to use; this is the primary public face of the repository.
3. **Quick start** — concise installation/start instructions written for a normal user.
4. **Intentional visual separation** before the technical-interest section.
5. **`Подробности для нёрдов` section** — conceptual architecture and implementation-relevant explanation for technically interested readers, but still written as readable public documentation rather than internal engineering notes.
6. **License / third-party legal footer and friendly closing sign-off**.

The nerd section may explain concepts such as GAME/DEV separation, storage, releases and high-level architecture, but it must not become a dump of internal technical debris: no audit logs, CI minutiae, debugging history, temporary implementation details, maintenance-process chatter, low-level agent workflow, internal checklists or other material that belongs under `DEV/`.

### Technical changes do not automatically authorize README edits

If a technical change makes a README statement, path or link inaccurate, **report the exact mismatch to the repository owner instead of silently rewriting the README**.

Only edit the root README when the repository owner explicitly asks for, or explicitly approves, a README change as part of the current task. When such an edit is authorized:

- make the **smallest targeted patch** needed;
- preserve the surrounding voice, structure, formatting and editorial rhythm;
- do not use the opportunity to rewrite adjacent text;
- keep the friendly section friendly and the nerd section readable;
- do not introduce internal implementation clutter merely because it is technically accurate.

Direct edits made by the repository owner to `README.md` are authoritative. Do not revert them to an older version, regenerate them from another source or "restore" a previous agent-authored variant unless explicitly asked.

The root README is **not machine-authoritative metadata**. Detailed architecture, release policy, tests, implementation plans and maintenance procedures belong under `DEV/`; runtime contracts belong under `GAME/`. The README should summarize only what is useful to human readers.

## Superpowers artifacts

All Superpowers research, design and implementation artifacts for this repository are development-only.

Use only:

```text
DEV/docs/superpowers/research/
DEV/docs/superpowers/specs/
DEV/docs/superpowers/plans/
```

Placement semantics:

- `research/` — non-normative research, reconnaissance, evidence gathering and feasibility-study artifacts that have not entered an approved design/specification chain;
- `specs/` — architecture/design, review, decision and canonicalization-chain artifacts;
- `plans/` — implementation plans produced after approved designs.

Do **not** create repository-root `docs/superpowers/` or repository-root `docs/` for Superpowers work. Historical research/specs/plans that are moved into DEV remain historical records; do not mechanically rewrite old path references when they describe the historical state accurately.

## Transient development branches in documentation

The active development branch/ref is session-specific repository state, not architecture semantics.

Do not write transient feature/research branch names into durable architecture, status, roadmap, contract, research, specification or implementation-plan documents as `Target`, `Target branch`, `Target development branch`, or equivalent working metadata. Determine the active ref from the repository at work time instead.

Record an exact branch/ref only when that identity is itself material evidence needed to reproduce or interpret a historical experiment, Git operation, release/provenance event, migration, comparison or failure. Accurate historical provenance must not be rewritten merely because later work moved to another branch.

## Branch creation guardrail

Remote branch creation is **prohibited by default**.

Never create a branch for probing, discovery, existence checks, temporary work, no-op operations, tool testing, recovery, uncertainty resolution, or as a substitute for a read-only ref query.

Never create disposable or placeholder branches with names such as `temp-*`, `do-not-use`, `noop`, `no-op`, `stop`, `scratch`, `test`, `ignore-me`, or equivalent variants.

A remote branch may be created only when the repository owner has explicitly requested a new branch or has explicitly approved the **exact branch name and exact base ref** for the current task.

Before any remote branch-creation action, the agent must state the exact intended branch name and base ref and obtain explicit owner approval. A general request to modify files, continue development, work on the current branch, or inspect repository state is not branch-creation approval.

If the connected GitHub interface does not expose remote ref deletion, branch creation must be treated as effectively irreversible for the session. This makes branch creation an especially high-risk write and never an acceptable experiment or discovery operation.

Use read-only operations for branch/ref discovery and verification, including branch search, current-file reads on a named ref, commit/ref comparison, and other Connector read surfaces. A create/write operation must never be used to answer a read-only question.

When an active development branch/ref is already specified, all ordinary reads and writes remain on that ref unless the repository owner explicitly changes the target.

For the current HDM rearchitecture program, the active development target is `v1/engine-rearchitecture`. Do not create another branch unless the repository owner explicitly requests or approves it under the rule above.

## GitHub transport policy

For HDM development in ChatGPT Work / Codex environments with connected GitHub Connector access:

```text
NATIVE_GIT_REMOTE = NATIVE_GIT_UNAVAILABLE
GITHUB_REMOTE_TRANSPORT = CONNECTOR_REQUIRED
```

Use the connected GitHub Connector for all remote repository communication: refs, commits, trees, blobs, files, comparisons, branch updates, pull requests and issues.

Do not use native Git/GitHub CLI/direct HTTP as a fallback for remote transport in this environment. In particular, do not run `git clone`, `git fetch`, `git pull`, `git push`, `git ls-remote`, `gh ...`, curl/Python HTTP credential workarounds or SSH/token bypasses.

If the Connector lacks a required capability, report that specific capability gap rather than bypassing it.

## Local Git is allowed

When a valid local checkout is already available, local-only Git operations are allowed, including status/diff/log/show/rev-parse/merge-base/merge/rebase/cherry-pick/add/restore/checkout/commit, provided they do not contact a remote.

A local commit is not proof that GitHub changed.

## Remote state is authoritative

Before a correctness-sensitive remote write, read the current target ref through the Connector. Construct the intended commit from that verified parent, update the ref without force unless explicitly required, then verify the remote ref again.

For multi-file/structural changes prefer Connector Git-data publication:

```text
read current ref
-> create UTF-8 blobs / reuse existing blob+tree SHAs
-> create tree from verified parent tree
-> create commit with expected parent
-> non-force update ref
-> verify ref/tree
```

## Text-file transport policy

For repository text files, use Connector UTF-8 text interfaces directly. Do not manually Base64-encode/decode Markdown, JSON, YAML, Python, configuration or other semantic text for transport, chunking, staging, reconstruction or verification.

Connector-internal Base64 required by GitHub APIs is allowed; agents must not add a redundant manual text→Base64→text layer. Explicit Base64 is reserved for genuinely binary content or a Connector operation with no usable text mode.

## Version metadata

- `DEV/ENGINE_DEVELOPMENT.yaml` is the complete development/release bookkeeping record.
- `GAME/ENGINE_VERSION.yaml` is the minimal installed-package/runtime projection.
- Shared fields must stay equal; builder/audit enforce this.
- `ENGINE_VERSION.yaml` must remain unique in the tracked repository so runtime package-root discovery is unambiguous.

Runtime GAME files read package metadata only from package-root `ENGINE_VERSION.yaml`; they never read DEV metadata.

## Development tools

Canonical DEV entry points:

```text
DEV/TOOLS/run_maintenance_audit
DEV/TOOLS/run_release_build.py
```

Both own/reuse the isolated repository-local `.hdm-devtools/` environment declared by `DEV/TOOLS/requirements-dev-tools.txt`. Do not install DEV dependencies into system Python and do not make GAME/runtime depend on them.

`GAME/TOOLS/init_campaign.py` is runtime support and remains Python-standard-library-only.

## Release boundary

`DEV/TOOLS/run_release_build.py` is the single authority for runtime package validation/composition, deterministic ZIP creation, asset naming and checksum creation. GitHub Actions must not maintain a second include/exclude list or duplicate builder dependency logic.

The supported install artifact is `hedgelion-dnd-master-runtime-v<version>.zip`. GitHub-generated source archives are repository snapshots and are not gameplay packages.

## GitHub Actions execution surface

GitHub-hosted Actions is a different execution surface from connector-backed ChatGPT/Codex. A release workflow may use its scoped `GITHUB_TOKEN` and GitHub-provided tooling/API to create a Release and upload the builder-produced assets. This does not relax Connector-only remote transport for interactive development sessions.

Release assets for an immutable tag are immutable: never silently overwrite different bytes under the same tag/asset name.

## Development versus gameplay

Development instructions, tests, release policy, catalogs under DEV and maintenance tooling must never be copied into gameplay prompts or runtime CORE context. GAME runtime behavior is defined only by the installed package and campaign storage contracts.

## Delegated-task prompt discipline

Standing project rules belong in repository instructions and process owners, not in every delegated task prompt.

When one development agent delegates work to another agent/chat/session:

- assume the worker will perform the required fresh-session bootstrap and read the current `AGENTS.md` plus applicable process files;
- do **not** repeatedly paste transport policy, branch-creation rules, evidence/completeness rules, decision-rights rules, repository ownership geometry, Superpowers requirements, or the generic checkpoint protocol when the repository already owns them;
- make the delegated message carry the **task-specific delta**: exact goal, expected current ref/cursor when useful, task-specific owning artifacts, concrete task-local constraints, material stop conditions, and required return evidence;
- restate a standing rule only when the current task introduces an exception, a narrower task-specific interpretation, or a known failure mode that makes the generic rule insufficiently precise;
- use concrete public repository terminology. Do not depend on private audit shorthand, metaphors, or labels that the worker cannot recover from the public repository sources.

A delegated prompt must remain sufficient to identify the requested work, but it should not become a second copy of `AGENTS.md` or the design-process documents. Repository-owned standing instructions are the durable/canonical place for recurring agent behavior.

## Coherent checkpoint commit discipline

For any large or interruption-prone development/implementation task, **do not wait until the entire assignment is finished before publishing progress** when a coherent verified slice is already complete.

The required pattern is:

```text
fresh current remote state
-> complete one coherent slice
-> run the focused verification that proves that slice
-> inspect the delta for partial migration / scope creep
-> commit
-> publish on the active ref without force
-> remote read-back
-> continue from the published HEAD
```

A slice is checkpoint-ready only when:

1. it is internally coherent and follows current owners;
2. its relevant focused tests/validation pass, or any unavailable verification is explicitly recorded rather than silently treated as PASS;
3. the published repository is not intentionally left in a broken or half-migrated contract state;
4. the checkpoint does not leave parallel old/new authority, partially synchronized identity carriers, producer/generated-artifact disagreement, or another state that necessarily requires hidden uncommitted work to be valid;
5. another agent could safely continue from that published HEAD without reconstructing hidden conversation-local work.

Good checkpoint boundaries include a complete schema+producer+test change, one fully synchronized migration, one independently complete implementation-plan task, one reconciled failure class, one coherent machine-contract realization, one completed evidence slice, or one status/canonicalization synchronization.

Do **not** create artificial micro-commits after arbitrary file counts or time intervals. Coherence and recoverability define the boundary.

### Interruption / exhaustion behavior

If context, message, credit, execution-time, or other practical limits are approaching:

```text
finish the nearest safe coherent slice
-> verify
-> publish
-> remote read-back
-> record exact continuation state
```

The continuation state should identify at least:

```text
LAST_PUBLISHED_SHA
COMPLETED_SLICES
CURRENT_VERIFICATION_STATE
NEXT_EXACT_TASK_OR_SLICE
KNOWN_BLOCKERS
UNPUBLISHED_WORK: NONE | exact description
```

If unfinished local work is in an unsafe midpoint and cannot be published coherently, explicitly identify the last safe published SHA and the unpublished state. Do not imply that uncommitted/chat-local work is durable project state.

Durability of completed work is part of execution quality. A long task may therefore produce several good commits before its final task-level completion claim.