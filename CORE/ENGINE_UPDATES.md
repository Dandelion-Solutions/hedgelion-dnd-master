# Engine Release Updates

framework_module_version: 0.5.4
load_when: storage-owner startup/resume, explicit engine-update request, safe maintenance opportunity

## Distribution model

Canonical public engine repository:
`Dandelion-Solutions/hedgelion-dnd-master`

Public `main` is development state.

Gameplay engine FILES come from a local D&D Master release ZIP. Campaign storage does not contain an engine copy.

GitHub release/tag metadata may be queried to discover a newer published release, but discovering a tag does not install its files. The user supplies the corresponding release ZIP to Project Sources/current chat.

## Authority

Only authenticated storage repository owner may:
- change storage baseline metadata;
- perform normal release-discovery prompts for that storage;
- approve/perform campaign engine migrations as storage maintenance.

A guest Master:
- does not modify storage metadata;
- does not govern engine updates;
- continues only with an exact engine package matching the campaign, or observes read-only if other access rules permit.

Campaign creator/player decisions required by a migration remain creator/player authority; storage ownership does not grant fictional agency.

## Version metadata

Storage v2:

`DND_STORAGE.yaml -> engine.baseline_version`

This is the approved default version for new campaigns.

Campaign manifest retains exact provenance:
- `base_tag` / `base_sha`
- `integrated_tag` / `integrated_main_sha`
- `update_policy`

A storage baseline may be newer than a campaign. That is valid.

## Update opportunities

No per-turn polling.

For storage owner consider updates only at:
- new chat/session startup/resume after meaningful pause;
- explicit update request;
- owner maintenance boundary;
- safe live-epoch rollover after compaction.

Guests perform no public release discovery as routine maintenance.

## Release discovery

At an owner opportunity, public GitHub tags may be queried.

Valid releases follow `RELEASE/VERSIONING.md`.

If a newer valid tag exists but its release ZIP is not available locally:
1. tell the owner a new release is available;
2. ask them to download GitHub Release **Source code (zip)** and add/attach it;
3. do not attempt to clone/pull/copy the engine from GitHub;
4. do not change storage/campaign engine metadata yet.

Never use untagged public `main` as a normal player release.

## Local package validation

Before adopting local target engine T:
1. read local `ENGINE_VERSION.yaml`;
2. validate version/recommended tag coherence;
3. for normal releases resolve the public tag to exact source commit SHA;
4. respect `campaign_update.compatibility`;
5. ensure the package selected for migration is the target package, not a mix of files from multiple archives.

Explicit development builds are engine-owner test-only.

## Ask / auto policy

Campaign default `update_policy: ask`.

When a newer locally available valid release can be adopted, offer:
- Update
- Not now
- Always update automatically

`Not now` is session-local deferral.

`auto` may proceed only at safe boundaries and only with a locally available validated target ZIP. Auto never downloads/reconstructs engine files itself.

## Phase A — storage baseline metadata

If storage owner approves local engine version T for new campaigns:
1. pin storage default-branch HEAD;
2. update only `DND_STORAGE.yaml -> engine.baseline_version` to T;
3. publish one coherent non-force metadata commit.

No engine files are copied to storage.
No unrelated storage files are deleted/replaced.

Phase A is optional for updating an existing campaign but normally keeps the default aligned with the owner's current release.

## Phase B — campaign engine adoption

Existing campaign engine adoption changes campaign DATA/metadata, not engine-owned file paths.

Let C be current campaign HEAD and target local release T.

Before migration:
- persist required dirty gameplay state;
- ensure no blocking active live epoch;
- pin C;
- validate target compatibility/migrations;
- load only migration/schema files required from the local target package.

Prepare one campaign maintenance batch:
- apply explicit required campaign data/schema migrations;
- preserve all unrelated campaign canon;
- update manifest `integrated_tag` and `integrated_main_sha` to T;
- keep immutable `base_tag/base_sha`;
- never copy CORE/RULES/SCHEMA/INSTALL files into the campaign branch.

Publish with optimistic non-force semantics. If HEAD moved, refresh affected state and re-evaluate.

## Engine mismatch at startup

If campaign integrated engine != current local package:
- do not silently use the wrong engine;
- prefer loading the exact matching release ZIP;
- owner may choose an authorized upgrade if target is newer and compatible;
- guest must supply/use matching release ZIP rather than upgrading storage/campaign.

## Partial success

Storage baseline metadata update and campaign migration are separate durable boundaries.

If baseline moves to T but campaign migration is deferred/fails, keep baseline at T and campaign on old release. Do not rollback merely to equalize versions.

## After successful campaign update

Only after campaign publication succeeds:
- repin campaign HEAD;
- switch runtime to the exact local target package;
- invalidate old loaded CORE/rule/bootstrap caches;
- reload target `BOOTSTRAP_RUNTIME.md`, `CORE_INDEX.md`, `RUNTIME.md`, `AI_REASONING.md`;
- reread only campaign records touched by migration.

Never claim update success before GitHub publication succeeds. Technical maintenance must not fabricate fictional elapsed time/events.
