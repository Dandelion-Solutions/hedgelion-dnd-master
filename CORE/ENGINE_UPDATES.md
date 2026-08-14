# Engine Release Updates

framework_module_version: 0.2.3
load_when: storage-owner gameplay startup/resume, explicit engine-update request, safe engine maintenance opportunity, tagged release integration

## Repository roles

Canonical public engine repository: `Dandelion-Solutions/hedgelion-dnd-master`.

Public engine `main` is development state. A release exists only when a valid engine tag exists. Campaign-storage `main` is the locally installed engine baseline and is identified by root `DND_STORAGE.yaml`.

From campaign runtime, public engine tags/main are read-only. D&D Master never publishes campaign/storage changes back to the public engine repository.

## Who may perform engine maintenance

Before any release discovery or engine maintenance, resolve the authenticated GitHub user and selected campaign-storage repository owner.

Only when authenticated login == storage repository owner may D&D Master:
- query for engine releases as part of normal update opportunities;
- change campaign-storage `refs/heads/main`;
- integrate a storage engine baseline into a campaign branch.

A guest Master skips this entire maintenance flow, even if the guest has Write/Admin repository permission, is campaign creator, or has an active PLAYER binding. Guest gameplay continues on the engine already integrated into the selected campaign.

Campaign creator identity remains authoritative for ordinary gameplay/owner operations. Engine maintenance is a separate storage-owner authority. A migration requiring a campaign creator/player decision must stop until the authorized person provides that decision; storage ownership does not grant fictional agency.

## Installed version metadata

Storage `refs/heads/main` has root `DND_STORAGE.yaml`:
- `engine.source_repository` — canonical public engine repository;
- `engine.installed_tag` — published release installed on storage main;
- `engine.installed_sha` — exact public tag commit SHA.

Each campaign manifest tracks its own engine state:
- `base_tag` / `base_sha` — immutable release from which campaign was created;
- `integrated_tag` — most recent release integrated into the campaign;
- `integrated_main_sha` — exact public release commit for that tag;
- `update_policy` — `ask` or `auto`.

A storage baseline may be newer than a campaign. That is valid and does not change gameplay until campaign integration succeeds.

## Update opportunities

Engine maintenance is event-driven, never per-turn polling. For a storage-owner Master, consider an update only at safe opportunities:
- new gameplay chat/session startup or resume after a meaningful pause;
- explicit engine-update request;
- owner maintenance boundary;
- live-epoch rollover after durable compaction and before successor opening, when no other active live epoch blocks global maintenance.

Guest Masters perform no release check.

At an owner opportunity, first compare the active campaign's integrated release with the already-installed storage baseline. Query public release tags only when checking for a release newer than storage `main`.

## Public release discovery

Valid tags follow `RELEASE/VERSIONING.md`. Resolve a candidate tag to exact public commit `T` and validate `ENGINE_VERSION.yaml` at `T`, including tag/version coherence and compatibility metadata.

Never install untagged public `main` commits. If public `main` has work after the latest tag, that work is invisible to storage/gameplay runtime.

## Ask and auto policy

`update_policy: ask` is the default for a campaign.

When storage owner is operating that campaign and a newer installable baseline/release is available, offer:
- `Update`;
- `Not now`;
- `Always update automatically`.

`Not now` is session-local deferral, not a permanent ignored-version list.

`update_policy: auto` allows automatic two-phase maintenance only at safe boundaries and only when all authorization, compatibility, cleanliness and concurrency gates pass. If migration/conflict requires a human decision, defer and ask rather than guessing.

## Safety gates

Before Phase A or B as applicable:
- no unresolved player action/adjudication;
- persist required dirty gameplay state first;
- no authoritative active live epoch in the campaign when global integration would invalidate it;
- validate repository role/owner identity;
- pin relevant storage/campaign HEADs;
- use optimistic concurrency and never force-push;
- `maintenance_required` or missing/unknown compatibility blocks blind auto;
- campaign-local modifications to engine-owned paths touched by the target baseline require bounded maintenance, not silent overwrite.

## Phase A — install release on storage main

If target public tag `T` is newer than `DND_STORAGE.engine.installed_tag` and the owner accepts/auto-allows it:
1. pin current storage `main` HEAD `S` and validate `DND_STORAGE.yaml`;
2. resolve exact public release tree at `T`;
3. construct new storage-main tree as the exact public release tree plus the existing storage-owned `DND_STORAGE.yaml` updated to `installed_tag=T` and `installed_sha=<public tag SHA>`;
4. remove every extra path from old storage `main` that is absent from the release tree, except `DND_STORAGE.yaml`;
5. publish one coherent storage-main maintenance commit with first parent `S`, `force=false`;
6. if storage main moved before publication, rebuild/re-evaluate; never overwrite a concurrent change.

Storage main must not contain gameplay state. Users should not store unrelated custom files there; such files are not preserved by engine baseline replacement.

Only after the storage-main ref update succeeds is the new baseline installed.

## Phase B — integrate storage baseline into a campaign

Let `C` be current campaign HEAD and `S2` the storage-main commit containing the target installed release.

Prepare one campaign maintenance commit:
- preserve populated campaign-owned `CAMPAIGN/**` from `C` except explicit defined migration changes;
- take engine-owned paths from `S2` exactly, including deletion of obsolete engine-owned files;
- exclude `DND_STORAGE.yaml` from the campaign tree; it is storage-main metadata only;
- update campaign manifest `integrated_tag` / `integrated_main_sha` to the public tag/SHA represented by `S2`;
- apply only explicit compatible migration/metadata changes.

Prefer merge-style provenance with first parent `C` and second parent `S2`. The public release commit is in another repository and MUST NOT be used as a cross-repository parent.

Publish the campaign ref with optimistic fast-forward semantics only. If campaign HEAD moved, refresh affected state and re-evaluate. Never force-push.

## Partial success

Phase A and Phase B are separate durable boundaries.

If storage main successfully advances to a newer release but campaign integration is deferred or fails, keep storage main on the newer release and keep the campaign on its old integrated release. Do not rollback the storage baseline merely to make versions equal.

A later owner maintenance opportunity may integrate the already-installed storage baseline without querying public releases again.

## After successful campaign integration

Only after the campaign ref update succeeds:
- consider the release installed for that campaign;
- repin campaign HEAD;
- invalidate cached engine/CORE/rule/bootstrap content that may have changed;
- reload `BOOTSTRAP_RUNTIME.md`, `CORE_INDEX.md`, `RUNTIME.md`, `AI_REASONING.md` and only required situational modules;
- reread only campaign records touched by migration.

Never claim storage or campaign update success before the corresponding GitHub ref update succeeds. Technical maintenance must not fabricate fictional elapsed time/events.
