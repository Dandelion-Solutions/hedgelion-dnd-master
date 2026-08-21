# HDM Development Agent Instructions

## Scope

This file governs **development work on the HDM engine repository**. It is not part of gameplay/runtime instructions and is never shipped in the runtime release asset.

## Development design process

Before architecture, system design, deep technical research, or other development work whose scope may affect architecture:

1. read and follow `DEV/DESIGN_PROCESS.md`;
2. for HDM architecture work, also read and follow `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

`DEV/DESIGN_PROCESS.md` is the canonical general development/design process. `DEV/ARCHITECTURE/DESIGN_PROCESS.md` is the project-specific HDM adapter and adds constraints; it does not replace or weaken the general process.

Do not rely on remembered versions of these rules. Read the current files on the active branch before substantive architecture/deep-work activity.

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

All Superpowers design and implementation artifacts for this repository are development-only.

Use only:

```text
DEV/docs/superpowers/specs/
DEV/docs/superpowers/plans/
```

Do **not** create repository-root `docs/superpowers/` or repository-root `docs/` for Superpowers work. Historical specs/plans that are moved into DEV remain historical records; do not mechanically rewrite old path references when they describe the historical state accurately.

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
