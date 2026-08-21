# Multi-runtime cache and maintenance continuity design

Date: 2026-08-18
Status: approved design, implementation not started
Branch: `feature/mechanical-runtime-hot-state`

## 1. Purpose

D&D Master must support several runtime release ZIPs in one ChatGPT Project, because different campaign branches may legitimately require different engine versions at the same time.

Selecting a campaign with a different engine must not end in a dead-end refusal. The runtime must either resolve the required package automatically, or offer the player the smallest valid maintenance choice.

Engine maintenance must also preserve gameplay continuity: after a successful package refresh or campaign engine update, the Master returns to the same unresolved scene/decision point instead of ending the response with a technical status message.

This design also establishes a one-hour durability ceiling for dirty HOT/SOFT campaign state during active work.

## 2. Explicit non-goals

This change does NOT design or implement backward migration from the repository's current legacy campaign-manifest engine fields.

The owner will start new chats/campaigns on the new schema. Future updates are designed against the new model only.

This change does NOT persist extracted engine files in campaign storage, ChatGPT Memory, or the engine repository.

This change does NOT make local runtime-cache directories canonical. They are disposable acceleration only.

## 3. Runtime packages in Project Sources

Project Instructions must no longer require exactly one D&D Master runtime ZIP.

A Project MAY contain multiple supported runtime assets:

```text
hedgelion-dnd-master-runtime-v0.7.zip
hedgelion-dnd-master-runtime-v0.8.zip
...
```

GitHub-generated `Source code (zip)` / `Source code (tar.gz)` archives remain unsupported as runtime packages.

At new-chat startup the bootstrap SHOULD identify available supported runtime ZIPs cheaply, but MUST NOT eagerly extract every version.

The package initially used to bootstrap storage/campaign discovery is only a bootstrap host. Exact runtime ownership is resolved only after the user explicitly selects a campaign or New Game.

## 4. Lazy versioned runtime cache

Exact runtime packages are extracted lazily into a disposable current-session cache.

Logical layout:

```text
<session-cache>/hdm-runtime/
  <version>/
    <package_sha256>/
      ENGINE_VERSION.yaml
      CORE/
      INSTALL/
      RULES/
      SCHEMA/
      CAMPAIGN/
      TOOLS/
      ...
```

Example:

```text
<session-cache>/hdm-runtime/0.8/4f2c.../
```

`package_sha256` is the SHA-256 of the exact runtime ZIP bytes.

The cache is not durable state. If the environment is cleared, expires, or otherwise loses the extracted directory, bootstrap silently re-extracts the matching ZIP from Project Sources/current-chat attachment. The user is not asked to repair or recreate cache directories.

No extracted runtime package is ever copied into campaign GitHub storage.

## 5. `current_runtime_root`

After exact package resolution, the chat keeps one ephemeral binding:

```text
current_runtime_root = <session-cache>/hdm-runtime/<version>/<package_sha256>/
```

`current_runtime_root` is local current-chat state only. It MUST NOT be written into campaign MANIFEST, GitHub, ChatGPT Memory, or other durable canon because its filesystem path is environment-specific and disposable.

All package-relative runtime access after engine selection MUST resolve under `current_runtime_root` only.

This includes:

- `ENGINE_VERSION.yaml`;
- `CORE/`;
- `RULES/`;
- `SCHEMA/`;
- `CAMPAIGN/` and other templates;
- runtime `TOOLS/`;
- package-relative Markdown/resource links.

After selection, runtime code/instructions MUST NOT globally search for the first `ENGINE_VERSION.yaml`, `CORE/`, `TOOLS/init_campaign.py`, or another matching path anywhere in the working filesystem.

Sibling cached engine versions are inert while another `current_runtime_root` is active.

The existing package-link validation principle remains: package-relative references must stay within the selected package root and must not escape into another cached runtime.

## 6. Campaign runtime identity

Campaign runtime identity remains in root `MANIFEST.yaml`; no second root authority file is introduced.

The new canonical shape is:

```yaml
engine:
  created_with:
    version: "0.8"
    package_id: "v0.8"
    source_commit_sha: "<sha|null>"

  current:
    version: "0.8"
    package_id: "v0.8"
    source_commit_sha: "<sha|null>"
    package_sha256: "<sha256>"
    adopted_at: "2026-08-18T13:18:00+02:00"

  update_policy: ask
```

### 6.1 `created_with`

`created_with` is immutable creation provenance.

- `version` is the semantic engine version used to create the campaign.
- `package_id` is the logical package identity.
- `source_commit_sha` is the source commit for a published package when known.

`created_with` does not change on later refreshes or migrations.

### 6.2 `current`

`current` is the runtime identity currently required by the campaign.

- `version` is the semantic engine version.
- `package_id` is the logical package identity. Published packages normally use values such as `v0.8`; authorized development packages may use `dev-v0.8`.
- `source_commit_sha` is provenance for the source commit represented by the accepted package, nullable only where development-package rules explicitly allow it.
- `package_sha256` is the digest of the exact ZIP last accepted for this campaign.
- `adopted_at` records when the campaign accepted this runtime identity and is audit/debug metadata, not ordering authority.

The field name `source_commit_sha` replaces the misleading historical `integrated_main_sha`; runtime provenance is not semantically tied to a branch named `main`.

### 6.3 Package digest is not a permanent lock

`package_sha256` identifies the exact last accepted artifact and is used for cache identity and diagnostics.

It MUST NOT mean that the old ZIP must remain available forever.

A newer artifact with the same semantic version/package identity may replace it through the same-version refresh rules below.

## 7. Resolving the required package

After explicit campaign selection, bootstrap reads authoritative `MANIFEST.engine.current` and resolves available runtime ZIPs.

Resolution priority:

1. Exact `package_sha256` available -> use/reuse that package.
2. Exact digest unavailable, but a package with matching `version` + `package_id` exists -> classify it as same-version same-package candidate.
3. Matching logical package absent -> enter engine-mismatch UX.

If more than one different ZIP claims the same `version` + `package_id`, bootstrap MUST NOT select arbitrarily. Prefer an exact `package_sha256`; otherwise classify candidates using source provenance and require an unambiguous result or creator decision.

Every selected ZIP is validated for supported package shape before extraction/use.

## 8. Same-version runtime refresh versus downgrade

Changing artifact bytes while keeping the same semantic engine version is a runtime refresh, not automatically a version migration.

Given:

```text
campaign current source_commit_sha = A
candidate source_commit_sha = B
version/package_id are equal
```

perform one bounded server-side GitHub ancestry/compare operation. Do not enumerate commit history.

Classification:

- `A == B` -> same source revision; a different ZIP digest is suspicious and requires validation/explicit handling rather than silent substitution.
- A is ancestor of B -> forward same-version refresh.
- B is ancestor of A -> downgrade.
- A and B diverged -> ambiguous replacement.
- ancestry cannot be established -> do not infer direction from timestamps; require explicit creator decision unless the artifact digest is already the exact accepted digest.

Commit/adoption timestamps MAY be shown as diagnostics, but MUST NOT be authority for forward-versus-backward classification.

A successful forward refresh updates `engine.current.source_commit_sha`, `package_sha256`, and `adopted_at`.

A downgrade MUST NOT happen automatically.

For development packages whose `source_commit_sha` is legitimately null, different bytes under the same logical package identity cannot be ancestry-classified and require explicit authorized engine-owner acceptance unless the digest already matches.

## 9. Update policy and authority

### 9.1 Campaign authority

The creator of the specific campaign branch is the authority for changing that campaign's engine runtime identity.

Creator identity remains derived from Git history: the author login of the first campaign-specific initialization commit. It is not duplicated as authority in MANIFEST.

A storage repository owner does not automatically gain authority to migrate a campaign created by somebody else.

### 9.2 Storage authority

Only the storage owner may change storage-level metadata such as `DND_STORAGE.yaml -> engine.baseline_version`.

Storage baseline and campaign runtime identity are independent authorities.

Changing one does not imply permission or obligation to change the other.

### 9.3 `update_policy`

`update_policy: ask` means an available forward refresh/version update is offered to the campaign creator at a safe maintenance boundary.

`update_policy: auto` may accept a forward refresh/update only when all normal compatibility, concurrency, durability and authority gates pass.

Downgrades and ambiguous replacements are never silently auto-adopted.

## 10. Engine mismatch player experience

An engine mismatch is not a terminal refusal.

### 10.1 Required package already exists

If the selected campaign requires a package already present in Project Sources/current-chat attachment:

```text
resolve package
-> reuse/extract versioned cache
-> bind current_runtime_root
-> rebuild exact CORE cache if necessary
-> continue campaign
```

No user prompt is needed merely because extraction cache was absent.

### 10.2 Required package absent; current user is not campaign creator

Offer the valid path only:

- add the matching `hedgelion-dnd-master-runtime-v<version>.zip` to Project Sources/current chat;
- after it becomes available, resolve it and continue automatically.

Do not offer migration of another creator's campaign.

### 10.3 Required package absent; current user is campaign creator

Offer both valid alternatives:

1. Add/restore the exact required runtime version and continue the campaign unchanged. This is preferred when one Project contains campaigns intentionally pinned to different versions.
2. Update the selected campaign to an available newer compatible runtime and continue after successful maintenance.

The Master must not present package mismatch as "I cannot continue" without these alternatives.

## 11. Runtime switch discipline

When runtime identity changes in the current chat:

1. finish/publish any durability work required before maintenance;
2. resolve and validate the target ZIP;
3. extract/reuse its isolated cache directory;
4. bind new `current_runtime_root` atomically;
5. invalidate the entire old engine CORE context cache;
6. preload complete target `CORE/*.md` plus `RULES/INDEX.md` and `RULES/README.md` once;
7. ensure all subsequent runtime file resolution uses only the new root;
8. continue campaign maintenance/gameplay without mixed old/new engine instructions.

At no point may one logical adjudication use files from two runtime roots.

## 12. Maintenance continuation frame

Maintenance is a transparent pause in gameplay, not the end of the turn.

Before an engine refresh/update performed during an active campaign chat, capture a current-chat continuation frame containing the minimum evidence needed to return to the same point:

- selected campaign identity;
- last known durable campaign frontier;
- current scene/location identity already loaded;
- last meaningful player action/utterance relevant to the unresolved point;
- last meaningful Master/NPC utterance or outcome relevant to that point;
- unresolved player decision/action point, if any.

The continuation frame is current-chat working state, not automatically new campaign canon.

After successful maintenance and runtime switch:

1. restore/validate the selected campaign working set under the new engine;
2. apply the already-known post-maintenance campaign state;
3. briefly tell the player maintenance succeeded if that information is useful;
4. restore the gameplay situation;
5. remind the player who last said/did what and what remains unresolved;
6. continue from that exact decision point.

Do not end the response with only "campaign updated" / "state saved" when active gameplay can resume.

### 12.1 Evidence rules

If the exact previous utterance/action is still available in current chat context, it may be recalled accurately.

If current-chat context is unavailable, use durable checkpoint/state/event/log evidence.

Never fabricate an exact quote or action merely to make the resume feel seamless. When only a semantic durable summary exists, present it as a summary rather than invented verbatim dialogue.

Maintenance itself does not advance fictional time or create fictional events unless the campaign data migration explicitly and legitimately requires such a change.

## 13. HOT/SOFT durability ceiling

Disposable runtime cache and campaign HOT/SOFT state are separate concerns.

Runtime cache may disappear at any time because it can be reconstructed from immutable runtime ZIPs.

Dirty HOT/SOFT campaign state may represent unpublished canon and therefore needs a durability ceiling.

### 13.1 One-hour rule

During active campaign work, if unpublished dirty HOT/SOFT state exists, the durable campaign frontier MUST NOT remain older than one hour of wall-clock time without creating a forced durability boundary.

Conceptually:

```text
dirty_hot_or_soft == true
AND now - durable_frontier_time >= 1 hour
=> forced durability boundary
```

The rule is additive to existing event/domain durability rules. Critical events may still force publication immediately; ordinary batching may still publish earlier.

### 13.2 No meaningless heartbeat commits

If no dirty canonical campaign state exists, the one-hour rule MUST NOT create an empty/no-op commit merely to make the last commit recent.

### 13.3 Inactive chat limitation

The assistant does not run continuously while the user is absent.

If more than one hour passes while the chat is inactive, the next user interaction must first check whether dirty state survived in current context and whether the durable frontier became stale.

If dirty state exists and the ceiling was exceeded, publish the coherent dirty batch before applying a new gameplay action, subject to normal concurrency/authority checks.

If local/chat working state was lost entirely, recover from the latest durable campaign frontier and do not invent unpublished canon.

## 14. New-chat behavior

A new chat does not assume extracted runtime directories from any other chat survive.

New-chat startup:

1. discover storage/campaign menu without selecting a campaign implicitly;
2. index available supported runtime ZIPs without eagerly extracting all of them;
3. after explicit campaign/new-game selection, resolve `MANIFEST.engine.current` or selected storage baseline;
4. reuse a matching local extracted cache only if it actually exists and validates in this environment;
5. otherwise silently extract the required ZIP into a fresh isolated cache root;
6. bind `current_runtime_root` and preload exact CORE context.

Missing cache is normal and must not be surfaced as an error to the player.

## 15. New campaign creation

New campaigns created after this design use only the new `engine.created_with` / `engine.current` model.

At creation:

- both blocks start with the same runtime identity;
- `package_sha256` records the exact ZIP used for creation;
- published package source commit provenance is recorded when resolvable;
- `adopted_at` is creation/adoption time;
- `created_with` then remains immutable;
- future updates modify `current` only.

The exact local `current_runtime_root` is never persisted.

## 16. Validation requirements

Implementation must add regression coverage for at least:

- multiple runtime ZIPs may coexist in Project Sources contract;
- package cache paths are isolated by version + digest;
- missing cache silently re-extracts the exact ZIP;
- runtime package resolution never crosses `current_runtime_root`;
- exact digest wins when available;
- same-version descendant commit classifies as forward refresh using one bounded compare;
- ancestor candidate classifies as downgrade;
- diverged candidate is not auto-selected;
- different bytes for the same source commit are not silently accepted;
- foreign campaign user is offered matching-package restore but not migration;
- campaign creator is offered restore or update;
- storage owner and campaign creator authority remain separate;
- successful maintenance resumes the same gameplay decision point;
- exact dialogue is not fabricated when only durable summary evidence exists;
- one-hour dirty ceiling forces publication at the next available boundary;
- clean state does not generate heartbeat commits;
- new campaigns emit only the new engine identity schema.

## 17. Files/contracts expected to change during implementation

At minimum, implementation is expected to touch the active contracts around:

- `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`;
- embedded Project Instructions in `GAME/INSTALL/README.md`;
- `GAME/INSTALL/00_DND_BOOTSTRAP.md`;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`;
- `GAME/CORE/ENGINE_UPDATES.md`;
- durability/session/persistence guidance needed for the one-hour dirty ceiling and post-maintenance continuation;
- `GAME/CAMPAIGN/MANIFEST.yaml`;
- `GAME/SCHEMA/campaign_manifest.schema.yaml`;
- `GAME/TOOLS/init_campaign.py`;
- applicable `DEV/TESTS/` and maintenance-audit rules.

Root `README.md` is outside automatic implementation scope and remains governed by its separate human-curated editorial contract in `AGENTS.md`.

## 18. Design invariants

The implementation is correct only if all of the following remain true:

1. Campaign canon stays only in campaign storage; engine files never become campaign canon.
2. Project Sources/current-chat attachments supply runtime ZIP bytes; extracted runtime-cache is disposable.
3. Multiple engine versions can coexist without cross-package file lookup or mixed CORE context.
4. Campaign MANIFEST stores portable runtime identity/provenance, never environment-specific paths.
5. Same-version forward refresh does not require an obsolete previous ZIP merely because the digest changed.
6. Downgrade is distinguishable from forward refresh without commit-history archaeology.
7. Campaign creator, not generic repository write access or storage ownership, controls campaign engine adoption.
8. Successful maintenance returns the player to the same unresolved gameplay point whenever evidence permits.
9. Dirty unpublished canon cannot be intentionally left solely in ephemeral HOT/SOFT state for more than one hour of active work.
10. No legacy migration/backward-compatibility burden is added to this implementation cycle.