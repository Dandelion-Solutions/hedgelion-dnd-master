# HDM Development Agent Instructions

## Scope

This file governs **development work on the HDM engine repository**. It is not part of gameplay/runtime instructions and is never shipped in the runtime release asset.

## Repository ownership geometry

The source repository has two product ownership trees:

- `GAME/` — exact source tree of the installed runtime distribution. The release builder archives the **contents** of this directory.
- `DEV/` — architecture, tests, release policy, development catalogs/schemas, Superpowers artifacts and developer tooling.

Repository root is reserved for repository infrastructure/metadata such as `.github/`, this `AGENTS.md`, root `README.md`, `.gitignore` and canonical legal files.

Do not recreate old repository-root product/development directories such as `CORE/`, `TESTS/`, `TOOLS/`, `ARCHITECTURE/`, `RELEASE/`, `CATALOG/`, `SCHEMA/`, `SCHEMAS/`, `CAMPAIGN/`, `TEMPLATE/`, `MIGRATIONS/`, `INSTALL/` or `docs/`.

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
DEV/TOOLS/run_release_build
```

Both own/reuse the isolated repository-local `.hdm-devtools/` environment declared by `DEV/TOOLS/requirements-dev-tools.txt`. Do not install DEV dependencies into system Python and do not make GAME/runtime depend on them.

`GAME/TOOLS/init_campaign.py` is runtime support and remains Python-standard-library-only.

## Release boundary

`DEV/TOOLS/run_release_build` is the single authority for runtime package validation/composition, deterministic ZIP creation, asset naming and checksum creation. GitHub Actions must not maintain a second include/exclude list or duplicate builder dependency logic.

The supported install artifact is `hedgelion-dnd-master-runtime-v<version>.zip`. GitHub-generated source archives are repository snapshots and are not gameplay packages.

## GitHub Actions execution surface

GitHub-hosted Actions is a different execution surface from connector-backed ChatGPT/Codex. A release workflow may use its scoped `GITHUB_TOKEN` and GitHub-provided tooling/API to create a Release and upload the builder-produced assets. This does not relax Connector-only remote transport for interactive development sessions.

Release assets for an immutable tag are immutable: never silently overwrite different bytes under the same tag/asset name.

## Development versus gameplay

Development instructions, tests, release policy, catalogs under DEV and maintenance tooling must never be copied into gameplay prompts or runtime CORE context. GAME runtime behavior is defined only by the installed package and campaign storage contracts.
