# Versioning

This policy is for engine/framework development. It is not a gameplay rule.

## Engine releases

The engine release version uses two numeric components with an optional prerelease suffix, for example `v0.1-beta`, `v0.2-RC`, or `v1.5`.

`ENGINE_VERSION.yaml` is the canonical in-repository release-version record. Git tags are immutable release/reference points and use the exact tag spelling chosen for that release.

Do not update unrelated files merely because the engine release/tag changed.

## CORE module versions

CORE/runtime modules use `MAJOR.MINOR.REVISION`.

- `MAJOR.MINOR` records the engine major/minor version in which that module was last materially changed.
- `REVISION` is a monotonically increasing counter belonging only to that module.
- A new module starts at revision `1` under the current engine major/minor.
- Each later logical change to that module increments its revision exactly once.
- If the engine version changes but the module does not, the module version does not change.
- On the next module change, update `MAJOR.MINOR` to the current engine major/minor and increment the existing module revision.
- Updating the version header as part of the same logical edit is metadata, not an additional revision.
- A correction that changes only version metadata does not increment the module revision.

Existing modules adopt revision `1` as the baseline when this policy is introduced; pre-policy history is not backfilled.

Prerelease suffixes such as `beta` or `RC` belong to the engine release/tag, not to module versions.

## Independent revisions

Schema versions, launcher revisions, format revisions and similar compatibility counters remain independent integers unless their own specification says otherwise.
