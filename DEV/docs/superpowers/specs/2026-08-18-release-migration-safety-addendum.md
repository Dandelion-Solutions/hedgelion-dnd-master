# Release Migration Safety Addendum

Status: written-spec review addendum; implementation pending final approval.

This addendum supplements the GAME/DEV boundary design and its risk-audit amendment with release-pipeline and migration-atomicity findings discovered during the same pre-implementation review.

## 1. The structural migration is one coherent tree transition

The GAME/DEV split moves or deletes a large fraction of the tracked repository tree while simultaneously changing active path references, development tools and release contracts.

Do not publish the migration as a long sequence of remote commits that leave the feature branch temporarily half-moved, for example `CORE/` already moved while `TESTS/` and audit tooling still expect it at root.

The final structural cutover should be represented as one coherent Git tree transition (or the smallest possible tightly coupled commit set where every intermediate commit is deliberately valid). Prefer one atomic structural commit constructed from the verified parent tree:

- reuse existing blob bytes and executable modes for pure moves;
- create new blobs only for files whose contents actually change;
- place moved blobs at their GAME/DEV destinations;
- omit/delete old root paths in the same resulting tree;
- add new workflow/build files in that tree;
- update the feature ref once, non-force, from the verified parent.

This preserves byte identity for pure moves and avoids an intermediate remote state that neither the old nor the new audit can understand.

The Connector-only remote transport and no-manual-Base64 rules remain unchanged.

## 2. Shared self-provisioning DEV tool environment

The release entry point must own its prerequisites. GitHub Actions should not contain hidden knowledge such as `pip install PyYAML` before calling the builder.

Generalize the current maintenance-only environment into a DEV-tools environment shared by maintenance audit and release build tooling.

Recommended source layout:

```text
DEV/TOOLS/
  run_maintenance_audit.py
  run_release_build
  audit_engine.py
  release_builder.py
  dev_tool_environment.py
  requirements-dev-tools.txt
```

Exact internal filenames may vary during the implementation plan, but the public entry-point contracts are:

```text
DEV/TOOLS/run_maintenance_audit.py
DEV/TOOLS/run_release_build
```

Both entry points provision/reuse the same isolated repository-local DEV environment and then invoke their internal tool. The pinned DEV requirements initially include at least:

- `jsonschema` for the maintenance/schema audit;
- `PyYAML` for robust release/version-manifest parsing.

The repository-local cache should use a purpose-accurate name such as:

```text
.hdm-devtools/
```

rather than `.hdm-maintenance/` once it serves more than maintenance auditing. The cache and build output remain ignored and outside GAME.

The environment fingerprint continues to depend on exact requirements bytes plus bootstrap Python major/minor, preserving the current reproducibility behavior.

GAME/runtime remains dependency-free with respect to these DEV packages. `GAME/TOOLS/init_campaign.py` stays Python-standard-library-only.

## 3. GitHub Action calls exactly one release build entry point

The tag workflow should know only repository checkout, Python setup, the tag context and the canonical release entry point.

Conceptually:

```text
checkout exact tag
setup supported Python
DEV/TOOLS/run_release_build --tag <exact tag> --output <ci output dir>
publish builder-produced assets
```

It must not independently install builder-specific Python packages, decide which GAME paths to include, compute package names from duplicate rules, or run a parallel set of package validations.

The release entry point owns environment preparation, validation, deterministic archive creation and checksum generation.

## 4. Release-status semantics must be explicit

The current release lifecycle sets `release_status: ready-for-tag` before creating the immutable tag. Because the tagged tree is immutable, a successful published asset built from that tag will naturally still contain `ready-for-tag`; there is no legitimate post-tag source mutation that can turn the same tagged bytes into `published`.

Therefore define the current meanings explicitly:

- `development` — local development package; owner-only explicit framework testing; not a normal player release;
- `ready-for-tag` — release-candidate tree eligible to be tagged and, once the exact recommended tag exists, a normal published package.

Published provenance is established by exact tag identity/resolution, not by mutating `release_status` after publication.

For a tag-triggered release build the builder must require:

- DEV/GAME shared status values agree;
- `release_status == ready-for-tag`;
- passed tag exactly equals `recommended_tag`;
- tag/version naming is coherent with `engine_version` under the versioning policy.

A tag workflow must reject `release_status: development` rather than accidentally publishing an owner-only dev package as a player release.

Runtime bootstrap continues to special-case `development`. A tag-backed `ready-for-tag` package is treated as the normal published-package path.

## 5. Pre-tag local verification and tag build must use the same code path

The team needs to validate the final runtime archive before creating a tag, but tag-triggered CI must rebuild the same bytes after the tag exists.

The canonical release entry point should therefore support validating/building an intended release tag from the ready-for-tag checkout even before that Git ref exists remotely. In local/pre-tag mode it validates the supplied intended tag against `recommended_tag` but does not require remote tag existence.

After the exact commit is tagged, GitHub Actions invokes the same entry point with the actual tag. Deterministic output means the CI-built runtime ZIP must be byte-identical to the pre-tag candidate built from the same tree and parameters.

This avoids having one "test packaging" implementation and a different "real release" implementation.

## 6. Asset naming is derived once

Asset naming belongs to the canonical release builder/entry point, not to the workflow.

For 0.8 the expected runtime asset is:

```text
hedgelion-dnd-master-runtime-v0.8.zip
```

The implementation must derive the name from validated release metadata/tag so future prerelease suffixes or version changes do not require editing the workflow separately.

The checksum sidecar, if produced, is named from the exact runtime asset in the same build result.

## 7. File modes are part of the structural move

Pure moves should preserve Git modes. In particular:

- `GAME/TOOLS/init_campaign.py` remains executable in the source tree;
- DEV launcher entry points remain executable;
- ordinary Markdown/YAML/JSON files remain ordinary non-executable files.

The deterministic ZIP may normalize archive permission metadata deliberately, but the repository migration itself should not accidentally lose executable modes.

Runtime correctness must not rely solely on the executable bit for Python scripts because the documented runtime can invoke them through Python, but mode preservation is still required repository hygiene.

## 8. Active DEV links need validation too

The original design correctly distinguishes package-relative GAME links and destination-relative campaign/storage links. The source split also moves active development documents deeper under `DEV/`, so relative links in active architecture/release/test documentation can break even though runtime packaging passes.

Maintenance audit should validate local relative links for current/active DEV documentation against the new source tree. Historical specs/audits are exempt when their old paths are intentional historical content; the checker must use explicit active/history scope rather than globally rewriting or rejecting every old-looking string.

The root `README.md` is active and must have its repository-browser links updated to source-tree destinations such as `GAME/INSTALL/...`, `GAME/CORE/...` and `DEV/TESTS/...`.

## 9. Release object creation is idempotent but assets are immutable

The tag workflow may encounter either:

- no GitHub Release object yet for the tag; or
- an already-created Release object for that exact tag.

The publishing step should use get-or-create semantics for the Release object without creating duplicates.

For the runtime asset itself, immutable-tag integrity rules from the risk-audit amendment apply: an existing identical asset is a successful idempotent rerun; an existing same-name asset with different bytes is a hard error and must not be overwritten.

## 10. Runtime ZIP shape is part of package identity

Merely finding an `ENGINE_VERSION.yaml` recursively is not sufficient to accept an installation archive.

After the GAME/DEV source split, GitHub's automatic Source code ZIP will itself contain `GAME/ENGINE_VERSION.yaml`. If startup recursively selects that directory as engine root, the unsupported source archive can accidentally remain bootable while DEV material is physically present in the same uploaded Project Source. That defeats the structural isolation goal.

Therefore Project Instructions/bootstrap package selection must validate the selected ZIP as a runtime-distribution archive before treating it as an engine package.

For the custom runtime asset:

- `ENGINE_VERSION.yaml` is a direct top-level ZIP member;
- `CORE/`, `INSTALL/`, `RULES/` and other required package trees are top-level siblings;
- there is no top-level `GAME/` or `DEV/` source-tree wrapper;
- the archive name follows the runtime-asset naming contract;
- the runtime marker/version manifest validates.

Do not recursively descend through an arbitrary source archive until an `ENGINE_VERSION.yaml` happens to be found and then reinterpret that nested directory as a valid release package.

GitHub Source code archives must fail this package-shape validation even if they contain a perfectly valid source-tree `GAME/` subtree.

This validation happens against ZIP member layout before or as part of extraction. After a validated runtime asset is extracted, ordinary package-root paths remain unchanged.

## 11. Release tags must come from the supported release lineage

A matching `v*` tag name and ready-for-tag metadata alone should not allow an accidental feature-branch commit to become the canonical public engine release.

The tag-triggered release workflow/builder must verify that the tagged commit belongs to the supported release lineage, normally the repository default branch (`main`). It may be the current main HEAD or an ancestor intentionally tagged as a release, but it must be reachable from the authoritative release branch according to the release policy.

This is a release-provenance check, not package-composition logic, and belongs in the canonical release validation path.

In GitHub Actions the checkout must provide enough local history/ref information for this validation, or the entry point must receive equivalent authoritative context. This scoped use of repository history inside GitHub Actions does not alter the Connector-only transport rule for ChatGPT/Codex development sessions.

## 12. Additional regression coverage

Add tests/checks for:

- structural cutover produces no half-old/half-new tracked root geometry;
- pure moved files retain expected bytes and executable modes unless intentionally edited;
- DEV tool environment provisions both jsonschema and YAML parsing through one self-owned entry-point mechanism;
- GitHub workflow contains no package dependency-install/composition knowledge beyond invoking the release entry point;
- tagged release build rejects `development` status;
- `ready-for-tag` + exact recommended tag is accepted as the normal published package path;
- pre-tag candidate and tag-triggered build from the same tree/parameters are byte-identical;
- asset filename comes from builder output rather than duplicated workflow string logic;
- current active DEV/root relative links resolve after the move;
- GitHub Source code ZIP shape is rejected even though it contains `GAME/ENGINE_VERSION.yaml`;
- custom runtime ZIP requires direct top-level package marker and package trees;
- release tag commit is reachable from the supported release branch before asset publication.
