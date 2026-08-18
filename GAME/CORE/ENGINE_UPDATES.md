# Engine Runtime Updates

framework_module_version: 0.9.1
load_when: campaign/storage startup, explicit engine-update request, runtime mismatch, safe maintenance opportunity

## Distribution model

Gameplay engine bytes come only from validated local D&D Master runtime assets supplied through Project Sources/current-chat attachments.

A package has three distinct identities:
- `ENGINE_VERSION.yaml` — semantic engine contract;
- `RUNTIME_PACKAGE.yaml` — provenance of the exact built package source state;
- final ZIP SHA-256 — exact artifact/cache identity.

Campaign storage contains no engine copy. GitHub release/tag metadata may assist discovery/provenance comparison, but it never installs engine files.

GitHub-generated `Source code (zip)` / `Source code (tar.gz)` archives are source snapshots and are **not runtime installation artifacts**; they MUST NOT be accepted as runtime packages.

## Portable runtime authorities

Two durable engine authorities are deliberately independent:

```text
DND_STORAGE.engine.baseline
    storage-owner default runtime for NEW campaigns only

MANIFEST.engine.current
    runtime identity currently adopted by THIS campaign
```

`current_runtime_root` is a third, ephemeral local cache binding and is never durable authority.

### Campaign authority

The **campaign creator** controls semantic engine-version adoption for that campaign branch. Creator identity is derived from the first campaign-specific initialization commit; it is not inferred from generic repository Write/Admin permission and is not replaced by storage ownership.

A non-creator may use a compatible forward same-version runtime refresh as defined below, but may not persist campaign engine-identity changes.

### Storage authority

Only the authenticated **storage owner** may persist `DND_STORAGE.engine.baseline` changes on the storage default branch.

Storage owner and campaign creator authority are independent. Updating storage baseline does not migrate existing campaigns. Updating one campaign does not change storage baseline or sibling campaigns.

## Update opportunities

Maintenance is event-driven, never per-turn polling. Consider runtime updates/refreshes at startup/resume, explicit update request, package mismatch, or another safe maintenance opportunity.

Do not repeatedly poll GitHub during ordinary turns.

Before package selection, cheaply index available local runtime ZIP metadata. A newer semantic version may be offered based on semantic `ENGINE_VERSION.engine_version` comparison alone; source-SHA archaeology is NOT required merely to decide that 0.8 is newer than 0.7.

## Creator prompt for a newer semantic version

When all of the following are true:
- selected campaign currently uses semantic version C;
- a validated local runtime ZIP with newer semantic version T is available;
- authenticated user is the campaign creator;
- the `(campaign_identity, target_engine_version)` prompt is not currently suppressed;
- asking does not interrupt a higher-priority unresolved operation;

with `update_policy: ask`, offer exactly these meanings:

1. **Update now** — adopt target semantic version T through normal authorized maintenance.
2. **Remind later** — suppress this same target-version prompt for 24 hours in the current environment, then re-evaluate at the next natural startup/maintenance opportunity.
3. **Do not remind about this version** — suppress this target semantic version for this campaign for the lifetime of the current environment.

Logical ephemeral key:

```text
(campaign_identity, target_engine_version)
```

The reminder/suppression state is **ephemeral convenience state**. It MUST NOT be written to campaign Git, storage Git, ChatGPT Memory, engine files, or any other durable canon.

`Remind later` is not a background timer/automation. If no interaction occurs, nothing runs. Once at least 24 hours have elapsed, the prompt becomes eligible again at the next normal check.

If the environment disappears, reminder/suppression state may disappear too. The question may then reappear; that is acceptable.

Suppression is target-version-specific. Suppressing 0.8 does not suppress a future 0.9 offer.

A non-creator is never offered semantic-version migration authority for somebody else's campaign.

`update_policy: auto`, when explicitly configured by authorized campaign creator, may adopt a newer semantic version only when all compatibility, durability, concurrency and maintenance gates allow it. Human-required migration decisions still block automatic adoption.

## Same-version runtime refresh

A package with the same semantic `engine_version` and same logical `package_id` as `MANIFEST.engine.current` is not a semantic-version upgrade.

Within one semantic version, a proven forward source revision is treated as a compatible cosmetic/maintenance **same-version refresh** under this contract and does not require a player prompt.

Candidate provenance MUST use `RUNTIME_PACKAGE.source_commit_sha` from the candidate ZIP itself. Do not infer the candidate's source SHA solely from the current position of a mutable tag.

Let campaign-recorded source commit be A and candidate package source commit be B.

Classify with **one bounded server-side compare** between A and B. Do not enumerate commit history.

- A == B and package digest matches -> exact accepted artifact.
- A == B and package digest differs -> suspicious repack/non-deterministic artifact; do not silently substitute it.
- A is ancestor of B -> proven forward same-version refresh; silently prefer B.
- B is ancestor of A -> downgrade candidate; do not silently use it.
- A and B diverged -> ambiguous replacement; do not arbitrarily order or silently choose it.
- ancestry unavailable because provenance SHA is null -> only exact accepted digest is automatically reusable; different bytes require explicit authorized handling.

"Newer SHA" means descendant commit proven by ancestry. Never order raw SHA text or timestamps.

### Candidate preference

For candidates matching current semantic `version` + `package_id`:
1. validate package shape, `ENGINE_VERSION.yaml`, `RUNTIME_PACKAGE.yaml` and digest;
2. identify the exact accepted digest if present;
3. identify proven descendant candidates from recorded `MANIFEST.engine.current.source_commit_sha`;
4. if one candidate is the unambiguous newest descendant/tip among usable same-version candidates, **silently prefer** that forward candidate even when the old exact-digest ZIP is still available;
5. otherwise reuse exact accepted digest when available;
6. never silently choose an ancestor/downgrade;
7. never silently choose between diverged candidates without a unique forward result.

This prevents an obsolete exact ZIP from permanently pinning a campaign to an earlier cosmetic build of the same semantic version.

### MANIFEST refresh after silent forward use

A proven forward same-version runtime may be used immediately without player confirmation.

If authenticated user is campaign creator, refresh these fields at the next otherwise-valid coherent campaign persistence transaction:

```text
MANIFEST.engine.current.source_commit_sha
MANIFEST.engine.current.package_sha256
MANIFEST.engine.current.adopted_at
```

This provenance refresh MUST NOT create a standalone cosmetic commit merely to record the same-version package change.

If current user is a **non-creator**, the compatible forward same-version runtime may still be used for play, but MANIFEST remains unchanged because that user lacks authority to persist campaign engine identity. A later creator session may refresh stale provenance at a normal coherent boundary.

## Storage baseline same-version refresh

The same forward-versus-downgrade classification applies when resolving `DND_STORAGE.engine.baseline` for New Game.

A proven descendant package within the same baseline semantic version/package identity may be used for a new campaign without treating it as a semantic-version migration.

Only storage owner may persist refreshed baseline `source_commit_sha`, `package_sha256`, and `adopted_at`. Do not create a storage metadata write merely from a non-owner session.

## Semantic-version adoption

A true semantic-version change modifies the selected campaign's `MANIFEST.engine.current`, not engine files in campaign storage.

Before creator-authorized adoption:
- resolve/validate the exact target runtime ZIP and artifact provenance;
- satisfy compatibility/migration rules declared by the target package for the currently supported schema;
- persist any gameplay state that must become durable before maintenance;
- ensure no blocking concurrent/live operation;
- establish the campaign known frontier and use `PERSISTENCE.md` transport discipline;
- never force-push.

Prepare the complete authorized campaign metadata/data delta coherently and publish it under the campaign persistence contract. `MANIFEST.engine.created_with` remains immutable. Update only `engine.current` plus data/schema state genuinely required by the target runtime.

This implementation cycle does not invent backward migration from retired pre-v3 engine-identity fields.

## Storage baseline semantic update

Storage baseline semantic-version change is a separate storage-owner metadata transaction. It changes the default for future New Game only.

If both storage baseline and one campaign are intentionally updated, they remain separate authorities and separate durable transactions. Success/failure of one does not imply rollback or mutation of the other.

## Package mismatch recovery

A package mismatch is not automatically a terminal failure. Missing extracted cache is not package mismatch: if the required ZIP bytes exist, cache can be reconstructed silently.

### Required current-version package is available

If a valid package for `MANIFEST.engine.current.version` is present in Project Sources/current-chat attachments, resolve candidate provenance/digest under the exact/same-version rules above, then **reuse or silently re-extract** its isolated cache and continue. Missing/expired local extraction requires **no player prompt**.

If a newer semantic-version ZIP also exists, creator update prompting may still happen under the normal semantic-version policy, but declining/postponing that offer does not invalidate the available current-version package.

### Required current-version package is absent; user is not campaign creator

The user lacks authority to change this campaign's semantic engine version. Tell them to **add the matching `hedgelion-dnd-master-runtime-v<version>.zip`** to Project Sources or the current chat, then automatically resume resolution once it becomes available.

The runtime MUST NOT offer semantic-version migration of another creator's campaign. A newer ZIP being available does not substitute for the campaign's missing current-version runtime.

### Required current-version package is absent; user is campaign creator

Offer the creator the valid alternatives rather than a dead-end refusal:

1. **Restore/add the campaign's current runtime version** by adding its matching runtime ZIP and continue unchanged. This is **preferred when one Project intentionally contains campaigns on different engine versions**.
2. **Update the campaign to an available newer semantic version** through the normal authorized semantic-version maintenance flow, including compatibility/durability gates and the configured update prompt policy.

If no newer valid runtime is available, only the restore/add-current-version path is offered.

Never silently run a proven downgrade or a different semantic version merely because it is the only extracted package.

The player-facing response MUST NOT stop at "cannot continue" when one of the above recovery actions exists. State what package/version is needed and present only actions the current user is authorized to take.

## Runtime switch discipline

When the selected exact package changes:
1. satisfy required durability boundary before maintenance;
2. validate/reuse/extract exact target ZIP in its isolated version+digest cache;
3. atomically bind new `current_runtime_root`;
4. invalidate entire old CORE instruction cache;
5. preload COMPLETE target `CORE/*.md` + `RULES/INDEX.md` + `RULES/README.md` from the new root once;
6. never adjudicate with mixed old/new runtime roots.

After semantic-version adoption, update `CAMPAIGN_CARD.engine_version` in the same campaign transaction as authoritative engine-version change.

Never claim update success before required GitHub publication succeeds. Technical maintenance must not fabricate fictional elapsed time/events.
