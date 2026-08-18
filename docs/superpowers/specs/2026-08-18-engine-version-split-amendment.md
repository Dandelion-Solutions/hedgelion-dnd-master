# Engine Version Split Amendment

Status: approved design amendment; implementation pending final written-spec review.

This document amends `2026-08-18-game-dev-release-boundary-design.md` for engine-version metadata only. All other approved GAME/DEV release-boundary decisions remain unchanged.

## Goal

Split the current repository-root `ENGINE_VERSION.yaml` into two consumer-owned files after the GAME/DEV migration:

- `DEV/ENGINE_VERSION.yaml` — complete development/release bookkeeping superset;
- `GAME/ENGINE_VERSION.yaml` — minimal installed-package/runtime projection.

As part of the same migration, raise the HDM engine version from `0.7` to `0.8`. The new GAME/DEV physical boundary and custom runtime-release format therefore debut as engine `0.8`, not as an in-place restructuring of `0.7`.

The runtime must never read version or compatibility metadata from `DEV/`. Development/release validation must ensure that shared fields in the two files remain coherent.

## DEV version file

`DEV/ENGINE_VERSION.yaml` retains the complete content model of the current `ENGINE_VERSION.yaml`. No current metadata is discarded merely because it is not needed by gameplay.

Its responsibilities include:

- engine version/release bookkeeping;
- repository/source identity;
- development-owner identity;
- rules/schema version metadata;
- all current module/layout/format/revision counters;
- campaign-update compatibility metadata;
- recommended release tag.

The current fields therefore remain valid in DEV, including all `*_revision` counters and `consistency_audit_revision`.

The migration changes the shared release identity fields to:

```yaml
engine_version: 0.8
recommended_tag: v0.8
```

`release_status` remains governed by the existing release lifecycle; this layout migration does not by itself falsely mark an unreleased development tree as published.

Development tooling, release policy, maintenance audit and repository-facing documentation that need the complete bookkeeping record must read `DEV/ENGINE_VERSION.yaml`.

## GAME runtime projection

`GAME/ENGINE_VERSION.yaml` contains only package/runtime identity and compatibility fields needed by installed HDM behavior:

```yaml
engine_version: 0.8
release_status: development
repository: Dandelion-Solutions/hedgelion-dnd-master
engine_owner_login: dkolyada
rules_baseline: D&D 2024 / SRD 5.2.1
schema_version: 2
campaign_update:
  compatibility: maintenance_required
recommended_tag: v0.8
```

The GAME file must not contain development-only revision counters such as:

- `ai_reasoning_revision`;
- `gm_craft_revision`;
- `install_layout_revision`;
- `branch_id_revision`;
- `access_control_revision`;
- `storage_format_revision`;
- `presentation_revision`;
- `persistence_revision`;
- `campaign_card_revision`;
- `mechanics_integrity_revision`;
- `character_readiness_revision`;
- `save_contract_revision`;
- `campaign_identity_revision`;
- `runtime_scope_revision`;
- `consistency_audit_revision`.

## Runtime consumers

After the split, installed/runtime instructions must read only package-root `ENGINE_VERSION.yaml`, which corresponds to source-tree `GAME/ENGINE_VERSION.yaml` and becomes archive-root `ENGINE_VERSION.yaml` in the release asset.

Runtime uses include:

- locating/validating the package root;
- reading `engine_version`;
- distinguishing published versus authorized development packages with `release_status`;
- resolving the canonical engine repository from `repository`;
- development-package authorization using `engine_owner_login`;
- rules/schema compatibility metadata from `rules_baseline` and `schema_version`;
- campaign-update gating through `campaign_update.compatibility`;
- published-package identity through `recommended_tag`.

Bootstrap/setup/update documents inside GAME must continue referring to package-root `ENGINE_VERSION.yaml`, never `GAME/ENGINE_VERSION.yaml`.

Where bootstrap currently duplicates the canonical engine repository as a hardcoded `engine_repository` value, the migration should prefer `ENGINE_VERSION.repository` as the package-owned source of that identity and remove unnecessary duplicate authority when safe.

## Development consumers

Repository development/release material must refer explicitly to `DEV/ENGINE_VERSION.yaml` when it needs the full metadata/revision record.

Examples include:

- release/versioning policy;
- maintenance audit;
- revision-counter consistency checks;
- development documentation that describes the repository bookkeeping record.

A development test that is specifically validating installed-package behavior may instead inspect `GAME/ENGINE_VERSION.yaml`; the consumer determines which file is correct.

## Shared-field coherence

The following fields exist in both files and must be equal:

- `engine_version`;
- `release_status`;
- `repository`;
- `engine_owner_login`;
- `rules_baseline`;
- `schema_version`;
- `campaign_update.compatibility`;
- `recommended_tag`.

For this migration, both files must therefore report `engine_version: 0.8` and `recommended_tag: v0.8`.

`DEV/ENGINE_VERSION.yaml` is the development/release superset. `GAME/ENGINE_VERSION.yaml` is the runtime projection used by the installed package.

The canonical release builder and maintenance audit must fail if any shared field differs. They must also fail if GAME unexpectedly contains a development-only revision field.

This avoids silent drift while preserving a clean runtime package.

## Module-version policy during the 0.8 migration

Raising the engine version to `0.8` does not mass-rewrite version headers of otherwise unchanged CORE modules.

Follow the existing versioning policy:

- a runtime/CORE module materially changed by this migration updates its module `MAJOR.MINOR` to `0.8` and increments that module's own revision exactly once;
- an unchanged module keeps its existing module version even though the engine moves to `0.8`;
- path-only relocation without a semantic change does not manufacture an unrelated revision unless the file's actual contract/text must change.

Installation/bootstrap/update modules whose behavior or release-asset references change as part of this migration are treated as materially changed and versioned accordingly.

## Builder behavior

`DEV/TOOLS/build_release.py` must:

1. read `DEV/ENGINE_VERSION.yaml` for full release/development bookkeeping;
2. read `GAME/ENGINE_VERSION.yaml` for the exact runtime manifest that will ship;
3. validate shared-field equality;
4. validate tag/release coherence using the appropriate shared release fields;
5. package only `GAME/ENGINE_VERSION.yaml` as archive-root `ENGINE_VERSION.yaml`;
6. never include `DEV/ENGINE_VERSION.yaml` in the runtime ZIP.

The GitHub Action remains unaware of this field split beyond invoking the builder.

## Migration of references

The implementation must audit every current `ENGINE_VERSION.yaml` reference and classify it by consumer rather than applying one global replacement.

Rules:

- runtime/package instructions inside GAME keep `ENGINE_VERSION.yaml`;
- development/release instructions become `DEV/ENGINE_VERSION.yaml` when they require the full record;
- source-tree development tests that inspect the runtime package use `GAME/ENGINE_VERSION.yaml`;
- build/release tooling may read both files for coherence validation;
- no gameplay instruction may refer to `DEV/ENGINE_VERSION.yaml`.

## Tests

Regression coverage must verify at least:

- DEV version file contains all current bookkeeping/revision fields;
- GAME version file contains exactly the approved runtime projection fields;
- both files report engine `0.8` and recommended tag `v0.8`;
- shared fields are identical;
- runtime ZIP includes only archive-root `ENGINE_VERSION.yaml` derived from GAME;
- runtime bootstrap/setup/update paths continue to resolve package-root `ENGINE_VERSION.yaml`;
- development revision checks read DEV rather than GAME;
- GAME contains no development-only revision counters;
- changing a shared field in only one file makes builder/audit fail.
