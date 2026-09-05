# Engine Runtime Updates

framework_module_version: 1.1.1
load_when: campaign/storage startup, explicit engine-update request, runtime mismatch, safe maintenance opportunity

## Distribution model

Gameplay engine bytes come only from validated local D&D Master runtime assets supplied through Project Sources/current-chat attachments.

A package has three distinct identities:

- `ENGINE_VERSION.yaml` — semantic engine contract;
- `RUNTIME_PACKAGE.yaml` — provenance of the exact built package source state;
- final ZIP SHA-256 — exact artifact/cache identity.

Campaign storage contains no engine copy. GitHub release/tag metadata may assist discovery/provenance comparison, but it never installs engine files and never substitutes for immutable package-carried compatibility evidence.

GitHub-generated `Source code (zip)` / `Source code (tar.gz)` archives are source snapshots and are **not runtime installation artifacts**; they MUST NOT be accepted as runtime packages.

## Compatibility horizon

Released-campaign compatibility begins at **released HDM v1.0+**.

Pre-release/v0.8 campaign layouts, schemas and package identities are not part of the supported compatibility horizon merely because historical documentation mentions them.

Version/generation/source ordering does not manufacture compatibility. For released packages:

```text
same engine_version
same package_id
source commit ancestry
```

are not sufficient compatibility proof for different artifact bytes.

Exact digest equality proves the exact previously accepted artifact. Different released bytes require affirmative compatibility support from the exact candidate package. Git ancestry remains provenance evidence only.

## Portable runtime authorities

Two durable engine authorities are deliberately independent:

```text
DND_STORAGE.engine.baseline
    storage-owner default runtime for NEW campaigns

MANIFEST.engine.current
    runtime identity currently adopted by THIS campaign
```

`current_runtime_root` is a third, ephemeral local cache binding and is never durable authority.

### Campaign authority

The **campaign creator** controls semantic engine/ruleset adoption and migration for that campaign branch. Creator identity is derived from the first campaign-specific initialization commit; it is not inferred from generic repository Write/Admin permission and is not replaced by storage ownership.

A non-creator may use a different exact runtime artifact only when current compatibility evaluation affirmatively proves `DIRECT_COMPATIBLE` or another owner-permitted non-adopting maintenance state and no creator-owned MANIFEST/native-state mutation is required.

### Storage authority

Only the authenticated **storage owner** may persist `DND_STORAGE.engine.baseline` changes or execute an explicitly supported storage-format migration on the storage-default authority.

Storage owner and campaign creator authority are independent. Updating storage baseline/storage format does not migrate existing campaigns. Updating one campaign does not change storage baseline, storage format or sibling campaigns.

If storage evolution is a prerequisite to campaign migration, the two remain separate transactions and success domains.

## Update opportunities

Maintenance is event-driven, never per-turn polling. Consider runtime updates/refreshes at startup/resume, explicit update request, package mismatch, or another safe maintenance opportunity.

Do not repeatedly poll GitHub during ordinary turns.

Before exact package selection, cheaply index available local runtime ZIP metadata. Semantic engine-version comparison may be used only to identify a **candidate update opportunity**. It does not prove direct compatibility or a migration path.

## Creator prompt for a newer semantic version

When all of the following are true:

- selected campaign currently uses semantic version C;
- a validated local runtime ZIP with newer semantic version T is available;
- authenticated user is the campaign creator;
- the `(campaign_identity, target_engine_version)` prompt is not currently suppressed;
- asking does not interrupt a higher-priority unresolved operation;

with `update_policy: ask`, offer these meanings:

1. **Update now** — evaluate and, if supported, adopt target T through normal authorized maintenance/migration.
2. **Remind later** — suppress this same target-version prompt for 24 hours in the current environment, then re-evaluate at the next natural maintenance opportunity.
3. **Do not remind about this version** — suppress this target semantic version for this campaign for the lifetime of the current environment.

Logical ephemeral key:

```text
(campaign_identity, target_engine_version)
```

The reminder/suppression state is ephemeral convenience state. It MUST NOT be written to campaign Git, storage Git, ChatGPT Memory, engine files or migration evidence.

`Remind later` is not a background timer/automation. If no interaction occurs, nothing runs. Once at least 24 hours have elapsed, the prompt becomes eligible again at the next normal maintenance check.

If the environment disappears, reminder/suppression state may disappear too. The question may then reappear; this is acceptable.

Suppression is target-version-specific. Suppressing one released target does not suppress a later released target.

A non-creator is never offered semantic-version migration authority for somebody else's campaign.

`update_policy: auto`, when explicitly configured by the authorized campaign creator, may adopt a target only when compatibility classification, migration path, durability, LIVE/currentness, accepted-work and publication gates all authorize it. `INDETERMINATE` or `UNSUPPORTED_INCOMPATIBLE` never auto-adopts.

## Compatibility evaluation

For one selected campaign and one exact target runtime, evaluate a bounded owner-composed compatibility evidence envelope including applicable:

```text
pinned campaign HEAD/currentness
campaign current engine + campaign-contract identity
exact current package provenance/digest
exact current ruleset-set identity + compatibility evidence
relevant persistent/protocol schema versions
storage format as a separate prerequisite axis
accepted resumable-work compatibility
LIVE ownership/absorption state
exact target package compatibility/migration support
```

The result is one of:

```text
DIRECT_COMPATIBLE
MAINTENANCE_REFRESH
MIGRATION_REQUIRED
UNSUPPORTED_INCOMPATIBLE
INDETERMINATE
```

Coarse `ENGINE_VERSION.campaign_update.compatibility` may route maintenance evaluation but is not complete proof.

### DIRECT_COMPATIBLE

Target affirmatively supports the source without authoritative persistent transformation.

### MAINTENANCE_REFRESH

Only owner-permitted nonsemantic/rebuildable/local maintenance is required. This is not implicit creator-owned adoption.

### MIGRATION_REQUIRED

An explicit directed migration path is required and supported by the exact target package.

### UNSUPPORTED_INCOMPATIBLE

Required source/contract/accepted-work state is unsupported or required immutable support material is absent.

### INDETERMINATE

Evidence/currentness/path selection is ambiguous or insufficient. Fail closed and re-evaluate when evidence changes; do not guess.

## Same-version provenance candidate ordering

A package with the same semantic `engine_version` and logical `package_id` is not automatically compatible with different released bytes. The following rules are **candidate provenance/order rules only**; they never replace the compatibility classification above.

Candidate provenance MUST use `RUNTIME_PACKAGE.source_commit_sha` from the candidate ZIP itself. Do not infer a candidate source SHA solely from the current position of a mutable tag.

Let campaign-recorded source commit be A and candidate package source commit be B. One bounded server-side compare is sufficient to classify ancestry; do not enumerate commit history.

- A == B and exact package digest matches -> exact accepted artifact.
- A == B and digest differs -> suspicious repack/non-deterministic artifact; different released bytes still require affirmative compatibility evidence.
- A is ancestor of B -> forward same-version provenance candidate.
- B is ancestor of A -> downgrade candidate; do not silently use it.
- A and B diverged -> ambiguous replacement; do not arbitrarily order it.
- provenance ancestry unavailable -> exact accepted digest remains the only automatically exact artifact.

When several same-version candidates are being considered for **compatibility evaluation**, an unambiguous newest descendant may be silently preferred as the candidate to evaluate, rather than repeatedly evaluating an older descendant. `silently prefer` here does not authorize use: different released bytes still require `DIRECT_COMPATIBLE` or another owner-permitted classification before binding.

If an exact different candidate is affirmatively classified as owner-permitted `MAINTENANCE_REFRESH`/`DIRECT_COMPATIBLE` and creator-owned persistent identity does not need to change, it may be used under that classification. If creator-owned MANIFEST provenance is eligible for a coherent refresh, that refresh MUST NOT create a standalone commit merely to record cosmetic/provenance information; it joins the next otherwise-valid coherent campaign transaction.

A non-creator never gains creator-owned MANIFEST/adoption authority from ancestry, direct compatibility or repository permission.

## Migration path discipline

Migration support is exact-target-package-scoped immutable support data.

A path exists only through explicit directed migration edges. Engine-version order, generation/schema order, Git ancestry, timestamps or lexical order never create an edge.

When several valid edge compositions remain, use only a canonical path/order explicitly declared by the exact target package. If no such declaration resolves ambiguity, classification is `INDETERMINATE`.

A reverse/downgrade transition requires its own explicit reverse edge/path. A prior checkpoint, old ref or older package is not generic rollback authority.

## Campaign migration prerequisites

Before creator-authorized campaign migration:

1. resolve/validate the exact target runtime artifact and its immutable compatibility/migration support;
2. pin exact current campaign HEAD and required independently writable owner currentness;
3. establish a clean recovery-safe durable frontier as required by persistence owners;
4. require no active LIVE-selected mutable authority for affected state;
5. require no CLOSED LIVE state awaiting required absorption/reconciliation;
6. prove the exact target can interpret all current accepted resumable-work closure under frozen causal/ruleset/package/RNG/provenance semantics;
7. satisfy any separately owned storage-format prerequisite;
8. select one deterministic explicit migration path when transformation is required.

If any required currentness changes during preparation, discard/re-evaluate. Never merge a prepared migration onto a moved campaign head and never force-push.

Accepted work MUST NOT be rebound to new ambient rules, rerolled, silently discarded or reconstructed from hidden model reasoning merely to permit an update.

## Migration transformation scope

Migration changes only declared campaign data/schema/native paths and allowed campaign identity/adoption projections.

Engine files are never copied or merged into campaign storage.

Preserve unrelated canon/history, stable IDs, creator/PLAYER authority, accepted execution identities/RNG evidence, truth/knowledge/disclosure separation, chronology, lifecycle, House Rules provenance and recovery semantics.

Required branch-persistent rebuildable indexes/projections may be rebuilt from the prepared migrated authoritative state when their owner permits it. Local HOT/SQLite/runtime caches do not participate in authoritative publication and are invalidated/rebuilt only after durable success.

## Authoritative migration publication

Prepare the complete authorized target campaign tree against pinned HEAD `H`, validate it, then publish only through the existing campaign persistence transaction:

```text
one prepared tree
-> one commit parented to H
-> one non-force campaign-ref CAS/update
```

Local transformation/validation success is only **PREPARED**.

- confirmed ref update -> durable migration/adoption success;
- rejected/ref-moved update -> current ref remains authority; migration did not happen;
- unknown transport result -> bounded authoritative ref read-back; never blind retry.

Prepared/unreachable Git objects do not become campaign authority.

Only after confirmed success may the runtime bind the exact target `current_runtime_root`, invalidate old engine/runtime caches and continue.

## Storage baseline and storage-format maintenance

Storage baseline semantic update changes the default runtime for **future New Game only**.

Storage-format migration belongs to the storage owner and separate storage migration support. It must not rewrite creator-owned campaign current identity as a hidden side effect.

If both storage and one campaign are intentionally updated, each operation reports its own outcome. Success/failure of one does not imply rollback or mutation of the other.

## Package mismatch recovery

A package mismatch is not automatically terminal. Missing extracted cache is not package mismatch: if the exact required ZIP bytes exist, cache can be reconstructed silently.

### Required current-version package is available

If a valid exact/current supported package for `MANIFEST.engine.current.version` is available, reuse or silently re-extract its isolated cache and continue. Missing/expired local extraction requires no player prompt.

If a different same-version artifact is available, it is evaluated under the exact-package compatibility rules above; ancestry alone is not permission to use different released bytes.

### Different candidate package is available

Do not use it merely because it has the same semantic version/package ID or a descendant source commit. Run current compatibility evaluation against the exact candidate.

- `DIRECT_COMPATIBLE` may be used within current authority rules;
- `MAINTENANCE_REFRESH` follows owner-permitted maintenance;
- `MIGRATION_REQUIRED` requires creator-authorized migration;
- `UNSUPPORTED_INCOMPATIBLE` is rejected;
- `INDETERMINATE` blocks until evidence/currentness is resolved.

### Required current-version package is absent; user is not campaign creator

The user lacks authority to change this campaign's semantic engine version. Tell them to add the matching `hedgelion-dnd-master-runtime-v<version>.zip` when that exact/current supported package is required.

The runtime MUST NOT offer semantic-version migration of another creator's campaign. A newer ZIP being available does not itself substitute for the campaign's required current-version runtime.

An alternative exact candidate may be used only if affirmative compatibility proves it can be used without creator-owned mutation.

### Required current-version package is absent; user is campaign creator

Offer valid recovery alternatives rather than a terminal refusal:

1. **Restore/add the campaign's current runtime version** by adding its matching runtime ZIP and continue unchanged. This is preferred when one Project intentionally contains campaigns on different engine versions.
2. **Update the campaign to an available newer semantic version** through the normal authorized compatibility/migration flow when the exact target supports it.

If no valid target update path exists, only the restore/add-current-version path remains.

Never silently run a downgrade, unsupported target or guessed substitute.

The player-facing response MUST NOT stop at a bare terminal refusal when a valid restore/update path exists.

## Gameplay continuation after maintenance

Maintenance during active gameplay is a transparent pause, not fictional elapsed time and not the end of the player's turn.

Before maintenance that may invalidate engine context, preserve the existing maintenance continuation frame under `SESSION.md`/recovery owners.

After confirmed success:

1. bind the exact target package;
2. invalidate the entire old engine instruction/runtime cache;
3. rebuild the complete target CORE/RULES runtime context required by current bootstrap rules;
4. restore the selected campaign working set from confirmed authoritative state;
5. remind the player who last said/did what using the strongest available evidence;
6. return to the same unresolved gameplay point without inventing events or verbatim history.

The runtime MUST NOT end the player-facing response with only a technical maintenance statement when gameplay can safely resume.

Never adjudicate with mixed old/new runtime roots.

## Unsupported newer state

An older runtime encountering a campaign/schema/ruleset/storage contract it does not explicitly support fails closed. Successful parsing, numeric decrement or guessed reverse migration is not compatibility.

## Migration evidence

Migration may persist bounded maintenance/audit/history evidence through an admitted owner, but that evidence is not publication authority.

Retain enough to identify source campaign basis, exact target package, selected ordered edge identities/artifacts, authorization basis and validation outcome. The resulting campaign ref/commit remains authoritative. Do not require a record inside a commit to self-embed its final containing commit SHA.
