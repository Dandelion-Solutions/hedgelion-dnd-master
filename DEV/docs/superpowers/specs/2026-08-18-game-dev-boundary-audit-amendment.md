# GAME / DEV Boundary Risk-Audit Amendment

Status: design amendment discovered during written-spec review; implementation pending final spec approval.

This document amends `2026-08-18-game-dev-release-boundary-design.md` and `2026-08-18-engine-version-split-amendment.md`. It records non-obvious failure modes found while auditing the current repository before implementation.

## 1. Superpowers artifacts are DEV-only

Superpowers defaults to repository-root `docs/superpowers/specs/` and `docs/superpowers/plans/` unless repository/user instructions override it. Merely moving the current directory does not change future behavior.

After migration, root `AGENTS.md` must explicitly override the artifact locations:

```text
DEV/docs/superpowers/specs/
DEV/docs/superpowers/plans/
```

It must explicitly forbid creating repository-root `docs/superpowers/`.

The maintenance audit must enforce this. Repository-root `docs/` must not silently reappear as a second development-document branch. Existing `docs/superpowers/**` moves intact under `DEV/docs/superpowers/**` during the migration.

Historical specs/plans are records of the state and decisions that existed when written. They must not be mechanically rewritten merely to make old prose describe the new layout. New active documents use current paths; historical documents may intentionally mention old paths. Path-validation rules must distinguish active contracts from historical design records.

## 2. Unique runtime package marker

There must be exactly one tracked file named `ENGINE_VERSION.yaml`: `GAME/ENGINE_VERSION.yaml`.

The DEV superset is therefore named `DEV/ENGINE_DEVELOPMENT.yaml`, not `DEV/ENGINE_VERSION.yaml`. This prevents package-root discovery from becoming ambiguous in a development checkout containing both GAME and DEV.

Project Instructions continue to locate a package root by the unique `ENGINE_VERSION.yaml` marker. In a source checkout that resolves to `GAME/`; in an extracted runtime asset it resolves to archive root.

## 3. Repository-root geometry is intentional

After migration, ordinary product/development content belongs under exactly one of the two ownership trees:

```text
GAME/
DEV/
```

Repository infrastructure remains at root only when it must or should be repository-scoped, including:

- `.github/` (GitHub requires workflow placement there);
- `AGENTS.md`;
- root `README.md`;
- `.gitignore` and similar repository configuration;
- canonical repository legal files and `LICENSES/`.

The maintenance audit must reject accidental reappearance of old root content branches such as `CORE/`, `TESTS/`, `TOOLS/`, `ARCHITECTURE/`, `RELEASE/`, `CATALOG/`, `SCHEMA/`, `SCHEMAS/`, `CAMPAIGN/`, `TEMPLATE/`, `MIGRATIONS/` or `docs/`.

This is a source-organization guard, not a release include list. The release builder still packages the entire contents of GAME.

## 4. Developer tools need three explicit roots

Current maintenance tools derive `ROOT` as the parent of root-level `TOOLS/`. That assumption breaks after moving them to `DEV/TOOLS/`.

Development tooling must distinguish explicitly:

```text
REPO_ROOT
DEV_ROOT = REPO_ROOT / "DEV"
GAME_ROOT = REPO_ROOT / "GAME"
```

`DEV/TOOLS/run_maintenance_audit`, `DEV/TOOLS/audit_engine.py`, their Python tests, and the release builder must use the correct root for each operation instead of overloading one `ROOT` variable.

The repository-local maintenance cache may remain at `REPO_ROOT/.hdm-maintenance/`.

Current path-sensitive tests must be migrated too. In particular, `TESTS/test_run_maintenance_audit.py` currently derives root from its own old location and builds temporary `TOOLS/` trees; the migrated test must model the new DEV layout deliberately rather than accidentally passing against the old geometry.

## 5. GAME runtime must not know DEV tree names

Physical separation should simplify runtime instructions rather than preserve a textual denylist for files that no longer ship.

Current `CORE/PLAY_POLICY.md` names `ARCHITECTURE/`, `RELEASE/`, `TESTS/` and `TOOLS/audit_engine.py` as things not to use during gameplay. After migration those development paths do not exist in the runtime package.

The 0.8 GAME runtime should express a positive package/runtime contract:

- CORE is the behavior instruction set;
- RULES routing files are preloaded and exact rule records are targeted;
- SCHEMA is a targeted data contract;
- CAMPAIGN/TEMPLATE/INSTALL/MIGRATIONS are used only at their specific setup/install/update boundaries;
- GAME/TOOLS contains only runtime tools and each is invoked only from its owning runtime procedure.

Do not teach GAME about `DEV/`, `DEV/TOOLS/audit_engine.py`, `DEV/TESTS/` or other development-only paths merely to say they are forbidden. Structural absence is the stronger firewall.

The maintenance audit must be rewritten accordingly; its current checks that demand development-directory names inside PLAY_POLICY become invalid after separation.

## 6. Runtime package metadata has one authority

Runtime identity fields in package-root `ENGINE_VERSION.yaml` are authoritative for package version/source/owner/compatibility.

Current runtime Markdown duplicates some of these values, for example canonical repository and owner fields in bootstrap/runtime headers. The migration must remove duplicate machine-authoritative metadata where the same value can be read from `ENGINE_VERSION.yaml`.

Human-facing prose may still name the public project repository when useful, but runtime behavior must not depend on two independently maintained copies of repository/owner/version metadata.

The builder/audit must also validate obvious duplicated runtime defaults that must stay coherent with the package manifest, including campaign scaffold `schema_version` and default `rules.baseline` unless a future schema explicitly defines a different relationship.

## 7. Template validation uses destination semantics

The release audit must model both source and destination layouts.

Examples:

```text
GAME/TEMPLATE/STORAGE_README.md -> storage-root README.md
GAME/CAMPAIGN/README.md         -> campaign-root README.md
GAME/CAMPAIGN/MANIFEST.yaml     -> campaign-root MANIFEST.yaml
```

Relative Markdown links in copied files are resolved against the destination tree. The checker must ignore external URL schemes and anchors appropriately, reject accidental `GAME/` or `DEV/` source prefixes, detect path escape outside the destination root, and verify exact path casing where the referenced destination exists.

Validation should not be limited to Markdown links when a generated YAML field is explicitly a path. Known scaffold path fields such as house-rules/storage roots must be checked against the generated campaign layout or approved future writable locations.

Package-local Markdown links that are not copied to campaign storage are instead validated against the extracted GAME/package layout.

## 8. Duplicated installation instructions must remain identical

`INSTALL/README.md` currently embeds a full copy of the Project Instructions while `INSTALL/PROJECT_INSTRUCTIONS.txt` stores the same contract separately.

Because 0.8 changes release-asset wording and package discovery, editing only one copy would create a subtle installation split-brain.

The builder/maintenance audit must compare the embedded Project Instructions block in `GAME/INSTALL/README.md` with `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` after deterministic newline normalization. They must fail on semantic/text drift.

The root repository README is a third, shorter installation description. It does not need byte equality, but release audit must ensure it no longer instructs users to install GitHub-generated Source code archives and that its links resolve to the new source-tree locations under GAME.

## 9. All Source-code-ZIP installation language must be migrated

The current repository has Source-code-ZIP assumptions in several independent places, including:

- root `README.md`;
- `INSTALL/README.md`;
- `CORE/ENGINE_UPDATES.md`;
- `RELEASE/CHECKLIST.md`;
- related regression cases.

All active installation/update/release contracts must switch to the custom runtime asset. GitHub's automatic `Source code (zip)` / `Source code (tar.gz)` remain source snapshots only and must be explicitly described as unsupported installation artifacts where user confusion is likely.

The runtime asset uses an unambiguous runtime-specific filename such as:

```text
hedgelion-dnd-master-runtime-v0.8.zip
```

Project Instructions should identify a candidate package by runtime asset naming plus valid package marker/content, not by a broad filename pattern that could accidentally match an unrelated/source archive.

## 10. Builder YAML parsing is a DEV dependency

The release builder must parse DEV/GAME YAML reliably to validate shared metadata and tag coherence. Python standard library has no YAML parser.

Do not implement an ad-hoc partial YAML parser merely to preserve a dependency-free builder.

A pinned development-only YAML dependency such as PyYAML is acceptable. It must live under DEV tooling/environment and never enter GAME/runtime requirements.

The implementation plan may either:

- extend the canonical maintenance/dev environment to include the YAML parser and run the builder through that environment; or
- define a small separate release-tool environment/launcher.

Prefer one shared DEV tooling environment unless isolation provides a concrete benefit.

## 11. Build output must never contaminate GAME

The canonical builder must reject an output directory located inside `GAME/`. Otherwise a local build could place an earlier ZIP inside GAME and recursively package it on a subsequent build.

Use a repository-local ignored build area such as `.hdm-release/` for local builds, or an explicitly supplied external/temp output directory in CI.

Update `.gitignore` for development-generated state, including the chosen release output/cache and ordinary Python caches (`__pycache__/`, `*.pyc`, test cache if introduced).

The builder should reject unclean package artifacts inside GAME such as Python bytecode/cache directories, editor/OS junk and prior build archives. Approved scaffold placeholders such as `.gitkeep` remain allowed.

## 12. Archive safety and cross-platform determinism

Because GAME is archived wholesale, release validation must guard filesystem edge cases rather than rely on a hand-maintained include list.

At minimum:

- reject symlinks inside GAME unless a future explicit design adds supported symlink semantics;
- reject archive paths that are absolute or contain traversal components;
- detect case-insensitive path collisions that would extract ambiguously on Windows/macOS-like filesystems;
- use normalized forward-slash ZIP member names;
- sort members deterministically;
- normalize ZIP timestamps/metadata sufficiently for reproducible output;
- ensure archive root contains GAME contents directly and no top-level GAME wrapper.

## 13. GitHub Actions is a different remote-transport environment

Root `AGENTS.md` correctly forbids `git`/`gh` remote transport for ChatGPT Work/Codex connector-backed development. A GitHub-hosted Actions runner is a different execution surface with its own scoped `GITHUB_TOKEN`.

The migration must clarify this distinction so the new release workflow is not accidentally interpreted as violating the development-agent transport policy.

The Actions workflow may use GitHub's authenticated release API or an appropriate trusted/official mechanism to create/update the Release and upload the builder-produced asset. This exception is scoped to GitHub Actions execution and does not relax Connector-only remote transport for ChatGPT/Codex development sessions.

The workflow itself remains thin and contains no package-composition logic.

## 14. Tagged runtime assets are immutable release objects

A workflow rerun for an already-created immutable tag must not silently replace a different runtime ZIP with `--clobber`-style behavior.

The builder must produce deterministic bytes and compute a SHA-256 digest for the runtime ZIP. Publishing logic must treat the tag + asset name as immutable identity:

- if no runtime asset exists, publish the builder output;
- if the same asset already exists and its bytes/digest are identical, the rerun may succeed without mutation;
- if the same asset name exists with different bytes, fail the release job and surface an integrity error rather than overwrite it.

A checksum sidecar or equivalent recorded digest is acceptable and recommended if it simplifies verification. The checksum is release metadata produced by the canonical builder/publish flow, not a second package-composition authority.

## 15. Maintenance audit must change semantics, not only paths

Current `audit_engine.py` contains assumptions that become wrong after migration:

- it looks for runtime CORE/SCHEMA/CAMPAIGN at repository root;
- it looks for development CATALOG/SCHEMAS/TESTS at repository root;
- it requires development-only names to appear in PLAY_POLICY;
- it requires the deprecated `TEMPLATE/CAMPAIGN_MANIFEST.yaml` stub to exist;
- its generator smoke test hardcodes `dev-v0.7`;
- it launches root `TOOLS/init_campaign.py` with repository root as source root.

The 0.8 audit must instead understand GAME and DEV as separate source trees, require the deprecated stub to be absent, derive the smoke-test engine identity from current GAME metadata, and run the exact `GAME/TOOLS/init_campaign.py` with GAME as source root.

The audit must additionally verify the final built archive, not merely the source tree.

## 16. MIGRATIONS documentation contains stale engine-tree semantics

Current `MIGRATIONS/README.md` says migrations are needed when a normal merge of `main` into a campaign branch is insufficient. This contradicts the current runtime model: campaign updates migrate campaign data/metadata; engine files are local-package content and are not merged/copied into campaign branches.

Before shipping MIGRATIONS in GAME 0.8, rewrite this README to match current update semantics. This is a real runtime-documentation correction, not merely a path rename.

## 17. Historical records versus active regression contracts

Some DEV files are historical artifacts, for example old pre-release audit records and prior Superpowers specs/plans. Global search-and-replace would corrupt their historical meaning.

Implementation must classify documents before rewriting:

- active source code, active regression tests, current architecture/release policy and current instructions are migrated to new paths/contracts;
- historical records may move under DEV but retain historical old-layout references when those references describe what actually happened;
- automated stale-path checks must not treat intentional historical quotations as active broken contracts.

If a historical document is currently mixed into an active-test directory in a way that makes classification ambiguous, move it into an explicit history/archive subdirectory under DEV rather than silently rewriting history.

## 18. Legal-file duplication is validated, not trusted

Repository-root legal files remain canonical repository material and equivalent copies ship under GAME for the standalone runtime distribution.

Release validation must compare root and GAME copies byte-for-byte (or exact normalized text only if a concrete newline policy is intentionally adopted) and fail on mismatch. Package-local notice references such as `LICENSES/SRD-5.2.1-ATTRIBUTION.md` must resolve within the extracted runtime tree.

## 19. Required 0.8 migration regression coverage

In addition to the original design tests, add regression checks for:

- no repository-root `docs/` after migration;
- root AGENTS forces future Superpowers output to DEV paths;
- unique tracked `ENGINE_VERSION.yaml` marker;
- explicit REPO_ROOT/DEV_ROOT/GAME_ROOT behavior in developer tools;
- no DEV-only path names or maintenance tools referenced by GAME runtime policy as runtime-visible files;
- Project Instructions README block matches the canonical text file;
- no active docs tell players to use GitHub Source code ZIP as the engine package;
- release output cannot be placed inside GAME;
- GAME contains no symlinks, build junk or cross-platform case collisions;
- package-relative and destination-relative links are validated in their correct namespaces;
- deprecated campaign-manifest stub is absent;
- MIGRATIONS documentation matches data-migration-only engine update semantics;
- GitHub Actions workflow invokes the canonical builder and does not duplicate package composition;
- repeated publication for the same immutable tag cannot replace a different runtime asset;
- extracted custom runtime asset passes bootstrap/package discovery and campaign-generator smoke tests.
