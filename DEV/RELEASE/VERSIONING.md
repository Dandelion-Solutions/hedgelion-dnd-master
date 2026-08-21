# Versioning

This policy is for engine/framework development. It is not a gameplay rule.

## Engine releases

The engine release version uses two numeric components with an optional prerelease suffix, for example `v0.8`, `v0.9-RC`, or `v1.5`.

`DEV/ENGINE_DEVELOPMENT.yaml` is the canonical development/release bookkeeping record. `GAME/ENGINE_VERSION.yaml` is the installed-package projection; all shared fields must match and are enforced by builder/audit.

Git tags are immutable release/reference points and use the exact `recommended_tag` spelling. Untagged commits on `main` are development state and MUST NOT be offered to campaigns as normal updates.

`release_status` remains meaningful development-package bookkeeping, but it is not a tag-publication gate. For an untagged build, `release_status: development` produces development package identity `dev-v<engine_version>` and runtime use remains subject to the development-package authorization gate. A tag-mode build is authorized by the tag itself: it must be a valid version tag, equal `recommended_tag`, correspond to `v<engine_version>`, resolve to the exact checked-out commit, and satisfy release-lineage validation. No manual `ready-for-tag` transition is required.

A correctly tagged package has release provenance from the immutable tag even when the source-tree status remains `development`; this does not weaken the separate authorization rules for untagged development packages.

Published provenance comes from exact tag identity/commit resolution. The tagged tree is not mutated afterward merely to change release status.

A release intended for campaign integration declares `campaign_update.compatibility` in both version manifests:
- `compatible` — normal automatic integration may proceed when runtime safety checks pass;
- `maintenance_required` — bounded campaign maintenance/migration is required.

Missing/unknown compatibility metadata is treated conservatively as maintenance-required.

## CORE module versions

CORE/runtime modules use `MAJOR.MINOR.REVISION`.

- `MAJOR.MINOR` records the engine major/minor version in which that module was last materially changed.
- `REVISION` is a monotonically increasing counter belonging only to that module.
- A new module starts at revision `1` under the current engine major/minor.
- Each later logical change increments its revision exactly once.
- If the engine version changes but the module does not, the module version does not change.
- On the next module change, update `MAJOR.MINOR` to current engine major/minor and increment the existing revision.
- Updating the version header as part of the same logical edit is metadata, not an additional revision.

Prerelease suffixes belong to the engine release/tag, not module versions.

## Independent revisions

Schema versions, launcher revisions, format revisions and similar compatibility counters remain independent integers unless their own specification says otherwise. Full revision bookkeeping lives in `DEV/ENGINE_DEVELOPMENT.yaml`; runtime GAME metadata does not carry development-only revision counters.